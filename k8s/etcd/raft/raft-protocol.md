---
title: Raft protocol 协议
date: 2024-05-11
private: true
---
# leader election.
> http://www.kailing.pub/raft/index.html
## node 状态
节点有几个状态:
- `term:1` 初始态
- candidate候选人(`vote count:1`) 初始态等待election timeout 会进入到candidate
    - 如果在election timeout 时间内没有收到大多数投票，就会开始新的选举
- voter投票人(`vote for B`) 初始态收到B的投票请求的话，就会投票给B变成`vote for B`（并且reset election timeout）
    - voter　先收到B的投票请求，然后又收到 C的投票请求，就又会变成`vote for C`(Note: 同意后要过一个超时时间，才能同意下一个)
- leader领导: `vote count` 超过半数后，就会变成leader，就会向voter/follower 发送 `Append Entries`(heartbeat time间隔)
- follower: voter(`vote for C`)或follower，收到`Append Entries`消息，就会变成 follower. 
    - 超过election timeout 一直没有收到C的`Append Entries`　请求的话，这个节点会变成candidate.
## 选举参数
- election timeout 选举超时: 指followers跟随者成为candidates候选者之前所等待的时间
    1. election timeout被随机分配在150毫秒至300毫秒之间。
- heartbeat interval 心跳间隔: 
  - 如果跟随者在心跳超时时间内没有收到领导者的心跳消息: 那么它会认为领导者已经失效，然后转变为候选者（candidate）状态，开始新的领导者选举
  - 领导者（leader）多次没有收到某个跟随者（follower）的响应，并且失去了半数followers。就不能服务了

## 选举过程election
1. followers 等待各自的election timeout
2. follower 选举超时后，跟随者成为候选者 candidate: 为自己投票`term:1`，开始新的election term选举任期; 并且向其它两个folloers 发送 Request Vote 请求投票消息
3. 如果接收节点在这个学期中还没有投票: 
   1. receiver 将投票给候选人B(`Vote For B`), 同时reset election timeout 
   2. candidate 收到获得多数vote票，便成为领导者leader
        1. leader开始向其追随者发送Append Entries追加条目消息
            1. 这些消息以heartbeat interval心跳超时指定的时间间隔发送
            2. 跟随者然后响应每个Append Entries 追加条目消息。
            3. 此选举任期将持续到: 追随者停止接收心跳并成为候选人为止. 进入第二轮选举`term:2`
4. 有两个candidates(split vote 分裂选举)发生:
    1. 由于两个candidates 都收不到多半的投票
    2. 经过一个election timeout　后，发起下一轮投票`term:term+1`

## Log replication
> Once we have a leader elected we need to replicate all changes to our system to all nodes.
> This is done by using the same `Append Entries message` that was used for `heartbeat`.

过程：
1. client 向leader 发送change: set 5/ put a 5 等指令
2. leader 收到记录change log: Change log is sent to follower on next heartbeat
3. follower收到 change log, 并响应
4. leader 收到半数follower 响应后，真正执行change(An entry is committed once majority of followers acknowlege it): 并且通过follower commit
5. follower: commit change log
5. 


# endpoints不一样会发生什么
## etcdctl  endpoints 不一样
> 如果有的etcdctl 使用的etcd-0.etcd:2379...etcd-5.etcd:2379 有的etcdctl 使用的etcd-0.etcd:2379...etcd-10.etcd:2379
### 导致数据不一致
如果你有两个不同的 etcdctl 客户端，一个连接到 etcd-0 到 etcd-5，另一个连接到 etcd-0 到 etcd-10，那么这两个客户端将看到不同的数据视图。

- 对于连接到 etcd-0 到 etcd-5 的客户端，它只能看到这些节点上的数据。如果有数据在 etcd-6 到 etcd-10 上，这个客户端将无法看到。

- 对于连接到 etcd-0 到 etcd-10 的客户端，它可以看到所有节点上的数据。

这可能会导致数据不一致的问题。例如，如果一个客户端在 etcd-6 到 etcd-10 上写入了数据，那么只连接到 etcd-0 到 etcd-5 的客户端将无法看到这些数据。

### endpoints 不一样会产生两个不同的leader吗？
不会，集群的领导者（leader）是由集群内部的 Raft 协议选举产生的，与客户端连接的节点无关。

## etcd server的endpoints不一样 
> http://www.kailing.pub/raft/index.html
可能数据不一致, 可能产生分区
- 如果leader收不到过半数ack消息，就无法commit log(uncommitted entries)
- 直接分区恢复后, 发现更高级别的term 的leader，就会roll bak uncommitted entries
- 如果不同的服务器连接到不同的 endpoints，可能会导致数据可见性的问题。例如，如果一个服务器只连接到部分节点，并在这些节点上写入数据，那么只连接到其他节点的服务器可能无法看到这些数据

# 读取数据
## 读取模式
etcd提供了两种读取模式来满足不同的需求：

- 线性一致性读取（Linearizable reads）：这种读取模式会从leader节点读取数据，确保读取到的数据是最新的。
- 序列一致性读取（Serializable reads）：这种读取模式可以从任何节点读取数据，可能读取到的数据不是最新的，但是可以提高读取性能。