#!/bin/bash
# REQUIREMENTS: figlet, lolcat


# MOTD CONFIG

bannerText="$(hostname)"

# Max chars per line for services readout
width=60

# Services to detect
services=("apport" "broken")
serviceNames=("Apport" "Broken")

# END CONFIG


# HOSTNAME - figlet hostname and animate with lolcat
figlet -f slant $bannerText | lolcat -f


# UPTIME - cut into fields split by " " and print the 2nd field onwards
echo "Uptime: $(uptime -p | cut -d " " -f2-)"


# SERVICES STATUS
# Heavily modified from https://reddit.com/r/unixporn/9gbenc/

# Collect is-active statuses
serviceStatus=()
for service in "${services[@]}"
do
    serviceStatus+=($(systemctl is-active "$service"))
done

# Each line begins with 2 spaces
line="  "
lineLen=2

echo  # Newline
echo "Service status:"

for i in ${!serviceStatus[@]}
do
    if [[ "${serviceStatus[$i]}" == "active" ]]; then
        nextStatus="\e[32m● ${serviceNames[$i]}\e[0m "
    else
        nextStatus="\e[31m▲ ${serviceNames[$i]}\e[0m "
    fi

    # Calculate "seen" chars instead of actual chars (escapes take up a lot)
    # 3 is for status symbol + space + trailing space
    nextStatusLen=$((3+${#serviceNames[$i]}))
    
    # If the current line will exceed the max column with then echo the current line
    # and start a new line
    if (( $((lineLen+nextStatusLen)) > $width )); then
        echo -e "$line"
        line="  "
        lineLen=2
    fi

    lineLen=$((lineLen+nextStatusLen))
    line+=$nextStatus
done

# echo anything thats left
echo -e "$line"
