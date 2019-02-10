# Install everything needed from apt
sudo apt update
sudo apt upgrade -y
sudo apt install nginx fail2ban sendmail ufw -y

# Install certbot
sudo apt-get install software-properties-common -y
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install certbot python-certbot-nginx -y

# Setup UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
# Only allows HTTPS, not HTTP
sudo ufw allow "Nginx HTTPS"
sudo ufw enable

# Move service files to correct locations
sudo cp -R /opt/selfhosted/services/fail2ban/. /etc/fail2ban/.
sudo cp -R /opt/selfhosted/services/nginx/. /etc/nginx/sites-available/.

# Link nginx sites to be enabled
sudo ln -s /etc/nginx/sites-available/selfhosted-webserver /etc/nginx/sites-enabled

# Reload configs, enable everything and (re)start fail2ban
sudo systemctl daemon-reload
sudo systemctl enable fail2ban
sudo systemctl enable nginx
sudo systemctl restart fail2ban

echo ""
echo "General setup done"
echo "Now running certbot setup for NGINX"
read -p "Press enter to continue"
sudo certbot --nginx

# (re)start NGINX now certbot has done its thing
sudo systemctl restart nginx

echo "- - - Done - - -"
