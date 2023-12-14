printf "\
================================================\n\
BOOT: Visualiser\n\
================================================\n"

#sleep 10
#STATUS="$(systemctl is-active mongodb.service)"
#if [ "${STATUS}" = "active" ]; then
#    echo "mongodb available"
#else 
#    echo "mongodb not available "  
#fi
#sleep 5

cd /visualizer
# NODE Visualiser
#node app.js &
npm run start &
# PYTHON Visualiser
# bash -c "source /venv/visualiser_env/bin/activate visualiser_env && python /visualizer/app/wizard/app.py" 1>/dev/null &
# bash -c "source /venv/visualiser_env/bin/activate && cd /visualizer/ && python app/wizard/app.py" 1>/dev/null &
#working:
#bash -c "source /venv/visualiser_env/bin/activate && cd /visualizer/ && python ./app/wizard/app.py" 1>/dev/null &  


# TEST
# bash -c "source /venv/visualiser_env/bin/activate && cd /sda/visualiser/test && /venv/visualiser_env/bin/python3 app.py" 1>/dev/null &
# bash -c "source /venv/visualiser_env/bin/activate && cd /sda/visualiser/test && python app.py" 1>/dev/null &

# BIAS DETECTION
# bash -c "source /venv/biasdetection_env/bin/activate && cd /biasdetection && uvicorn server:app --host 0.0.0.0 --workers 3 --root-path ${PATH_PREFIX}science" 1>/dev/null &
#working:
#bash -c "source /venv/biasdetection_env/bin/activate && cd /biasdetection && uvicorn server:app --host 0.0.0.0 --port 5004" 1>/dev/null &
