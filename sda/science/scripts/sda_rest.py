# -*- coding: utf-8 -*-

# future import statements
from __future__ import print_function
from __future__ import division

# version information
__project__ = "EXPLORE"
__author__  = "ACRI-ST"
__modifiers__ = '$Author: L. Schober, M. Rauch$'
__date__ = '$Date: 2022, 2023 $'
__version__ = '$Rev: 1.0 $'
__license__ = '$Apache 2.0 $'

import os

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.wsgi import WSGIMiddleware

from pydantic import BaseModel
from typing import Union
import globals

#from dashapp import initialize_dash_app
#sda = initialize_dash_app()

#sda.scripts.config.serve_locally = True
#sda.title = "EXPLORE: G-Tomo"
#sda.config.suppress_callback_exceptions = True

#server = sda.server

from algorithm_handler import AlgorithmHandler

app = FastAPI()
globals.initialise()
#app.mount("/dash/", WSGIMiddleware(server))

class SliceParameters(BaseModel):
    # Slice Configuration Options
    # Optional (currently)
    #ulon: Union[str, None] = None
    #ulat: Union[str, None] = None
    #unlon: Union[str, None] = None
    #unlat: Union[str, None] = None
    #udist: Union[str, None] = None
    #frame: Union[str, None] = None
    
    # Mandatory options
    lon_orig: int
    lat_orig: int
    dist_orig: int
    lon_norm: int
    lat_norm: int

class CubeParameters(BaseModel):
    # Cube Configuration Options
    cube_file: Union[str, None] = "explore_cube_density_values_050pc_v1.h5"
    ra: int
    dec: int
    distance: int 
    cube_distance: int
    
class ExecutionRequest(BaseModel):
    id: str
    parameters: Union[SliceParameters, CubeParameters]

@app.post("/api/process/cube")
async def read_process(request: ExecutionRequest, background_tasks: BackgroundTasks):
    try:
        if request.id == None:
            return { "error": 400, "message": "Invalid ID" }
        else:
            print(f"Got a new process request for '{request.id}': {request.parameters}")
            handler = AlgorithmHandler.create_new_handler(request.id, request.parameters, "cube")
            if handler is None:
                print(f"Handler for task '{request.id}' not created")
                return { "status": 400, "message": f"Task with ID '{request.id}' already running" }
            else:
                background_tasks.add_task(handler.run_algorithm)
                # handler.run_algorithm()
                return { "status": 200, "message": "Submitted new task" }
    except Exception as e:
        print(f"Exception while processing request: {e}")
        return { "error": 400, "message": "Encountered an error processing request, check your headers and/or submitted form data" }
    
@app.post("/api/process/slice")
async def read_process(request: ExecutionRequest, background_tasks: BackgroundTasks):
    try:
        if request.id == None:
            return { "error": 400, "message": "Invalid ID" }
        else:
            print(f"Got a new process request for '{request.id}': {request.parameters}")
            handler = AlgorithmHandler.create_new_handler(request.id, request.parameters, "slice")
            if handler is None:
                print(f"Handler for task '{request.id}' not created")
                return { "status": 400, "message": f"Task with ID '{request.id}' already running" }
            else:
                background_tasks.add_task(handler.run_algorithm)
                # handler.run_algorithm()
                return { "status": 200, "message": "Submitted new task" }
    except Exception as e:
        print(f"Exception while processing request: {e}")
        return { "error": 400, "message": "Encountered an error processing request, check your headers and/or submitted form data" }

@app.get("/")
async def root():
    return {
        "message": "Hello World",
        "status": 200
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5002)
