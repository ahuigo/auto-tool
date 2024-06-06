# useradd
add alex
    
    username=alex
    sudo useradd -m $username
    sudo usermod -aG sudo $username
    sudo passwd $username
    sudo update-alternatives --set editor /usr/bin/vim.basic
    echo 'alex ALL=(ALL:ALL) NOPASSWD: ALL'

