# etcdctl 
etcdctl is etcdclient 

    alias etcdctl="etcdctl --endpoints=$ENDPOINTS"
    etcdctl put web/pg/user pg_user 
    etcdctl put web/pg/passwd pg_123
    etcdctl put web/redis/user redis_user 
    etcdctl get web --prefix
    etcdctl --write-out="json" get web


# delete
etcdctl del web --prefix

    --prefix[=false]: delete keys with matching prefix
    --prev-kv[=false]: return deleted key-value pairs
    --from-key[=false]: delete keys that are greater than or equal to the given key using byte compare
    --range[=false]: delete range of keys without delay

# transaction

    etcdctl --endpoints=$ENDPOINTS put user1 bad
    etcdctl txn --interactive

    compares:
    value("user1") = "bad"

    success requests (get, put, delete):
    del user1

    failure requests (get, put, delete):
    put user1 good