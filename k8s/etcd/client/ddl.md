# databae
## save database
    etcdctl --endpoints=$ENDPOINT snapshot save my_snapshot.db
    etcdctl --endpoints=$ENDPOINT -w json snapshot save my_snapshot.db

    -w, --write-out string   set the output format (fields, json, protobuf, simple, table) (default "simple")
## show database
    etcdutl -w table snapshot status my_snapshot.db
    etcdutl -w json snapshot status my_snapshot.db

Note: etcdutl 是一个辅助工具，主要用于处理 etcd 的底层数据和元数据。它的功能包括：

    管理 etcd 的成员和集群配置
    创建和验证 etcd 数据库的快照
    检查和修复 etcd 数据库
    打印数据库的哈希值
    迁移数据

