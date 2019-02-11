# Install everything needed from apt
sudo apt update
sudo apt upgrade -y
sudo apt install nginx fail2ban software-properties-common -y

# Install certbot
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
sudo ufw enable

# Lock root login for security
sudo passwd -l root

# Move service files to correct locations
sudo cp -R services/fail2ban/. /etc/fail2ban/.
sudo cp -R services/nginx/. /etc/nginx/sites-available/.

# Link nginx sites to be enabled
sudo ln -s /etc/nginx/sites-available/selfhosted-webserver /etc/nginx/sites-enabled

# Restart fail2ban so it uses new config
sudo systemctl restart fail2ban

# Reload nginx configs
sudo service nginx reload

echo ""
echo "General setup done"
echo "Double check now that the NGINX config is working for HTTP"
# TODO: Why does this read get ignored? (only happens if certbot is after)
read -p "Press enter to run certbot setup for NGINX"
sudo certbot --nginx

curl -L https://agent.digitalocean.com/install.sh | sudo bash

echo "- - - Done - - -"
