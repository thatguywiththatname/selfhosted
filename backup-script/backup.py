from datetime import datetime
import paramiko
import stat
import os

# User Defined Variables #######################################################
localUsername = ""  # The username the script will be running under
host = ""
port = 0
username = ""
password = ""
sqlPassword = ""  # The password for the mysql servers bookstack user
################################################################################

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
            sftp.get(remotePath, localPath)

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

# First of all run the commands we need to
ssh = transport.open_session()
# TODO: Make this a bit less dodgy, look into using sshclient(?)
bigCommand = " && ".join(commandsToExecute)
ssh.exec_command(bigCommand)
ssh.close()

# Then connect through sftp
sftp = paramiko.SFTPClient.from_transport(transport)

for remoteDir in backupPaths:
    downloadDirectory(sftp, remoteDir, os.path.join(backupLocalPath, backupPaths[remoteDir]))

for remoteFile in backupFiles:
    localFilePath = os.path.join(backupLocalPath, backupFiles[remoteFile])
    localDirPath = os.path.split(localFilePath)[0]
    os.path.exists(localDirPath) or os.makedirs(localDirPath)
    sftp.get(remoteFile, localFilePath)

sftp.close()
transport.close()
