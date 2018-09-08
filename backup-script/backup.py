from datetime import datetime
from userDetails import *
import paramiko
import logging
import stat
import os

logFilePath = "/var/log/selfhosted-sftp-backup.log"
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
            logger.info("Getting {}".format(remotePath))
            sftp.get(remotePath, localPath)

def runCommand(transport, command):
    logger.info("Executing command {}".format(command))
    ssh = transport.open_session()
    ssh.exec_command(command)
    ssh.close()

# Timestamp for this run
timestamp = datetime.today().strftime("%H:%M_%d-%m-%Y")

# Dump Redis db and dump bookstack sql db to users home path
commandsToExecute = [
    "redis-cli -s /tmp/redis.sock SAVE",
    "mysqldump -u bookstack -p{} bookstack > /home/{}/bookstack.sql".format(sqlPassword, username)
]

backupLocalPath = os.path.join("/home", localUsername, "selfhosted-backups", timestamp)
# A dict of remoteDirectoryPath: $backupLocalPath/localDirectoryPath
backupPaths = {
    "/var/log/SLB": "logs/SLB",
    "/var/www/bookstack/public/uploads": "bookstack/public/uploads",
    "/var/www/bookstack/storage/uploads": "bookstack/storage/uploads"
}
# A dict of remoteFilePath: $$backupLocalPath/localFilePath
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
    logger.info("Getting {}".format(remoteDir))
    downloadDirectory(sftp, remoteDir, os.path.join(backupLocalPath, backupPaths[remoteDir]))

for remoteFile in backupFiles:
    logger.info("Getting {}".format(remoteFile))
    localFilePath = os.path.join(backupLocalPath, backupFiles[remoteFile])
    localDirPath = os.path.split(localFilePath)[0]
    os.path.exists(localDirPath) or os.makedirs(localDirPath)
    sftp.get(remoteFile, localFilePath)

sftp.close()
transport.close()
