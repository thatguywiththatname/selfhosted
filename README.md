# Apollo

(Front|Back)end code for my personal server + website

Server Stack:

- [Hetzner CX11 Server](https://www.hetzner.com/cloud)
  - Debian 10 Minimal
    - [UFW](https://wiki.debian.org/Uncomplicated%20Firewall%20%28ufw%29)
    - [Caddy](https://caddyserver.com/)
    - [Docker](https://www.docker.com/)
      - [Fail2ban](https://github.com/crazy-max/docker-fail2ban)
      - [SpaceXLaunchBot](https://github.com/r-spacex/SpaceXLaunchBot)

## Setup

```bash
git clone https://github.com/psidex/apollo ~/apollo && cd ~/apollo && sudo bash setup
```
