# Install everything needed from apt
sudo apt update
sudo apt upgrade -y
sudo apt install nginx fail2ban software-properties-common lolcat figlet fortune -y

# Install certbot (software-properties-common needed)
sudo add-apt-repository universe -y
sudo add-apt-repository ppa:certbot/certbot -y
sudo apt-get update
sudo apt-get install certbot python-certbot-nginx -y

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

# Restart fail2ban so it uses new config
sudo systemctl restart fail2ban

# Reload nginx configs
sudo service nginx reload

# Delete old MOTD, move new MOTD files over
sudo rm /etc/update-motd.d/*
sudo cp motd/* /etc/update-motd.d/

echo -e "\n\nForcing MOTD update\n\n"
sudo run-parts /etc/update-motd.d/

# Install DO metrics agent
curl -L https://agent.digitalocean.com/install.sh | sudo bash

cat << EndOfMsg

General setup done
Double check now that the NGINX config is working for HTTP

EndOfMsg

# https://stackoverflow.com/a/15744486
printf "Press enter to run certbot setup for NGINX"
read _

sudo certbot --nginx

echo "- - - Done - - -"
