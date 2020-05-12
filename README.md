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

## Setup

```bash
git clone https://github.com/psidex/Apollo ~/Apollo && cd ~/Apollo && sudo bash setup
```

All files used by docker images are stored in `/etc/dockercontainerfiles`.

The `Apollo` directory can be deleted after `setup` is run.
