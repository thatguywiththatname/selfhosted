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

commandsToExecute = [
    # Dump Redis db
    "redis-cli -s /tmp/redis.sock SAVE",
    # Dump bookstack sql db to users home path
    f"mysqldump -u bookstack -p{sqlPassword} bookstack > /home/{username}/bookstack.sql"
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
    f"/home/{username}/bookstack.sql": "bookstack"
}

# Setup
transport = paramiko.Transport((host, port))
transport.connect(username=username, password=password)

# First of all run the commands we need to
ssh = transport.open_session()
ssh.get_pty()
for command in commandsToExecute:
    ssh.exec_command(command)
ssh.close()

# Then connect through sftp
sftp = paramiko.SFTPClient.from_transport(transport)

for remoteDir in backupPaths:
    downloadDirectory(sftp, remoteDir, os.path.join(backupLocalPath, backupPaths[remoteDir]))

for remoteFile in backupFiles:
    sftp.get(remoteFile, os.path.join(backupLocalPath, backupFiles[remoteFile]))

sftp.close()
transport.close()
