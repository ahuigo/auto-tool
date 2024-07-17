name=go1.21.5.linux-amd64.tar.gz
wget https://go.dev/dl/$name
{ rm -rf /usr/local/go && tar -C /usr/local -xzf $name; } || sudo tar -C /usr/local -xzf $name

#sudo apt-get update
#sudo apt-get -y upgrade
cat <<MM >>~/.zshrc
export GOROOT=/usr/local/go 
export GOPATH=$HOME/go
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
MM
