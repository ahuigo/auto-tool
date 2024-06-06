# update
apt-get update -y && apt-get upgrade -y && apt-get dist-upgrade -y
# oh-my-zsh
apt install zsh -y
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
sudo apt install autojump git silversearcher-ag -y
[ -f ~/.profile ] && source ~/.profile
