---
title: etcd tuning　调校
date: 2024-05-11
private: true
---
# etcd 调优
> refer: https://etcd.io/docs/v3.5/tuning/
## 超时tuning
原则：
- heartbeat interval 心跳间隔时间, 不小于包往返时间
- election timeout 至少是包平均往返时间的10倍
    - 美国和日本之间的时间约为350-400ms。如果网络性能不均匀或有规律的数据包延迟/丢失，则可能需要重试几次才能成功发送数据包。因此，5s 是全球往返时间的安全上限, 10倍是50s为合理最大值

## snapshots　tuning
> etcd appends all key changes to a log file. This log grows forever 
默认情况下，每 10,000 次更改后将创建快照。如果 etcd 的内存使用率和磁盘使用率过高，请尝试通过命令行设置以下内容来降低快照阈值：

    # Command line arguments:
    $ etcd --snapshot-count=5000

    # Environment variables:
    $ ETCD_SNAPSHOT_COUNT=5000 etcd

## disk tuning
etcd 集群对磁盘延迟非常敏感。由于 etcd 必须将建议保留到其日志中，因此来自其他进程的磁盘活动可能会导致长时间 fsync 的延迟。结果是 etcd 可能会错过心跳，导致请求超时和临时 leader 丢失。当给定高磁盘优先级时，etcd 服务器有时可以与这些进程一起稳定运行。

    # best effort, highest nice priority on linux
    $ sudo ionice -c2 -n0 -p `pgrep etcd`

## network tuning
如果 etcd leader 处理大量并发客户端请求，可能会因为网络拥塞而延迟处理后续 Peer 请求。
If the etcd leader serves a large number of concurrent client requests, it may delay processing follower peer requests due to network congestion(拥塞). 
This manifests(表现) as send buffer error messages on the follower nodes:

    dropped MsgProp to 247ae21ff9436b2d since streamMsg's sending buffer is full
    dropped MsgAppResp to 247ae21ff9436b2d since streamMsg's sending buffer is full

These errors may be resolved by prioritizing etcd’s peer traffic over its client traffic. On Linux, peer traffic can be prioritized by using the traffic control mechanism:
这些错误可以通过将 etcd 的对等流量优先于其客户端流量来解决。可以使用 Linux tc（Traffic Control）命令对对等流量进行优先级排序：

    # 在设备 eth0 上添加一个根队列规则，使用优先级队列规则（prio），并设置有3个带宽（bands）。
    tc qdisc add dev eth0 root handle 1: prio bands 3

    # 在设备 eth0 上添加一个过滤器，匹配源端口（sport）为 2380 的 IP 流量，并将其分类到流ID 1:1。(优先级1, 高)
    tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip sport 2380 0xffff flowid 1:1
    # 在设备 eth0 上添加一个过滤器，匹配目标端口（dport）为 2380 的 IP 流量，并将其分类到流ID 1:1。
    tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip dport 2380 0xffff flowid 1:1

    # 类似(优先级2, 次高)
    tc filter add dev eth0 parent 1: protocol ip prio 2 u32 match ip sport 2379 0xffff flowid 1:1
    tc filter add dev eth0 parent 1: protocol ip prio 2 u32 match ip dport 2379 0xffff flowid 1:1

To cancel tc, execute:

    tc qdisc del dev eth0 root

## cpu tuning
在 Linux 上，可以将 CPU 调控器配置为性能模式：

    echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor