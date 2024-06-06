# watch key
etcdctl watch $KEY [$END_KEY]


    -i, --interactive[=false]: interactive mode
    --prefix[=false]: watch on a prefix if prefix is set
    --rev=0: Revision to start watching
    --prev-kv[=false]: get the previous key-value pair before the event happens
    --progress-notify[=false]: get periodic watch progress notification from server


# list watcher