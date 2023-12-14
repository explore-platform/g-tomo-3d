from fastapi import FastAPI
import os
import json
#from scripts.science import get_data

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Hello World",
        "status": 200
        # Test that the VENV still has access to the host envs
        #"path_prefix": os.environ.get('PATH_PREFIX')
    }
#@app.get("/data", status_code=200)
#async def data_get():
#    data = get_data()
#    return {
#        "count": len(data),
#        "value": json.loads(data)
#    }