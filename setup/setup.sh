#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# Inspired by netdata installer: /master/packaging/installer/functions.sh#L188
TPUT_RESET="$(tput sgr 0)"
TPUT_YELLOW="$(tput setaf 3)"
TPUT_WHITE="$(tput setaf 7)"
TPUT_BGRED="$(tput setab 1)"
TPUT_BGGREEN="$(tput setab 2)"
TPUT_BOLD="$(tput bold)"
TPUT_DIM="$(tput dim)"

run() {
    location="[${TPUT_DIM}${PWD}${TPUT_RESET}]$ "
    printf "${location}${TPUT_BOLD}${TPUT_YELLOW}"
    printf "$*"
    printf "${TPUT_RESET}\n"

    # Run all arguments - * puts all arguments to this function into a single string
    # Note: only call run on one command, piping and redirection kinda doesen't work
    $*

    # The ? gets the exit status of the command
    ret=$?

	if [ ${ret} -ne 0 ]; then
		# FAILED
        printf "${TPUT_BGRED}${TPUT_WHITE}${TPUT_BOLD} FAILED ${TPUT_RESET} \n\n"
	else
        # OK
		printf "${TPUT_BGGREEN}${TPUT_WHITE}${TPUT_BOLD} OK ${TPUT_RESET} \n\n"
	fi

	return $ret
}
# -----------------------------------------------------------------------------

# Lock root login for security
run sudo passwd -l root

# Install everything needed from apt
run sudo apt update
run sudo apt upgrade -y
run sudo apt install curl ufw nginx fail2ban lolcat figlet fortune certbot python-certbot-nginx -y

# Setup UFW
run sudo ufw default deny incoming
run sudo ufw default allow outgoing
run sudo ufw allow ssh
run sudo ufw allow 80  # HTTP
run sudo ufw allow 443 # HTTPS
# force means it wont prompt for y/n
run sudo ufw --force enable

# Move service files to correct locations
run sudo cp -R services/fail2ban/. /etc/fail2ban/.
run sudo cp -R services/nginx/. /etc/nginx/sites-available/.

# Link nginx sites to be enabled
run sudo ln -s /etc/nginx/sites-available/simonjenner.me.conf /etc/nginx/sites-enabled

# Restart fail2ban so it sees the new config
run sudo systemctl restart fail2ban

# Reload nginx
run sudo systemctl restart nginx

# Install DO metrics agent
# https://www.digitalocean.com/docs/monitoring/how-to/install-agent/
run curl -sSL https://repos.insights.digitalocean.com/install.sh -o do-install.sh
run sudo bash do-install.sh
run rm do-install.sh

cat << EndOfMsg
General setup done
Double check now that the NGINX config is working for HTTP
EndOfMsg

# https://stackoverflow.com/a/15744486
printf "Press enter to run certbot setup for NGINX\n"
read _
run sudo certbot --nginx

# Update MOTD after HTTPS setup so it the ssl part will work
run chmod +x motd/*
# Delete old MOTD, move new MOTD files over
run sudo rm /etc/update-motd.d/*
run sudo cp motd/* /etc/update-motd.d/

# Force MOTD update
run sudo run-parts /etc/update-motd.d/

printf "- - - Done - - -"
