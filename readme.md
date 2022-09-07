# Dev Tools

本仓库包括一些效率开发工具

1. `git_template`:
   - auto code test for go/nodejs/python/java
   - git commit template
2. azure devops tools
   - mo-import-helm.py auto import helm to current project(You should execute
     `$cd project` first)
3. ssl:
   - gen-ssl.py : ssl certificate generate
4. string 工具
    - str/unescape.py

所有的工具使用默认的yaml 配置文件 `~/.mo.yaml`.

    touch <<MM > $HOME/.mo.yaml
    helm:
        # 指定helm chart path
        chart_path: ~/hdmap/hdmap-helm-charts
        # 本地运行时：把短域名替换成长域名
        mojito:7900:
            dev: tos.dev.hdmap-inner.momenta.works
            staging: tos.staging.hdmap-inner.momenta.works
            prod: tos.hdmap-inner.momenta.works
    MM
