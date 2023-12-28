name=go1.21.5.linux-amd64.tar.gz
wget https://go.dev/dl/$name
rm -rf /usr/local/go && tar -C /usr/local -xzf $name
