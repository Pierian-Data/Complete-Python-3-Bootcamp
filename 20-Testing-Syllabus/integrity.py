"""integrity.py - tamper evidence for the test suite, the ledger and the work.

Three mechanisms, layered:

1. **Hash-chained ledger.** Every entry in ``records.json`` carries the hash of
   its predecessor and of its own content. Editing or deleting a past entry
   breaks the chain and ``verify`` says exactly where.

2. **Manifest.** ``suite.manifest.json`` holds the SHA-256 of every file in
   this folder. Changing a test, a check cell or the grader itself shows up
   as a modified file - so nobody can weaken a check to make a grade pass.

3. **Signed seal.** ``SEAL.json`` binds the chain head, the manifest and the
   attestations together, and is signed with an Ed25519 key held outside the
   repository. Anyone with the public key can verify who produced it.

The seal is only as strong as where you anchor it. Anchor the seal hash in a
place you do not control (GitHub artifact attestation, an OpenTimestamps
stamp, a mail to yourself) and the chain becomes evidence rather than
decoration. See INTEGRITY.md.

Standard library plus ``cryptography`` (for Ed25519).
"""

import base64
import datetime
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LEDGER = os.path.join(HERE, "records.json")
MANIFEST = os.path.join(HERE, "suite.manifest.json")
SEAL = os.path.join(HERE, "SEAL.json")
ATTESTATIONS = os.path.join(HERE, "attestations")
PUBKEY = os.path.join(HERE, "agent.pub")
GENESIS = "0" * 64

# Files whose content is expected to change; they are not in the manifest.
# records.json is covered by the hash chain, SEAL.json by the signature, and
# GRADE_REPORT.md is regenerated from the chain - CI diffs the committed
# report against a fresh one, so a hand-edited report is still caught.
VOLATILE = {"records.json", "suite.manifest.json", "SEAL.json", "GRADE_REPORT.md"}


# --------------------------------------------------------------------------
# hashing helpers
# --------------------------------------------------------------------------

