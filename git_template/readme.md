# git template
What this template contains?
1. pre-commit hook:  
it supports automatic test(go/python/java/nodejs/deno/...) before `git commit` execution.
2. git commit message template

## 1-Click install
1-Click install all git tools:

    # install global template
    bash ./git_template/init.sh

    # import template to old project
    cp -r ~/.git_template/ .git/

Force install:

    # With `-f` option, it will override old `git_template` and backup it automatically
    bash ./git_template/init.sh -f

For help:

    ./git_template/init.sh -h

## Usage
### Auto code test
This template includes hook for performing automated tests.

Just run:

    $ cd golang_project
    $ git commit
    ....
    go test ./....

## Commit template
Just run:

    $ git commit 
    # Commit messages rule:
    # 
    #     <type>(<scope>): <subject>
    #     <BLANK LINE>
    #     <body>
    #     <BLANK LINE>
    #     <footer>
    #
    # Example 1:
    # ....
