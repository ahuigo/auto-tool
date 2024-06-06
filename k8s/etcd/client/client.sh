export ETCDCTL_API=3
HOST_1=10.240.0.17
HOST_2=10.240.0.18
HOST_3=10.240.0.19
ENDPOINTS=$HOST_1:2379,$HOST_2:2379,$HOST_3:2379

alias etcdctl="etcdctl --endpoints=$ENDPOINTS --endpoints=$ENDPOINT2 --endpoints=$ENDPOINT2"
alias etcdctl="etcdctl --endpoints=$ENDPOINTS"
etcdctl member list

# etcdctl put 命令在成功返回后，表示数据已经被成功写入到了 etcd 集群的大多数节点。
etcdctl put web1 123
etcdctl put web2 123
etcdctl get web --prefix
etcdctl --write-out="json" get web1
etcdctl -w="json" get web1