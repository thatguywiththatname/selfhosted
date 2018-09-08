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

# Dump Redis db and dump bookstack sql db to users home path
commandsToExecute = [
    "redis-cli -s /tmp/redis.sock SAVE",
    "mysqldump -u bookstack -p{} bookstack > /home/{}/bookstack.sql".format(sqlPassword, username)
]

backupLocalPath = os.path.join("/home", localUsername, "selfhosted-backups")
# A dict of remoteDirectoryPath: $backupLocalPath/localDirectoryPath
backupPaths = {
    "/var/log/SLB": "logs/SLB",
    "/var/www/bookstack/public/uploads": "bookstack/public/uploads",
    "/var/www/bookstack/storage/uploads": "bookstack/storage/uploads"
}
# A dict of remoteFilePath: $$backupLocalPath/localFilePath
backupFiles = {
    "/var/lib/redis/dump.rdb": "redis",
    "/var/www/bookstack/.env": "bookstack",
    "/home/{}/bookstack.sql".format(username): "bookstack"
}

# Setup
transport = paramiko.Transport((host, port))
transport.connect(username=username, password=password)

# First of all run the commands we need to
ssh = transport.open_session()
bigCommand = " && ".join(commandsToExecute)  # TODO: Make this a bit nicer, look into using sshclient(?)
ssh.exec_command(bigCommand)
ssh.close()

# Then connect through sftp
sftp = paramiko.SFTPClient.from_transport(transport)

for remoteDir in backupPaths:
    downloadDirectory(sftp, remoteDir, os.path.join(backupLocalPath, backupPaths[remoteDir]))

for remoteFile in backupFiles:
    localPath = os.path.join(backupLocalPath, backupFiles[remoteFile])
    os.path.exists(localPath) or os.makedirs(localPath)
    sftp.get(remoteFile, localPath)

sftp.close()
transport.close()
