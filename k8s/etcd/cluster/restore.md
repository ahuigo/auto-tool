# 踩坑记
- etcd数据损坏的处理：https://blog.itdo.top/archives/etcd%E6%95%B0%E6%8D%AE%E6%8D%9F%E5%9D%8F%E6%82%B2%E5%82%AC%E5%A4%84%E7%90%86%E8%BF%87%E7%A8%8B%E8%AE%B0%E5%BD%95
- 恢复：https://www.cnblogs.com/WeiyiGeek/p/17192341.html#0x01-%E7%8E%AF%E5%A2%83%E5%87%86%E5%A4%87

# backup
> https://etcd.io/docs/v3.1/op-guide/recovery/

    ETCDCTL_API=3 etcdctl --endpoints $ENDPOINT snapshot save snapshot.db

# import 
## import data to m1
```bash
    ETCDCTL_API=3 etcdctl snapshot restore snapshot.db \
    --name m1 \
    --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
    --initial-cluster-token etcd-cluster-1 \
    --initial-advertise-peer-urls http://host1:2380
```

## start etcd with the new data directories:

```bash
    $ etcd \
    --name m1 \
    --listen-client-urls http://host1:2379 \
    --advertise-client-urls http://host1:2379 \
    --listen-peer-urls http://host1:2380 &
```