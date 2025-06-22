# qBittorrent with ProtonVPN via Docker Compose (ARM64 Ready)

This project sets up qBittorrent to run through a ProtonVPN connection using Docker Compose. All qBittorrent traffic will be routed through the VPN. This setup is optimized for ARM64 devices like the Raspberry Pi (4B, 5, etc.) but will also work on x86-64 architectures.

## Features

-   **Secure Torrenting:** All qBittorrent traffic is routed through ProtonVPN.
-   **ARM64 Compatible:** Designed to work on Raspberry Pi and other ARM64 devices. Also compatible with x86-64.
-   **qBittorrent Web UI on Port 9090:** Access qBittorrent remotely.
-   **Easy Configuration:** Primarily via a simple `.env` file for your ProtonVPN credentials.
-   **Persistent Configuration:** qBittorrent settings are saved in a Docker volume.
-   **Local Download Directory:** Maps to a `./downloads` folder on your host.
-   **Healthcheck:** Ensures qBittorrent only starts/runs when the VPN is confirmed active.
-   **Kill Switch:** If the VPN container stops, qBittorrent loses network access.

## Prerequisites

-   Docker: [Install Docker](https://docs.docker.com/get-docker/)
-   Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop or installed via pip)
-   A ProtonVPN account (free or paid).
    -   You need your **OpenVPN/IKEv2 username and password**. Find these by logging into your ProtonVPN account at [account.protonvpn.com/account](https://account.protonvpn.com/account) and navigating to `Account -> OpenVPN/IKEv2 username`.

## "Plug and Play" Setup

The goal is to make this as close to "plug and play" as possible after providing your ProtonVPN credentials.

1.  **Clone the Repository or Download Files:**
    ```bash
    # Example if you have git installed
    # git clone <repository_url>
    # cd <repository_name>
    # If downloaded, extract and navigate to the project directory
    ```

2.  **Create `.env` File for Credentials:**
    Copy the provided `example.env` file to `.env`:
    ```bash
    cp example.env .env
    ```
    Now, **edit the `.env` file** with your ProtonVPN OpenVPN/IKEv2 username and password:
    ```dotenv
    # .env
    PROTONVPN_USERNAME=your_protonvpn_openvpn_username
    PROTONVPN_PASSWORD=your_protonvpn_openvpn_password

    # Optional: Specify a ProtonVPN server (e.g., NL-FREE#1, US-CA#123, JP-TOR#1)
    # If left empty or commented out, the fastest P2P server will be chosen automatically.
    # PROTONVPN_SERVER=NL-FREE#1

    # Optional: Override default PUID/PGID if needed for file permissions on downloads
    # PUID=1000
    # PGID=1000
    # TZ=America/New_York
    ```
    *   **This is the main configuration step you need to perform.**
    *   For `PROTONVPN_SERVER`, you can leave it blank to automatically connect to the fastest P2P server, or specify one. Find server names via `protonvpn-cli servers` (once running) or the ProtonVPN website.

3.  **Create Downloads Directory:**
    This directory will store your downloaded files on the host machine.
    ```bash
    mkdir downloads
    ```
    *(If you change the PUID/PGID in `.env`, ensure this directory's ownership or permissions align if you encounter permission issues with downloaded files.)*

## Usage

1.  **Build and Start the Services:**
    From the project directory (where `docker-compose.yml` is located):
    ```bash
    docker-compose up --build -d
    ```
    -   `--build`: Builds the custom Docker images the first time or if Dockerfiles change.
    -   `-d`: Runs the containers in detached mode (in the background).
    -   This might take a few minutes on the first run, especially on devices like a Raspberry Pi, as it builds the `protonvpn` image.

2.  **Access qBittorrent Web UI:**
    Once the `protonvpn` container is healthy and connected (see `docker-compose ps` or `docker-compose logs protonvpn`), you can access the qBittorrent Web UI at:
    [http://localhost:9090](http://localhost:9090)
    (Replace `localhost` with your Raspberry Pi's IP address if accessing from another device on your network).

    Default qBittorrent credentials:
    -   Username: `admin`
    -   Password: `adminadmin`
    **IMPORTANT: Change these default credentials immediately after your first login!** (Tools -> Options... -> Web UI tab)

3.  **Check VPN Status & Logs:**
    -   To see the status of your containers: `docker-compose ps`
    -   To view logs for the ProtonVPN container (shows connection status, IP):
        ```bash
        docker-compose logs protonvpn
        ```
    -   To view logs for qBittorrent:
        ```bash
        docker-compose logs qbittorrent
        ```

4.  **Stopping the Services:**
    ```bash
    docker-compose down
    ```
    To stop and remove volumes (this will delete qBittorrent's configuration):
    ```bash
    docker-compose down -v
    ```

## Configuration Details

-   **ARM64 (Raspberry Pi):** The `protonvpn/Dockerfile` uses an `arm64v8/ubuntu` base. The `linuxserver/qbittorrent` image is multi-arch, supporting ARM64.
-   **Performance on Raspberry Pi:** While functional, performance (VPN speed, torrent processing) on Raspberry Pi will depend on the model, SD card speed, and network connection. Use a good quality power supply and consider an SSD for downloads for better performance.
-   **ProtonVPN Server:** If `PROTONVPN_SERVER` in `.env` is empty, the `entrypoint.sh` script connects to the fastest P2P server using UDP.
-   **qBittorrent Ports:**
    -   Web UI: `9090`
    -   Incoming P2P: `6881` (TCP/UDP). These are exposed through the VPN.
-   **File Permissions:** The `PUID` and `PGID` environment variables (default to 1000) in `docker-compose.yml` (and overridable in `.env`) control the user under which qBittorrent runs. This affects file ownership in the `./downloads` directory. If your host user ID is different, you might want to adjust these. Find your user's ID with `id -u` and group ID with `id -g`.

## Updating

-   **To update qBittorrent (if a new `linuxserver/qbittorrent:latest` is out):**
    ```bash
    docker-compose pull qbittorrent
    docker-compose up --build -d --remove-orphans
    ```
-   **To rebuild the `protonvpn` image (e.g., for OS updates or ProtonVPN CLI updates):**
    ```bash
    docker-compose build protonvpn
    docker-compose up -d --remove-orphans
    ```

## Troubleshooting

-   **ProtonVPN Connection Issues:**
    -   Check `docker-compose logs protonvpn`.
    -   Verify `PROTONVPN_USERNAME` and `PROTONVPN_PASSWORD` in `.env` are your OpenVPN/IKEv2 credentials.
    -   Try a specific `PROTONVPN_SERVER` or leave it blank for automatic. Ensure the server supports P2P.
    -   Ensure your ProtonVPN account is active.
-   **qBittorrent Web UI Not Accessible at `http://localhost:9090`:**
    -   Run `docker-compose ps`. Ensure `protonvpn` service is `healthy` and `qbittorrent` is `running`.
    -   Check `docker-compose logs qbittorrent`.
    -   Ensure no other service on your host is using port `9090`.
-   **Permission Denied for `/dev/net/tun` (protonvpn container):**
    -   This usually means the TUN module isn't loaded on the Docker host or Docker lacks permission.
    -   On Linux hosts, try: `sudo modprobe tun`.
    -   The `cap_add: [NET_ADMIN, SYS_MODULE]` and `devices: [/dev/net/tun:/dev/net/tun]` in `docker-compose.yml` should handle this on most systems.
-   **Slow Speeds on Raspberry Pi:**
    -   Use a wired Ethernet connection.
    -   Ensure your Pi has adequate cooling.
    -   Select a ProtonVPN server geographically close to you.
    -   Limit the number of active torrents/connections in qBittorrent.

## Security

-   **Change qBittorrent Default Credentials!**
-   Protect your `.env` file; it contains your VPN credentials. `chmod 600 .env`.
-   The included `.gitignore` prevents committing `.env` by default.
-   **Port Forwarding:** This setup does **not** handle automatic port forwarding from ProtonVPN to qBittorrent. For optimal seeding, port forwarding is beneficial. ProtonVPN's paid plans offer this. You'd need to configure it on the ProtonVPN website and then set that specific port in qBittorrent's listening port settings. This is an advanced step.

Enjoy your secure and private qBittorrent setup!
