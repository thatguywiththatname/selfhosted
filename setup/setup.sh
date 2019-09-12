#!/usr/bin/env bash

# Install everything needed from apt
sudo apt update
sudo apt upgrade -y
sudo apt install ufw nginx fail2ban lolcat figlet fortune certbot python-certbot-nginx -y

# Setup UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow "Nginx HTTP"
sudo ufw allow "Nginx HTTPS"
# Automate y/n prompt
echo "y" | sudo ufw enable

# Lock root login for security
sudo passwd -l root

# Move service files to correct locations
sudo cp -R services/fail2ban/. /etc/fail2ban/.
sudo cp -R services/nginx/. /etc/nginx/sites-available/.

# Link nginx sites to be enabled
sudo ln -s /etc/nginx/sites-available/simonjenner.me.conf /etc/nginx/sites-enabled

# Restart fail2ban so it sees the new config
sudo systemctl restart fail2ban

# Reload nginx
sudo systemctl restart nginx

# Install DO metrics agent
# https://www.digitalocean.com/docs/monitoring/how-to/install-agent/
curl -sSL https://repos.insights.digitalocean.com/install.sh | sudo bash

cat << EndOfMsg

General setup done
Double check now that the NGINX config is working for HTTP

EndOfMsg

# https://stackoverflow.com/a/15744486
printf "Press enter to run certbot setup for NGINX"
read _

sudo certbot --nginx

echo "Updating MOTD"
# Done after HTTPS setup so it the ssl MOTD part will work

chmod +x motd/*
# Delete old MOTD, move new MOTD files over
sudo rm /etc/update-motd.d/*
sudo cp motd/* /etc/update-motd.d/

echo -e "\n\nForcing MOTD update\n\n"
sudo run-parts /etc/update-motd.d/

echo "- - - Done - - -"
