# 1. config
## 1.1 from  config
host=
dbname=
port=5432
user=root
passwd=

## 1.2 to  config
tohost=
topasswd=

# 2. dump
pg_dump "postgresql://$user:$passwd@${host}:$port/$dbname" > $dbname.sql
echo "dump $dbname done!"

# 3. import
cat $dbname.sql | psql "postgresql://$user:$topasswd@${tohost}:$port/$dbname"
echo "sync $dbname done!"
