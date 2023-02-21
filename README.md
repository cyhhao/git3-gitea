# build

TAGS="bindata sqlite sqlite_unlock_notify" make build

# run

./gitea

# debug

TAGS="bindata sqlite sqlite_unlock_notify" make watch
