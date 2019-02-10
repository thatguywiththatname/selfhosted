# selfhosted

My personal server configuration, currently setup to run on `simonjenner.me`

Redirection is done through NGINX and not through the DNS so that in the future I can
quickly switch it over to something different (e.g. A Django server)

Run `setup.sh` and it will:
- Setup my NGINX config
- Setup Fail2Ban
- Setup UFW for the current config
- Walk you through setting up HTTPS for my NGINX config

## HTTPS

Certbot comes with a cron job that will renew the HTTPS certificates automatically
