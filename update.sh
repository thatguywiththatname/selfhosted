get_latest_git_release() {
    curl --silent "https://api.github.com/repos/$1/releases/latest" |
        grep '"tag_name":' |
        sed -E 's/.*"([^"]+)".*/\1/'
}

# gotop
RELEASE=$(get_latest_git_release "cjbassi/gotop")
ARCHIVE=gotop_${RELEASE}_linux_amd64.tgz
wget -q --show-progress https://github.com/cjbassi/gotop/releases/download/${RELEASE}/${ARCHIVE}
tar xf ${ARCHIVE}
sudo mv gotop /usr/local/bin
rm ${ARCHIVE}

echo "- - - Done - - -"
