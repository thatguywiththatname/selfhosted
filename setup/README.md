# Setting up an Ubuntu 18.04 server

**Before anything, `git clone` this repository to `/opt`**

This guide will install:
 - Required dependencies through apt and pip
 - selfhosted-webserver
 - BookStack

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

## BookStack

Go [here](https://www.bookstackapp.com/docs/admin/installation/#ubuntu-1804) and
follow the installation instructions

Once this is done, we want to remove apache2 and replcae it with nginx. To do
this, run these commands:

 - `sudo apt remove apache2 --purge`
 - `sudo apt autoremove`
 - `sudo apt remove apache2.*`

This should completely nuke apache from your system

BookStacks nginx file(s) will be created when `setup.sh` is run later

## selfhosted-webserver

Simply execute this script and selfhosted-webserver will setup

`sudo sh setup.sh`

## Setup https for all nginx pages

Vist [Let's Encrypt](https://letsencrypt.org/) and follow their getting started
guide for nginx on ubuntu, it should do everything automatically

Now the https certificate(s) need to be automatically renewed, to do this create
a cron task to run `certbot renew` (or `certbot-auto renew`, depending on what
you installed) every day at a random time

## UFW / firewall

If you are using ufw (or any other firewall), https traffic through nginx will
need to be enabled. To enable it for ufw, run this command:

`sudo ufw allow 'Nginx HTTPS'`
