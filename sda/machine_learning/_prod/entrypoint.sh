cat <<EOF
================================================\n
BOOT: Machine learning\n
================================================\n
EOF


#TODO: change port numbers to config variables
bash -c "source /venv/machine_learning_env/bin/activate machine_learning_env && gunicorn --bind 0.0.0.0:5001 --chdir machine_learning --workers 3 wsgi:app"