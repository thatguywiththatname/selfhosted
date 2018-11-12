# Add selfhosted user + group and sort out permissions
sudo adduser --system --group --no-create-home selfhosted
sudo chown -R selfhosted:selfhosted /opt/selfhosted

# https://superuser.com/a/91966
sudo chmod -R u+rwX,go+rX,go-w /opt/selfhosted

# Python requirements for selfhosted-webserver
sudo pip3 install -r /opt/selfhosted/setup/requirements.txt

# Logging directory (used by uWSGI)
sudo mkdir /var/log/selfhosted
sudo chown -R selfhosted:selfhosted /var/log/selfhosted

# Move service files to correct locations
sudo cp -R /opt/selfhosted/setup/services/fail2ban/. /etc/fail2ban/.
sudo cp -R /opt/selfhosted/setup/services/systemd/. /lib/systemd/system/.
sudo cp -R /opt/selfhosted/setup/services/nginx/. /etc/nginx/sites-available/.

# Link nginx sites to be enabled
sudo ln -s /etc/nginx/sites-available/selfhosted-webserver /etc/nginx/sites-enabled

# Start services
sudo systemctl daemon-reload
sudo systemctl enable selfhosted-webserver
sudo systemctl start selfhosted-webserver
sudo systemctl restart nginx
