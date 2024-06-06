# etcd gateway
> https://etcd.io/docs/v3.1/op-guide/grpc_proxy/

1. etcd gateway：
etcd gateway 是一个简单的 TCP 代理，它将所有的请求转发到 etcd 集群的一个成员。它不会解析请求，也不会缓存任何数据。它的主要用途是提供一个单一的访问点，使客户端不需要知道所有 etcd 集群成员的地址。

2. etcd grpc-proxy：
etcd grpc-proxy 是一个更复杂的反向代理，它可以解析 gRPC 请求，并对一些请求进行缓存。
    1. 它可以缓存 key 的读取请求，以减少对 etcd 集群的读取压力。
    2. gRPC 代理支持多个 etcd 服务器端点。当代理启动时，它会随机选择一个 etcd 服务器端点来使用。此终结点为所有请求提供服务，直到代理检测到终结点故障

3. etcd --proxy：
这是 etcd 的旧版代理模式，已在 etcd v3.5 中被弃用 https://etcd.io/docs/v2.3/proxy/
支持两种代理模式： readwrite 和 readonly .默认模式是 readwrite