# Add selfhosted user and sort out permissions
sudo adduser --system --group --no-create-home selfhosted
sudo chown -R selfhosted:selfhosted /opt/selfhosted

# https://superuser.com/a/91966
sudo chmod -R u+rwX,go+rX,go-w /opt/selfhosted

# Python requirements for selfhosted-dashboard
sudo pip install -r /opt/selfhosted/setup/requirements.txt

# Logging directory (used by uWSGI)
sudo mkdir /var/log/selfhosted
sudo chown -R selfhosted:selfhosted /var/log/selfhosted

# Move service files to correct locations
sudo cp -R -p /opt/selfhosted/services/systemd/. /lib/systemd/system/.
sudo cp -R /opt/selfhosted/services/nginx/. /etc/nginx/sites-available/.
sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/bookstack /etc/nginx/sites-enabled
