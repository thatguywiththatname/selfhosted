# Setting up an Ubuntu 18.04 server

**Before anything, `git clone` this repository to `/opt`**

This guide will install:
 - Required dependencies through apt and pip
 - selfhosted-webserver

## Requirements

Going through these steps will install all of the required dependencies as well
as set up the necessary users, groups, and permissions

 - Make sure the package list is up to date (apt update, upgrade)

 - First of all, install all the necessary pacakges contained in the `aptfile` in
this directory (you may have some already installed)

 - Once these are installed, install pip3 ([?](https://pip.pypa.io/en/stable/installing/)):

```bash
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python3 get-pip.py
$ rm get-pip.py
```

## selfhosted-webserver

Simply execute this script and selfhosted-webserver will setup

`sudo sh setup.sh`

## Setup https for all nginx pages

Vist [Let's Encrypt](https://letsencrypt.org/) and follow their getting started
guide for nginx on ubuntu, it should do everything automatically

Following the guide should install a version of `certbot`, which should
set up something (either a cron job or a systemd timer) to automatically run the
renew command every 12 hours. Check these 2 things to see if one of them have
been set up, if not, set up your own

## UFW / firewall

If you are using ufw (or any other firewall), HTTPS traffic through nginx will
need to be enabled. HTTP will also need to be enabled to allow http -> https
redirections. To enable them for ufw, run these commands:

 - `sudo ufw allow 'Nginx HTTPS'`
 - `sudo ufw allow 'Nginx HTTP'`
