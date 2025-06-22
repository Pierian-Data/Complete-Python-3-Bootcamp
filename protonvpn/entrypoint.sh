#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "ProtonVPN Entrypoint Script Started"

# Check if credentials are provided
if [ -z "$PROTONVPN_USERNAME" ] || [ -z "$PROTONVPN_PASSWORD" ]; then
  echo "Error: PROTONVPN_USERNAME and PROTONVPN_PASSWORD must be set as environment variables."
  exit 1
fi

echo "Initializing ProtonVPN CLI and logging in..."
# Attempt to initialize ProtonVPN.
# The input '1' selects OpenVPN protocol.
# Then username and password are provided.
# Using sudo as the protonuser needs it for this command.
# Adding error handling for init
if ! sudo protonvpn init <<EOF
1
${PROTONVPN_USERNAME}
${PROTONVPN_PASSWORD}
EOF
then
  echo "ProtonVPN init failed. Please check credentials and if the CLI is working."
  # Attempt to logout in case of partial previous session
  sudo protonvpn logout || echo "Logout attempt failed or was not necessary."
  # Retry init once after logout, as sometimes stale sessions can cause issues
  echo "Retrying ProtonVPN init..."
  if ! sudo protonvpn init <<EOF
1
${PROTONVPN_USERNAME}
${PROTONVPN_PASSWORD}
EOF
  then
    echo "ProtonVPN init failed on retry. Exiting."
    exit 1
  fi
fi
echo "ProtonVPN initialized successfully."


# Determine server to connect to
CONNECT_ARGS=""
if [ -n "$PROTONVPN_SERVER" ]; then
    echo "Connecting to specified ProtonVPN server: ${PROTONVPN_SERVER} (P2P)"
    # Ensure --p2p is included if a specific server is named, assuming it's for P2P.
    # The user should pick a P2P server if that's the intent.
    # Most official server names don't need --p2p if they are already P2P optimized.
    # However, protonvpn-cli connect <SERVER_NAME> --p2p is valid.
    # Forcing protocol to OpenVPN UDP as it's generally good for performance/stability with torrents.
    CONNECT_ARGS="${PROTONVPN_SERVER} --protocol udp"
else
    echo "Connecting to the fastest ProtonVPN P2P server with UDP protocol..."
    CONNECT_ARGS="--p2p --fastest --protocol udp"
fi

# Connect to ProtonVPN
echo "Attempting to connect: sudo protonvpn connect ${CONNECT_ARGS}"
if ! sudo protonvpn connect ${CONNECT_ARGS}; then
    echo "ProtonVPN connect command failed. Check server name or network."
    # Try a more generic connection if specific one failed
    echo "Attempting connection to fastest P2P server as a fallback..."
    if ! sudo protonvpn connect --p2p --fastest --protocol udp; then
        echo "Fallback ProtonVPN connection also failed. Exiting."
        exit 1
    fi
fi

echo "ProtonVPN connection established."
echo "Verifying external IP address (will try a few sources):"
external_ip=$(curl -s --max-time 10 ifconfig.me || curl -s --max-time 10 api.ipify.org || curl -s --max-time 10 checkip.amazonaws.com)
if [ -n "$external_ip" ]; then
    echo "External IP: $external_ip"
else
    echo "Could not fetch external IP. VPN might not be routing traffic correctly."
fi
echo ""

# Keep the script running and monitor the VPN connection.
while true; do
  if sudo protonvpn status | grep -q -E "Connected to|Status: Connected"; then
    current_time=$(date)
    # echo "VPN Connection active at $current_time" # Can be verbose
    # Let's check the IP periodically as well as a sanity check
    # new_external_ip=$(curl -s --max-time 10 ifconfig.me)
    # if [ "$new_external_ip" != "$external_ip" ] && [ -n "$new_external_ip" ]; then
    #   echo "Warning: External IP changed from $external_ip to $new_external_ip at $current_time"
    #   external_ip=$new_external_ip
    # elif [ -z "$new_external_ip" ]; then
    #   echo "Warning: Could not fetch external IP for check at $current_time"
    # fi
    sleep 60 # Check every 60 seconds
  else
    echo "ProtonVPN disconnected at $(date). Attempting to reconnect..."
    if ! sudo protonvpn connect ${CONNECT_ARGS}; then
        echo "Reconnect attempt with primary args failed. Trying fallback (fastest P2P)..."
        if ! sudo protonvpn connect --p2p --fastest --protocol udp; then
            echo "Fallback reconnect failed. Waiting 30s before retrying primary..."
            sleep 30
        else
            echo "Reconnected with fallback server."
            external_ip=$(curl -s --max-time 10 ifconfig.me || curl -s --max-time 10 api.ipify.org) # Update IP
            echo "New External IP: $external_ip"
        fi
    else
        echo "Reconnected with primary server/args."
        external_ip=$(curl -s --max-time 10 ifconfig.me || curl -s --max-time 10 api.ipify.org) # Update IP
        echo "New External IP: $external_ip"
    fi
  fi
done

# Fallback if the loop exits (it shouldn't).
echo "Entrypoint script unexpected exit."