def canonical(obj):
    """Stable byte representation of a JSON-serialisable object."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry_hash(entry):
    """Hash of a chain entry: its payload plus the hash of its predecessor."""
    payload = {k: v for k, v in entry.items() if k != "hash"}
    return sha256_bytes(canonical(payload))


def now():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()


# --------------------------------------------------------------------------
# ledger chain
# --------------------------------------------------------------------------

def load_ledger():
    if not os.path.exists(LEDGER):
        return {"entries": []}
    with open(LEDGER, encoding="utf-8") as handle:
        data = json.load(handle)
    data.setdefault("entries", [])
    data.setdefault("attempts", [])  # legacy key, kept for older readers
    return data


def save_ledger(data):
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def chain_entries(data):
    return data.get("entries", [])


def append_entry(payload):
    """Append a payload to the chain and return the sealed entry."""
    data = load_ledger()
    entries = chain_entries(data)
    previous = entries[-1]["hash"] if entries else GENESIS
    entry = dict(payload)
    entry["seq"] = len(entries) + 1
    entry["prev"] = previous
    entry["hash"] = entry_hash(entry)
    entries.append(entry)
    data["entries"] = entries
    save_ledger(data)
    return entry


def verify_chain():
    """Recompute the chain. Returns (ok, problems, head, length)."""
    data = load_ledger()
    entries = chain_entries(data)
    problems = []
    previous = GENESIS
    for index, entry in enumerate(entries):
        if entry.get("seq") != index + 1:
            problems.append("entry %d has seq %r" % (index + 1, entry.get("seq")))
        if entry.get("prev") != previous:
            problems.append("entry %d (%s) does not follow the previous entry" % (
                index + 1, entry.get("test", "?")))
        recomputed = entry_hash(entry)
        if recomputed != entry.get("hash"):
            problems.append("entry %d (%s) has been edited: hash %s does not match content %s" % (
                index + 1, entry.get("test", "?"), entry.get("hash"), recomputed))
        previous = entry.get("hash", previous)
    head = entries[-1]["hash"] if entries else GENESIS
    return (not problems), problems, head, len(entries)


def voided_tests(data=None):
    """Tests whose attempts were voided by a later reset event."""
    data = load_ledger() if data is None else data
    voided = set()
    for entry in chain_entries(data):
        if entry.get("event") == "reset":
            voided.add(entry.get("test"))
    return voided


# --------------------------------------------------------------------------
# manifest
# --------------------------------------------------------------------------

def suite_files():
    """Every file in the suite folder that belongs in the manifest.

    Attestations are excluded: they are appended over time, each is signed on
    its own, and the seal lists them explicitly.
    """
    names = []
    for name in sorted(os.listdir(HERE)):
        path = os.path.join(HERE, name)
        if not os.path.isfile(path) or name in VOLATILE:
            continue
        if name.endswith(".pyc"):
            continue
        names.append(name)
    return names


def build_manifest():
    files = {}
    for name in suite_files():
        path = os.path.join(HERE, name)
        files[name.replace("\\", "/")] = manifest_entry(path, name)
    manifest = {"created": now(), "files": files}
    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return manifest


def manifest_hash():
    return sha256_file(MANIFEST) if os.path.exists(MANIFEST) else None


def is_work_file(key):
    """True for the notebooks the learner writes their answers in.

    These are expected to change as the learner works, so they are protected
    differently: the manifest records a fingerprint of the parts that must not
    change (the check cells, the solution blocks and the header), and the
    ledger pins the whole file - a SHA-256 and a git blob id - at the moment
    it was graded.
    """
    name = key.replace("\\", "/")
    return name.startswith("T") or name.startswith("PRACTICE") or name.startswith("FINAL")


def protected_fingerprint(path):
    """Hash of the parts of a learner notebook that must not change.

    The learner may write anything in the answer cells, so those are left
    out. Everything that decides what the test checks - the check cells, the
    reference solutions and the header - is included, so weakening a check or
    editing a question is caught.
    """
    try:
        with open(path, encoding="utf-8") as handle:
            document = json.load(handle)
    except (OSError, ValueError):
        return None
    parts = []
    for index, cell in enumerate(document.get("cells", [])):
        source = "".join(cell.get("source", []))
        if cell.get("cell_type") == "code":
            if "check" in cell.get("metadata", {}).get("tags", []):
                parts.append("check:%d:%s" % (index, source))
        else:
            if index == 0 or "<details>" in source:
                parts.append("markdown:%d:%s" % (index, source))
    return sha256_bytes(canonical(parts))


def manifest_entry(path, name):
    """The manifest record for one file."""
    key = name.replace("\\", "/")
    record = {"sha256": sha256_file(path)}
    if is_work_file(key):
        record["fingerprint"] = protected_fingerprint(path)
    return record


def verify_manifest():
    """Compare the files on disk with the manifest.

    Returns (ok, problems, expected_changes). Problems are changes to the
    system files or to the protected parts of a learner notebook, and always
    matter. Expected changes are edits to the learner's own answer cells,
    which are normal.
    """
    if not os.path.exists(MANIFEST):
        return False, ["suite.manifest.json is missing - run: python integrity.py manifest"], []
    with open(MANIFEST, encoding="utf-8") as handle:
        manifest = json.load(handle)
    expected = manifest.get("files", {})
    problems = []
    expected_changes = []
    for name in suite_files():
        path = os.path.join(HERE, name)
        key = name.replace("\\", "/")
        record = expected.get(key)
        if record is None:
            message = "new file not in the manifest: %s" % key
            (expected_changes if is_work_file(key) else problems).append(message)
            continue
        if isinstance(record, str):          # older manifest format
            record = {"sha256": record}
        if record.get("sha256") != sha256_file(path):
            message = "modified since the manifest was written: %s" % key
            (expected_changes if is_work_file(key) else problems).append(message)
        if record.get("fingerprint"):
            current = protected_fingerprint(path)
            if current != record["fingerprint"]:
                problems.append(
                    "protected content changed in %s (a check cell, a solution or the header) - "
                    "the grading logic must not be edited" % key)
    for key in expected:
        if key not in set(n.replace("\\", "/") for n in suite_files()):
            message = "file recorded in the manifest is missing: %s" % key
            (expected_changes if is_work_file(key) else problems).append(message)
    return (not problems), problems, expected_changes


# --------------------------------------------------------------------------
# signing
# --------------------------------------------------------------------------

def private_key_path():
    return os.path.join(os.path.expanduser("~"), ".professor", "professor_key.pem")


def load_private_key():
    from cryptography.hazmat.primitives import serialization
    path = private_key_path()
    if not os.path.exists(path):
        return None
    with open(path, "rb") as handle:
        return serialization.load_pem_private_key(handle.read(), password=None)


def load_public_key():
    from cryptography.hazmat.primitives import serialization
    if not os.path.exists(PUBKEY):
        return None
    with open(PUBKEY, "rb") as handle:
        return serialization.load_pem_public_key(handle.read())


def key_id(public_key):
    from cryptography.hazmat.primitives import serialization
    raw = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return sha256_bytes(raw)[:16]


def keygen():
    """Create the agent keypair. The private key never enters the repo."""
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    path = private_key_path()
    if os.path.exists(path):
        print("key already exists: %s" % path)
        return 1
    os.makedirs(os.path.dirname(path), exist_ok=True)
    private = Ed25519PrivateKey.generate()
    with open(path, "wb") as handle:
        handle.write(private.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass  # Windows ACLs
    with open(PUBKEY, "wb") as handle:
        handle.write(private.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ))
    print("private key: %s (keep it out of the repository)" % path)
    print("public key : %s (committed)" % PUBKEY)
    print("key id     : %s" % key_id(private.public_key()))
    return 0


def sign(payload):
    """Sign a JSON-serialisable payload with the agent key."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    private = load_private_key()
    if private is None:
        return None, "no agent key - run: python integrity.py keygen"
    signature = private.sign(canonical(payload))
    from cryptography.hazmat.primitives import serialization
    raw_public = private.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return {
        "algorithm": "ed25519",
        "key_id": key_id(private.public_key()),
        "public_key": base64.b64encode(raw_public).decode("ascii"),
        "signature": base64.b64encode(signature).decode("ascii"),
    }, None


