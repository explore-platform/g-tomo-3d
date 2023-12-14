printf "\
================================================\n\
BOOT: Machine learning\n\
================================================\n"
# export FLASK_APP=/sda/machine_learning/app.py
# flask run --port 5001 --host=0.0.0.0

export FLASK_ENV=development
# python /sda/machine_learning/app.py

bash -c "source /venv/machine_learning_env/bin/activate machine_learning_env && python /sda/machine_learning/app.py"