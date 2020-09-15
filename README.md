# Apollo

(Front|Back)end code for my personal server + website.

Server Stack:

- [Hetzner CX11 Server](https://www.hetzner.com/cloud)
  - Debian 10 Minimal
    - [UFW](https://wiki.debian.org/Uncomplicated%20Firewall%20%28ufw%29)
    - [Docker](https://www.docker.com/)
      - [Ouroboros](https://github.com/pyouroboros/ouroboros)
      - [Fail2ban](https://github.com/crazy-max/docker-fail2ban)
      - [Caddy](https://caddyserver.com/) as a reverse proxy with https
        - [psm](https://psm.simonj.tech)
        - [goStatic](https://github.com/PierreZ/goStatic)
          - [Hugo](https://gohugo.io/) + [Pulp](https://github.com/koirand/pulp)
      - [SpaceXLaunchBot](https://github.com/r-spacex/SpaceXLaunchBot)

## Setup

```bash
git clone --recurse-submodules https://github.com/psidex/Apollo ~/Apollo && cd ~/Apollo && sudo bash setup
```

The setup script will remove the `~/Apollo` directory after it is run, but will leave
the `update-site` script in `~`. It also installs the `unattended-upgrades` package,
but it must be [set up](https://libre-software.net/ubuntu-automatic-updates/) afterwards
for it to work.

All files used by docker containers are stored in `/etc/dockercontainerfiles`, such as
volumes and config files.

If SSH port is changed, make sure to change it in the fail2ban jail as well.
