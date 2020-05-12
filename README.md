# Apollo

(Front|Back)end code for my personal server + website.

Server Stack:

- [Hetzner CX11 Server](https://www.hetzner.com/cloud)
  - Debian 10 Minimal
    - [UFW](https://wiki.debian.org/Uncomplicated%20Firewall%20%28ufw%29)
    - [Docker](https://www.docker.com/)
      - [Caddy](https://caddyserver.com/) as a reverse proxy with https
      - [Fail2ban](https://github.com/crazy-max/docker-fail2ban)
      - [SpaceXLaunchBot](https://github.com/r-spacex/SpaceXLaunchBot)
      - [goStatic](https://github.com/PierreZ/goStatic)
      - [Watchtower](https://github.com/containrrr/watchtower)

## Setup

```bash
git clone https://github.com/psidex/Apollo ~/Apollo && cd ~/Apollo && sudo bash setup
```

The setup script will remove the `~/Apollo` directory after it is run, but will leave
the `update-site` script in `~`. It also installs the `unattended-upgrades` package,
but it must be [set up](https://libre-software.net/ubuntu-automatic-updates/) afterwards
for it to work.

All files used by docker containers are stored in `/etc/dockercontainerfiles`, such as
volumes and config files.
