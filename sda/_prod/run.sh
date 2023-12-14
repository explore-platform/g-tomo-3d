printf "\
=======================================================\n\n\
[PROD] SDA DEMONSTRATOR STARTUP\n\n\
=======================================================\n\n"

service nginx start

/usr/bin/mongod --config /etc/mongod.conf & 
sleep 2
arangod --server.endpoint tcp://0.0.0.0:8529 & # --database.directory standalone 
sleep 2

bash ./machine_learning/_prod/entrypoint.sh &
bash ./science/_prod/entrypoint.sh &
bash ./visualiser/_prod/entrypoint.sh &

tail -f /dev/null


