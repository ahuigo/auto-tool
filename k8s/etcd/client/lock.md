#### client 1##############
    # 命令执行完后自动release lock
    etcdctl --endpoints=$ENDPOINTS lock mutex1

    # 命令会执行10s
    etcdctl --endpoints=$ENDPOINTS lock mutex1 -- bash -c 'echo locked; sleep 10'

# ###### client2 #############
    # another client with the same name blocks
    etcdctl --endpoints=$ENDPOINTS lock mutex1