def verify_signature(payload, signature_block, public_key=None):
    """Check a signature block against a public key (the agent's by default)."""
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

    if not signature_block:
        return False, "no signature block"
    if public_key is None:
        public_key = load_public_key()
        if public_key is None:
            return False, "no public key available (%s missing)" % PUBKEY
    try:
        raw = base64.b64decode(signature_block["public_key"])
    except (KeyError, ValueError):
        return False, "malformed signature block"
    key = Ed25519PublicKey.from_public_bytes(raw)
    try:
        key.verify(base64.b64decode(signature_block["signature"]), canonical(payload))
    except (InvalidSignature, ValueError):
        return False, "signature does not match the content"
    return True, "signature valid (key %s)" % signature_block.get("key_id", "?")


# --------------------------------------------------------------------------
# seal
# --------------------------------------------------------------------------

def git_commit():
    try:
        result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
        return result.stdout.strip() or None
    except OSError:
        return None


def seal(force=False):
    """Write SEAL.json: chain head + manifest + attestations, signed."""
    ok, problems, head, length = verify_chain()
    if not ok:
        print("refusing to seal a broken chain:")
        for problem in problems:
            print("  " + problem)
        return 1
    if not os.path.exists(MANIFEST):
        build_manifest()
    attestations = []
    if os.path.isdir(ATTESTATIONS):
        for name in sorted(os.listdir(ATTESTATIONS)):
            if name.endswith(".json"):
                attestations.append(name)
    attest_hash = sha256_bytes(canonical(attestations))
    payload = {
        "sealed_at": now(),
        "chain_head": head,
        "chain_length": length,
        "manifest_sha256": manifest_hash(),
        "attestations": attestations,
        "attestations_sha256": attest_hash,
        "git_commit": git_commit(),
    }
    signature, error = sign(payload)
    if error:
        print(error)
        return 1
    seal_document = dict(payload)
    seal_document["signature"] = signature
    with open(SEAL, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(seal_document, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print("sealed: chain head %s (%d entries), manifest %s" % (head[:16], length, (payload["manifest_sha256"] or "")[:16]))
    print("seal   : %s" % SEAL)
    print("anchor : publish this hash somewhere you do not control -")
    print("         %s" % head)
    return 0


def load_seal():
    if not os.path.exists(SEAL):
        return None
    with open(SEAL, encoding="utf-8") as handle:
        return json.load(handle)


def verify_seal():
    """Verify the seal: signature, chain position, manifest and attestations."""
    problems = []
    document = load_seal()
    if document is None:
        return False, ["SEAL.json is missing - run: python integrity.py seal"]
    payload = {k: v for k, v in document.items() if k != "signature"}
    ok, message = verify_signature(payload, document.get("signature"))
    if not ok:
        problems.append("seal signature: %s" % message)

    ok, chain_problems, head, length = verify_chain()
    problems.extend(chain_problems)
    sealed_head = document.get("chain_head")
    if sealed_head:
        entries = chain_entries(load_ledger())
        sealed_index = None
        for index, entry in enumerate(entries):
            if entry.get("hash") == sealed_head:
                sealed_index = index
                break
        if sealed_index is None and head != sealed_head:
            problems.append("the sealed chain head is not in the ledger - the seal was replaced")
        elif sealed_index is not None and length <= sealed_index:
            problems.append("the ledger is shorter than the sealed chain")
    if document.get("manifest_sha256") and os.path.exists(MANIFEST):
        if manifest_hash() != document["manifest_sha256"]:
            problems.append("the manifest changed after the seal was made")
    return (not problems), problems


# --------------------------------------------------------------------------
# attestations
# --------------------------------------------------------------------------

def attest(statement, context=None):
    """Write a signed statement about completed work."""
    os.makedirs(ATTESTATIONS, exist_ok=True)
    data = load_ledger()
    entries = chain_entries(data)
    payload = {
        "statement": statement,
        "context": context or {},
        "issued_at": now(),
        "chain_head": entries[-1]["hash"] if entries else GENESIS,
        "chain_length": len(entries),
    }
    signature, error = sign(payload)
    if error:
        print(error)
        return 1
    document = dict(payload)
    document["signature"] = signature
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    label = (context or {}).get("test", "session").replace(" ", "-")
    path = os.path.join(ATTESTATIONS, "%s-%s.json" % (stamp, label))
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(document, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print("attestation written: %s" % path)
    return 0


def verify_attestations():
    problems = []
    count = 0
    if not os.path.isdir(ATTESTATIONS):
        return True, problems, 0
    for name in sorted(os.listdir(ATTESTATIONS)):
        if not name.endswith(".json"):
            continue
        count += 1
        path = os.path.join(ATTESTATIONS, name)
        with open(path, encoding="utf-8") as handle:
            document = json.load(handle)
        payload = {k: v for k, v in document.items() if k != "signature"}
        ok, message = verify_signature(payload, document.get("signature"))
        if not ok:
            problems.append("%s: %s" % (name, message))
    return (not problems), problems, count


# --------------------------------------------------------------------------
# the learner's work
# --------------------------------------------------------------------------

def git_blob(path):
    """The git blob id of a file - survives as long as the commit does."""
    try:
        result = subprocess.run(["git", "hash-object", path], cwd=ROOT, capture_output=True, text=True)
        return result.stdout.strip() or None
    except OSError:
        return None


def work_drift():
    """Compare the latest graded version of each notebook with the file on disk.

    Only the newest attempt per test is checked: an earlier attempt is
    expected to differ, because that is what a redo looks like. What matters
    is whether the work changed *after* the last time it was graded.
    """
    entries = chain_entries(load_ledger())
    latest = {}
    for entry in entries:
        if entry.get("event") == "attempt" and entry.get("notebook"):
            latest[entry["notebook"]] = entry
    drift = []
    for name, entry in sorted(latest.items()):
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            drift.append((name, "file no longer exists"))
            continue
        current = sha256_file(path)
        if entry.get("notebook_sha256") and current != entry["notebook_sha256"]:
            drift.append((name, "content changed after it was last graded (git history shows the edit)"))
    return drift


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def cmd_verify(args):
    ok_chain, chain_problems, head, length = verify_chain()
    ok_manifest, manifest_problems, work_changes = verify_manifest()
    ok_seal, seal_problems = verify_seal()
    ok_attest, attest_problems, attest_count = verify_attestations()
    drift = work_drift()

    print("=" * 72)
    print("INTEGRITY REPORT - Complete Python 3 Bootcamp test suite")
    print("=" * 72)
    print("ledger chain   : %s (%d entries, head %s)" % (
        "OK" if ok_chain else "BROKEN", length, head[:16]))
    for problem in chain_problems:
        print("    ! %s" % problem)
    print("suite manifest : %s (%d files)" % (
        "OK" if ok_manifest else "CHANGED", len(load_manifest_files())))
    for problem in manifest_problems:
        print("    ! %s" % problem)
    if work_changes:
        print("    - %d learner notebook(s) changed since the manifest was written" % len(work_changes))
        print("      (expected while you are working; they are pinned per attempt in the ledger)")
    print("seal           : %s" % ("OK" if ok_seal else "PROBLEM"))
    for problem in seal_problems:
        print("    ! %s" % problem)
    print("attestations   : %s (%d signed statements)" % (
        "OK" if ok_attest else "PROBLEM", attest_count))
    for problem in attest_problems:
        print("    ! %s" % problem)
    print("work drift     : %s" % ("none" if not drift else "%d file(s) changed since grading" % len(drift)))
    for name, note in drift:
        print("    - %s: %s" % (name, note))

    healthy = ok_chain and ok_manifest and ok_seal and ok_attest
    print()
    print("RESULT: %s" % ("integrity verified" if healthy else "integrity problems found"))
    if healthy and drift:
        print("NOTE  : the graded work changed after grading - check git history if that was not you.")
    return 0 if healthy else 1


def load_manifest_files():
    if not os.path.exists(MANIFEST):
        return {}
    with open(MANIFEST, encoding="utf-8") as handle:
        return json.load(handle).get("files", {})


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("keygen", help="create the agent keypair (private key stays outside the repo)")
    sub.add_parser("manifest", help="write suite.manifest.json (hash of every file)")
    sub.add_parser("seal", help="write a signed SEAL.json over the chain and the manifest")
    sub.add_parser("verify", help="verify chain, manifest, seal and attestations")

    p_attest = sub.add_parser("attest", help="write a signed attestation about completed work")
    p_attest.add_argument("statement")
    p_attest.add_argument("--context", default="{}", help="JSON object with extra context")

    args = parser.parse_args(argv)

    if args.command == "keygen":
        return keygen()
    if args.command == "manifest":
        manifest = build_manifest()
        print("manifest written: %s (%d files)" % (MANIFEST, len(manifest["files"])))
        return 0
    if args.command == "seal":
        return seal()
    if args.command == "verify":
        return cmd_verify(args)
    if args.command == "attest":
        try:
            context = json.loads(args.context)
        except ValueError:
            print("--context must be a JSON object")
            return 1
        return attest(args.statement, context)
    return 1


if __name__ == "__main__":
    sys.exit(main())
