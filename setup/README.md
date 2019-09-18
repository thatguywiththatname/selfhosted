# Setup

This script assumes you:
- Are running Debian 10 on a Digital Ocean "Droplet"
- Have the `sudo` and `git` packages installed
- Are running it as a normal user that is a member of the `sudo` group

This code snippet will clone this repo to `~/apollo` and run the setup script:

```bash
git clone https://github.com/psidex/simonjenner.me ~/apollo && cd ~/apollo/setup && sudo bash setup
```

This script will:

- Lock the root login so it can't be used anymore
- `apt` update and upgrade
- Install various packages this setup depends on
- Install [certbot](https://certbot.eff.org/) for nginx & run it
- Install & setup UFW for the current config
- Install & Setup Fail2Ban
- Install & Setup NGINX with the config in `services/nginx`
- Install TIC from the [TICK stack](https://www.influxdata.com/time-series-platform/): InfluxDB, Telegraf, and Chronograf (set to run on :8882) - This provides nice monitoring of various metrics and also for [SpaceXLaunchBot](https://github.com/r-spacex/SpaceXLaunchBot)
- Install [do-agent](https://github.com/digitalocean/do-agent) for monitoring
- Setup custom MOTD message

## Next Steps

### Changing SSH port

- Open `/etc/ssh/sshd_config`
- Find `# Port 22`, un-comment it and change the number to your desired SSH port
- Make sure to allow the new port in your firewall, e.g. `sudo ufw allow $sshport/tcp`
- Restart the ssh service, `sudo systemctl restart ssh`
- Reconnect and test the new port is working properly
- Deny the default SSH port in your firewall once you confirm the new port is working
- If you have fail2ban setup, change the config to look at the new ssh port
