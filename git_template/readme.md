# git tools

## install this git tools

## Global hooks template
What hooks this templatedir provides?
1. pre-commit hook:  it supports automatic test(go/python/java/nodejs/deno/...) before `git commit` execution.

### 1. Set global templatedir
Set git's global templatedir

    bash ./git_template/init.sh

With `-f` option, it will override old `git_template`

    # force
    bash ./git_template/init.sh -f

You can also import this template manully as following:

    mkdir ~/.git_template
    cp -r `pwd`/git_template/ ~/.git_template

### 2. Init new project
By default, if you init a new project, your previously configured `~/.git_template` would  be automatically copied to  **new-project/.git**.

    git clone https://github.com/user/demo new-project

So, you don't have to do any extra configuration. 

### 3. Old project
If your old project doesn't have hooks, you should copy global `~/.git_template/` to old project manully like this:

    cd old_git_project
    cp -r ~/.git_template/ .git/


## Commit template
Set commit template globally:
    
    git config --global commit.template '~/.git_template/gitmessage

