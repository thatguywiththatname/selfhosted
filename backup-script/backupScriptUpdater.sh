# Just update this directory after it has been moved to /home/simon

cd /home/simon

# Copy our details out
cp backup-script/userDetails.py userDetails.py
rm -rf backup-script

# Clone and move backup stuff
mkdir temp
cd temp
git clone https://github.com/thatguywiththatname/selfhosted.git
cp -r selfhosted/backup-script /home/simon
cd ..
rm -rf temp

# Copy our details back in
cp userDetails.py backup-script/userDetails.py
rm userDetails.py
