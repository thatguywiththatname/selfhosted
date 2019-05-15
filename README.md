# simonjenner.me

My personal website and server configuration, currently powering [simonjenner.me](https://simonjenner.me) and [SpaceX-Launch-Bot](https://github.com/r-spacex/SpaceX-Launch-Bot)

Redirection on [simonjenner.me](https://simonjenner.me) is done through my NGINX config and not through the DNS so that in the future I can quickly switch it over to something different (e.g. A Django server)

## Installation

```bash
cd ~
git clone https://github.com/psidex/simonjenner.me
cd simonjenner.me
sudo sh setup.sh
```

This script will:

- Update and upgrade through `apt`
- Install [certbot](https://certbot.eff.org/) for nginx
- Setup UFW for the current config
- Lock the root login so it can't be used anymore
- Setup Fail2Ban
- Setup my NGINX config
- Setup custom MOTD message
- Install Digital Ocean's [Agent](https://github.com/digitalocean/do-agent) for Droplet metrics
- Run certbot for the NGINX config

Once this is done you can delete the simonjenner.me directory:

```bash
rm -rf ~/simonjenner.me
```

## Notes

### HTTPS

"Certbot comes with a cron job that will renew the HTTPS certificates automatically"

### Changing SSH port

- Open `/etc/ssh/sshd_config`
- Find `# Port 22`, un-comment it and change the number to your desired SSH port
- Make sure to allow the new port in your firewall, e.g. `sudo ufw allow $sshport/tcp`
- Restart the ssh service, `sudo systemctl restart sshd`
- Reconnect and test the new port is working properly
- Deny the default SSH port in your firewall once you confirm the new port is working
