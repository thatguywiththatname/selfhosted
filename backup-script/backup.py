from userDetails import *
import datetime
import paramiko
import logging
import shutil
import stat
import os

logFilePath = os.path.join("/home", localUsername, "selfhosted-backup.log")
handler = logging.FileHandler(filename=logFilePath, encoding="UTF-8", mode="a")
handler.setFormatter(logging.Formatter("%(asctime)s : %(levelname)s : %(message)s"))
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger(__name__)

def downloadDirectory(sftp, remoteDir, localDir):
    """
    sftp.get doesen't support download whole directories, so use this
    """
    os.path.exists(localDir) or os.makedirs(localDir)
    dir_items = sftp.listdir_attr(remoteDir)
    for item in dir_items:
        remotePath = os.path.join(remoteDir, item.filename)
        localPath = os.path.join(localDir, item.filename)
        if stat.S_ISDIR(item.st_mode):
            downloadDirectory(sftp, remotePath, localPath)
        else:
            logger.info("Downloading {}".format(remotePath))
            sftp.get(remotePath, localPath)

def runCommand(transport, command):
    logger.info("Executing command {}".format(command))
    ssh = transport.open_session()
    ssh.exec_command(command)
    ssh.close()

# Timestamp for this run
timestamp = datetime.datetime.today().strftime("%H:%M:%S@%d-%m-%Y")
logger.info("Starting backup, using timestamp: {}".format(timestamp))

# Dump Redis db and dump bookstack sql db to users home path
commandsToExecute = [
    "redis-cli -s /tmp/redis.sock SAVE",
    "mysqldump -u bookstack -p{} bookstack > /home/{}/bookstack.sql".format(sqlPassword, username)
]

backupDirectory = os.path.join("/home", localUsername, "selfhosted-backups")
currentBackupPath = os.path.join(backupDirectory, timestamp)
# A dict of remoteDirectoryPath: $currentBackupPath/localDirectoryPath
backupPaths = {
    "/var/log/SLB": "logs/SLB",
    "/var/log/selfhosted": "logs/selfhosted",
    "/var/www/bookstack/public/uploads": "bookstack/public/uploads",
    "/var/www/bookstack/storage/uploads": "bookstack/storage/uploads"
}
# A dict of remoteFilePath: $currentBackupPath/localFilePath
backupFiles = {
    "/var/lib/redis/dump.rdb": "redis/dump.rdb",
    "/var/www/bookstack/.env": "bookstack/.env",
    "/home/{}/bookstack.sql".format(username): "bookstack/bookstack.sql"
}

# Setup
transport = paramiko.Transport((host, port))
transport.connect(username=username, password=password)

# Run the commands we need to through SSH
for command in commandsToExecute:
    runCommand(transport, command)

# Then connect through sftp
sftp = paramiko.SFTPClient.from_transport(transport)

for remoteDir in backupPaths:
    downloadDirectory(sftp, remoteDir, os.path.join(currentBackupPath, backupPaths[remoteDir]))

for remoteFile in backupFiles:
    logger.info("Downloading {}".format(remoteFile))
    localFilePath = os.path.join(currentBackupPath, backupFiles[remoteFile])
    localDirPath = os.path.split(localFilePath)[0]
    os.path.exists(localDirPath) or os.makedirs(localDirPath)
    sftp.get(remoteFile, localFilePath)

sftp.close()
transport.close()

logger.info("Finished downloading backup")
logger.info("Analysing backup directory")

now = datetime.datetime.now()
backups = [d for d in os.listdir(backupDirectory) if os.path.isdir(os.path.join(backupDirectory, d))]
for backup in backups:
    # dd/mm/yyyy
    date = backup.split("@")[1]
    day, month, year = [int(i) for i in date.split("-")]
    if day == 1 or day == 15:
        # Falls on a 1st or a 15th so don't do anything
        pass
    else:
        backupDate = datetime.date(day=day, month=month, year=year)
        backupDate = datetime.datetime.combine(backupDate, datetime.datetime.min.time())
        if (now - backupDate).days > 7:
            # Directory is older than a week
            logger.info("Removing backup {}".format(backup))
            shutil.rmtree(os.path.join(backupDirectory, backup))

logger.info("Finished")
