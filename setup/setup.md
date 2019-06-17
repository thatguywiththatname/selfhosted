# Setup

This code snippet will clone this repo to `~/site` and run the setup script

```bash
git clone https://github.com/psidex/simonjenner.me ~/site && cd ~/site/setup && sudo sh setup.sh
```

This script will:

- `apt` update and upgrade
- Installng various packages this setup depends on
- Install [certbot](https://certbot.eff.org/) for nginx
- Setup UFW for the current config
- Lock the root login so it can't be used anymore
- Setup my NGINX config
- Setup Fail2Ban
- Install Digital Ocean's [Agent](https://github.com/digitalocean/do-agent) for Droplet metrics
- Run certbot for the NGINX config
- Setup custom MOTD message

## Notes

### Redirection

Redirection on [simonjenner.me](https://simonjenner.me) is done through my NGINX config and not through the DNS so that in the future I can quickly switch it over to something different (e.g. A Django server)

### HTTPS

"Certbot comes with a cron job that will renew the HTTPS certificates automatically"

### Changing SSH port

- Open `/etc/ssh/sshd_config`
- Find `# Port 22`, un-comment it and change the number to your desired SSH port
- Make sure to allow the new port in your firewall, e.g. `sudo ufw allow $sshport/tcp`
- Restart the ssh service, `sudo systemctl restart sshd`
- Reconnect and test the new port is working properly
- Deny the default SSH port in your firewall once you confirm the new port is working
- If you have fail2ban setup, change the config to look at the new ssh port

### Install pip

```bash
sudo apt install python3-distutils
curl https://bootstrap.pypa.io/get-pip.py | sudo python3
```
