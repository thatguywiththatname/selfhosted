# backup-script

Not designed to be run on the server, this script connects to given ip & port
using sftp and downloads bookstack files, a redis dump, a bookstack sql dump,
and SpaceX-Launch-Bot log files. Designed to be run as a cron task or similar

For this script to work:

 - The SSH user on the server needs to be able to access `/var/lib/redis`, if not add the user to the `redis` group.
 - The requirements in requirements.txt need to be installed through pip3

Before running the script there are several variables that need to be filled out
in `userDetails.py` in order for it to work. The bookstack sql password can be
found in bookstacks `.env` file 

Writes a log to `/home/$localUsername/selfhosted/selfhosted-backup.log`

Stores backups in `/home/$localUsername/selfhosted/selfhosted-backups`

Currently uses this structure:
 - Backup relevant files to a directory which name is a timestamp
 - Scan through the current backups and decide what to do using this:
   - If the timestamp is within the last week, keep it
   - If the timestamp falls on the 1st or the 15th (roughly half way though the
   month), keep it
   - If none of the above are true, delete it and it's contents
