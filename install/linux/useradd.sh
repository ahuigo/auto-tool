# useradd
add alex
    
    username=alex
    sudo useradd -m $username
    sudo usermod -aG sudo $username
    sudo usermod -aG root $username
    sudo usermod -aG docker $username
    sudo passwd $username
    sudo update-alternatives --set editor /usr/bin/vim.basic
    echo 'alex ALL=(ALL:ALL) NOPASSWD: ALL'

change zsh

    chsh -s $(which zsh)

## remove user
> deluser 来自debian 更友好。userdel 更标准基础
remove user from a group

    sudo deluser alex sudo
    # or
    sudo gpasswd -d alex sudo

remove user and home

    sudo userdel -r alex

## remove group
    deluser --group <GROUP>
