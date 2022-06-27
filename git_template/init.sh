#!/usr/bin/env zsh
####################### shell type ####################
getShellType(){
    if [[ -n $BASH_VERSION ]] || [[ -n $BASH_SOURCE ]]; then
        echo bash
    elif [[ -n $ZSH_VERSION ]]; then
        echo zsh
    fi
}
SHELL_TYPE=`getShellType`
isZsh(){
    if [[ $SHELL_TYPE = 'zsh' ]]; then
        return 0
    else
        return 1
    fi
}
isBash(){
    if [[ $SHELL_TYPE = 'bash' ]]; then
        return 0
    else
        return 1
    fi
}
####################### script  path ####################
if isZsh; then
    CWD=$(dirname ${0:a})
elif isBash; then
    CWD=$(dirname ${BASH_SOURCE[0]})
    CWD=$(cd $CWD;pwd)
else
    echo "This script only support zsh and bash!!"
    return 1
fi
if ! ls $CWD/init.sh >/dev/null;then
    exit 1
fi

####################### link script####################
RED='\033[0;31m'
NC='\033[0m' # No Color
if test "$1" = '-f' && test -d $HOME/.git_template ;then
    echo mv ~/.git_template ~/.git_template.bak
    mv ~/.git_template ~/.git_template.bak
fi
if ! { [[ -L $HOME/.git_template ]] || [[ -d $HOME/.git_template ]];};then
    if ! [[ -d $HOME/.git_template ]];then
        #ln -s $CWD ~/.git_template
        mkdir ~/.git_template
        cp -r $CWD/ ~/.git_template
    fi
    git config --global init.templatedir '~/.git_template'
    git config --global commit.template '~/.git_template/gitmessage'

    printf "Installed ${RED}~/.git_template/${NC} successfully.\n"
else
    printf "You've installed ${RED}~/.git_template${NC} before.\n"
    printf "You could run `init.sh -f` to override old template(auto backup)\n"
fi

