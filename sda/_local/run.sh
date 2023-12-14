printf "\
=======================================================\n\n\
[LOCAL] SDA DEMONSTRATOR STARTUP\n\n\
=======================================================\n\n"

service nginx start

bash ./machine_learning/_local/entrypoint.sh &
bash ./science/_local/entrypoint.sh &
bash ./visualiser/_local/entrypoint.sh