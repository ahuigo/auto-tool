# cluster health
etcdctl --endpoints=$ENDPOINTS endpoint health
etcdctl --endpoints=$ENDPOINTS member list

# 怎么选举leader
一个选p1 一个选p2

    etcdctl --endpoints=$ENDPOINTS elect one p1

    # another client with the same name blocks
    etcdctl --endpoints=$ENDPOINTS elect one p2

# member manage
## get member ID
export ETCDCTL_API=3
HOST_1=10.240.0.13
HOST_2=10.240.0.14
HOST_3=10.240.0.15
etcdctl --endpoints=${HOST_1}:2379,${HOST_2}:2379,${HOST_3}:2379 member list
etcdctl --endpoints=$ENDPOINTS --endpoints=$endpoints2 member list

## remove the member
MEMBER_ID=278c654c9a6dfd3b
etcdctl --endpoints=${HOST_1}:2379,${HOST_2}:2379,${HOST_3}:2379 \
	member remove ${MEMBER_ID}

## add a new member (node 4)
    export ETCDCTL_API=3
    NAME_1=etcd-node-1
    NAME_2=etcd-node-2
    HOST_1=10.240.0.13
    HOST_2=10.240.0.14

    NAME_4=etcd-node-4
    HOST_4=10.240.0.16 # new member
    etcdctl --endpoints=${HOST_1}:2379,${HOST_2}:2379 \
        member add ${NAME_4} --peer-urls=http://${HOST_4}:2380


## start the new member with --initial-cluster-state existing flag:

    # [WARNING] If the new member starts from the same disk space,
    # make sure to remove the data directory of the old member
    # restart with 'existing' flag
    TOKEN=my-etcd-token-1
    CLUSTER_STATE=existing
    NAME_1=etcd-node-1
    NAME_2=etcd-node-2
    NAME_4=etcd-node-4
    HOST_1=10.240.0.13
    HOST_2=10.240.0.14
    HOST_4=10.240.0.16 # new member
    CLUSTER=${NAME_1}=http://${HOST_1}:2380,${NAME_2}=http://${HOST_2}:2380,${NAME_4}=http://${HOST_4}:2380

    THIS_NAME=${NAME_4}
    THIS_IP=${HOST_4}
    etcd --data-dir=data.etcd --name ${THIS_NAME} \
        --advertise-client-urls http://${THIS_IP}:2379 \
        --initial-advertise-peer-urls http://${THIS_IP}:2380 \
        --listen-client-urls http://${THIS_IP}:2379 \
        --listen-peer-urls http://${THIS_IP}:2380 \
        --initial-cluster ${CLUSTER} \
        --initial-cluster-state ${CLUSTER_STATE} \
        --initial-cluster-token ${TOKEN}

Note:

1. 监听：listen-client-urls 与 listen-peer-urls 指定 etcd 服务器绑定到的本地地址以接受传入连接。要侦听所有接口的端口，请指定 0.0.0.0 为侦听 IP 地址。
    1. listen-client-urls 是用于监听客户端请求的
    2. listen-peer-urls 是用于监听集群内部的节点间通信的。
2. 公告：advertise-client-urls 与 initial-advertise-peer-urls 指定 etcd 客户端或其他 etcd 成员用于联系 etcd 服务器的地址。播发地址必须可从远程计算机访问。不要播发类似 localhost 或 0.0.0.0 用于生产设置的地址，因为这些地址无法从远程计算机访问。
    1. advertise-client-urls 是 etcd 服务向客户端公告的地址(每个etcd node都有自己的client-url地址)
    2. initial-advertise-peer-urls 是 etcd 服务在初始集群配置中向其他节点公告的地址
