printf "\
================================================\n\
BOOT: Science\n\
================================================\n"

bash -c "source /venv/science_env/bin/activate science_env && cd science && uvicorn app:app --reload --host 0.0.0.0 --root-path /sda/science/"
# uvicorn app:app --reload --host 0.0.0.0 --root-path /sda/science/