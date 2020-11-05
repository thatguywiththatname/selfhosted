# Apollo

(Front|Back)end code for my personal server + website.

Server Stack:

- [Hetzner CX11 Server](https://www.hetzner.com/cloud)
  - Debian 10 Minimal
    - [UFW](https://wiki.debian.org/Uncomplicated%20Firewall%20%28ufw%29)+
    - [Fail2Ban](https://www.fail2ban.org)
    - [Docker](https://www.docker.com/)
      - [Ouroboros](https://github.com/pyouroboros/ouroboros)
      - [Caddy](https://caddyserver.com/) as a reverse proxy with https
        - [psm](https://psm.simonj.tech)
        - [messenger stats](https://messenger.simonj.tech)
        - [goStatic](https://github.com/PierreZ/goStatic)
      - [SpaceXLaunchBot](https://github.com/r-spacex/SpaceXLaunchBot) (setup not included in this repo)
