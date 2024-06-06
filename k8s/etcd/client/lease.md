etcdctl --endpoints=$ENDPOINTS lease grant 300
# lease 34058f22d5100922 granted with TTL(300s)

etcdctl --endpoints=$ENDPOINTS put sample value --lease=34058f22d5100922
etcdctl --endpoints=$ENDPOINTS get sample

# 重置续约为300s
etcdctl --endpoints=$ENDPOINTS lease keep-alive 34058f22d5100922

# revoke
etcdctl --endpoints=$ENDPOINTS lease revoke 34058f22d5100922
# or after 300 seconds
etcdctl --endpoints=$ENDPOINTS get sample