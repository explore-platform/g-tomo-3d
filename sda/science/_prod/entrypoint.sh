printf "\
================================================\n\
BOOT: Science\n\
================================================\n"

# cd science
# uvicorn app:app --host 0.0.0.0 --workers 3 --root-path ${PATH_PREFIX}science

#bash -c "source /venv/science_env/bin/activate science_env && cd science && uvicorn sda_rest:app --host 0.0.0.0 --port 5002 --workers 3 --root-path ${PATH_PREFIX}science" 1>/dev/null &
bash -c "source /venv/science_env/bin/activate science_env && cd science/scripts/ && uvicorn sda_rest:app --host 0.0.0.0 --port 5002 &"
bash -c "source /venv/science_env/bin/activate science_env && cd science/scripts/ && python3 sda_gtomo.py &"
