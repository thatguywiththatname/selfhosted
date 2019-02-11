# selfhosted

My personal server configuration, currently setup to run on [simonjenner.me](https://simonjenner.me)

Redirection is done through NGINX and not through the DNS so that in the future I can
quickly switch it over to something different (e.g. A Django server)

Clone this repo to your home directory (should work anywhere):

```bash
cd ~
git clone https://github.com/thatguywiththatname/selfhosted
```

Then run `setup.sh` and it will (in this order):
- Install [certbot](https://certbot.eff.org/) for nginx
- Setup UFW for the current config
- Lock the root login so it can't be used anymore
- Setup my NGINX config
- Setup Fail2Ban
- Run certbot for NGINX config
- Install Digital Oceans [Agent](https://github.com/digitalocean/do-agent) for Droplet metrics

Once this is done you can delete the selfhosted directory:

```bash
rm -rf ~/selfhosted
```

## HTTPS

"Certbot comes with a cron job that will renew the HTTPS certificates automatically"

## Changing SSH port

- Open `/etc/ssh/sshd_config`
- Find `# Port 22`, un-comment it and change the number to your desired SSH port
- Make sure to allow the new port in your firewall, e.g. `sudo ufw allow $sshport/tcp`
- Restart the ssh service, `sudo systemctl restart sshd`
- Reconnect and test the new port is working properly
- Deny the default SSH port in your firewall once you confirm the new port is working
