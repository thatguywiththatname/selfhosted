# selfhosted

My personal server configuration, currently setup to run on `simonjenner.me`

Redirection is done through NGINX and not through the DNS so that in the future I can
quickly switch it over to something different (e.g. A Django server)

Clone this repo to `/opt` and then run `setup.sh` and it will:
- Lock the root login so it can't be used anymore
- Setup my NGINX config
- Setup Fail2Ban
- Setup UFW for the current config
- Walk you through setting up HTTPS for my NGINX config

## Digital Ocean

If running on a Digital Ocean Droplet, install DigitalOcean Agent for better metrics:

`curl -L https://agent.digitalocean.com/install.sh | sudo bash`

## HTTPS

Certbot comes with a cron job that will renew the HTTPS certificates automatically

## Changing SSH port

- Open `/etc/ssh/sshd_config`
- Find "# Port 22", un-comment it and change the number to your desired SSH port
- Make sure to allow the new port in your firewall, e.g. `sudo ufw allow $sshport/tcp`
- Restart the ssh service, `sudo systemctl restart sshd`
- Reconnect and test the new port is working properly
- Deny the default SSH port in your firewall once you confirm the new port is working
