# install etcd

# server
TOKEN=token-01
CLUSTER_STATE=new
NAME_1=machine-1
HOST_1=127.0.0.1 # 只允许127.0.0.1访问
# HOST_1=0.0.0.0 # 允许所有访问
CLUSTER=${NAME_1}=http://${HOST_1}:2380

# For machine 1
THIS_NAME=${NAME_1}
THIS_IP=${HOST_1}
etcd --data-dir=data.etcd --name ${THIS_NAME} \
	--initial-advertise-peer-urls http://${THIS_IP}:2380 --listen-peer-urls http://${THIS_IP}:2380 \
	--advertise-client-urls http://${THIS_IP}:2379 --listen-client-urls http://${THIS_IP}:2379 \
	--initial-cluster ${CLUSTER} \
	--initial-cluster-state ${CLUSTER_STATE} --initial-cluster-token ${TOKEN}



# client
export ETCDCTL_API=3
HOST_1=127.0.0.1
ENDPOINTS=$HOST_1:2379

etcdctl --endpoints=$ENDPOINTS member list