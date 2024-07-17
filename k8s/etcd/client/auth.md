# role/user
## role
role是角色
### add role
    etcdctl --endpoints=${ENDPOINTS} role add root
    etcdctl --endpoints=${ENDPOINTS} role add role0

    etcdctl role get role0
    etcdctl role del role0 --user=root:1

    etcdctl role list

## user
### add user
默认root 用户被赋予了所有的角色，因此它具有所有的权限

    etcdctl --endpoints=${ENDPOINTS} user add root
    etcdctl user add user0
    etcdctl user get user0
    etcdctl user passwd user0

list user

    etcdctl user list

### modify user's role
    $ etcdctl user grant-role user0 role0
    $ etcdctl user revoke-role user0 role0
    $ etcdctl user grant-role root root

# auth
## open auth
当 etcd 的认证功能被启用后，客户端需要提供有效的用户名和密码才能访问 etcd 服务

    etcdctl auth enable
    # now all client requests go through auth
    etcdctl auth disable --user=root:12

## change role's permission
可读写 my-key, wildcard key

    etcdctl --user=root:1 role grant-permission role0 readwrite my-key
    etcdctl --user=root:1 role grant-permission role0 readwrite 'web/pg/*'
    etcdctl --user=root:1 role grant-permission role0 readwrite foo --prefix=true

`*`不能用于前缀，它不是通配符

    $ etcdctl --user=root:1 role get role0
    KV Read:
        [foo, fop) (prefix foo) 表示foo foo1.. 到fop 之前的区间
        web/pg/*        不是prefix 匹配
    KV Write:
        [foo, fop) (prefix foo)
        web/pg/*


你可以通过执行 命令来移除 web/pg/user key 的特殊权限设置。

    etcdctl --user=root:1 role revoke-permission role0 'web/pg/user' 
    etcdctl --user=root:1 role revoke-permission role0 'web/pg/*' 
    etcdctl --user=root:1 role revoke-permission role0  foo --prefix=true

### example
多级目录：

    etcdctl --user=root:1 role add role0
    etcdctl --user=root:1 role grant-permission role0 readwrite 'web/pg/' --prefix=true
    etcdctl --user=root:1 user grant-role user0 role0

    etcdctl put web/pg/user 112
    etcdctl put web/pg/passwd 111
    etcdctl put web/redis/user 111
    etcdctl get web --prefix
    etcdctl --write-out="json" get web

