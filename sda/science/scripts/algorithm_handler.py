from __future__ import annotations

import tab3d
from cube_cut import cube_cut
from load_cube import load_cube

import globals

import os
from time import sleep
import requests
import json

from astropy.coordinates.sky_coordinate import SkyCoord
from pydantic import BaseModel
from typing import Union, Dict
import pandas as pd
import numpy as np

class CubeParameters(BaseModel):
    # Cube Configuration Options
    cube_file: str
    ra: int
    dec: int
    distance: int 
    cube_distance: int
    overwrite: bool = False
    
class SliceParameters(BaseModel):
    # Slice Configuration Options
    # Optional (currently)
    ulon: Union[str, None] = None
    ulat: Union[str, None] = None
    unlon: Union[str, None] = None
    unlat: Union[str, None] = None
    udist: Union[str, None] = None 
    frame: Union[str, None] = None
    
    # Mandatory options
    long_orig: int
    lat_orig: int
    dist_orig: int
    lon_norm: int
    lat_norm: int
    overwrite: Union[bool, None]
    
class AlgorithmHandler:
    VIS_API_STATUS_UPDATER_URL = f"http://{os.getenv('VISUALIZER_HOST')}:{os.getenv('VISUALIZER_PORT')}/algoapi/executionStatus"
    VIS_API_RECIEVER_URL = f"http://{os.getenv('VISUALIZER_HOST')}:{os.getenv('VISUALIZER_PORT')}/algoapi/submitExecutionResult"
    VIS_DATA_API_RECIEVER_URL = f"http://{os.getenv('VISUALIZER_HOST')}:{os.getenv('VISUALIZER_PORT')}/dataapi/addData"
    #VIS_DATA_API_RECIEVER_URL = f"http://localhost:20000/dataapi/addData"
    #VIS_API_STATUS_UPDATER_URL = f"http://localhost:20000/algoapi/executionStatus"
    #VIS_API_RECIEVER_URL = f"http://localhost:20000/algoapi/submitExecutionResult"
    #VIS_DATA_API_RECIEVER_URL = f"http://host.docker.internal:20000/dataapi/addData"
    #VIS_API_STATUS_UPDATER_URL = f"http://host.docker.internal:20000/algoapi/executionStatus"
    #VIS_API_RECIEVER_URL = f"http://host.docker.internal:20000/algoapi/submitExecutionResult"
    
    algorithm_tasks = {}

    @staticmethod
    def create_new_handler(id: str, parameters: CubeParameters | SliceParameters, execType: str):
        task_id = id
        
        print(f"Creating new handler for task ({execType}) '{task_id}': {parameters}")
        handler = AlgorithmHandler(execType, task_id, parameters)

        #if task_id in AlgorithmHandler.algorithm_tasks:
        #    print(f"Task id '{task_id}' already exists")
        #    AlgorithmHandler.submit_result(task_id, { "stage": 3, "stages": 4, "text": "failed" }, [])
        #    return None
        #else:
        AlgorithmHandler.algorithm_tasks[task_id] = handler
        print(f"Handler for task '{task_id}' created")
        AlgorithmHandler.submit_status(task_id, "running", { "stage": 1, "stages": 4, "status": "Starting" })
        # handler.run_algorithm()
        return handler

    @staticmethod
    def get_handlers() -> Dict[str, AlgorithmHandler]:
        return AlgorithmHandler.algorithm_tasks
    
    @staticmethod
    def get_handler(task_id: str):
        if task_id not in AlgorithmHandler.algorithm_tasks:
            raise Exception(f"Task with id {task_id} does not exist")
        handler = AlgorithmHandler.get_handlers()[task_id]

        return handler
    
    @staticmethod
    def remove_handler(task_id):
        if task_id not in AlgorithmHandler.algorithm_tasks:
            print(f"Task with id {task_id} does not exist")
        else:
            AlgorithmHandler.algorithm_tasks.pop(task_id)
            print(f"Removed handler for task '{task_id}'")
            
    @staticmethod
    def create_dataset(dataframe) -> dict:
        """
        Creates a visualizer-friendly dataset from a pandas dataframe
        """
        col = ""
        v = ""
        try:
            dataset = {}
            for index, column in enumerate(dataframe.columns):
                content = []
                col = column
                for val in dataframe[column].tolist():
                    v = val
                    try:
                        # Try to convert from numpy dtype
                        content.append(val.item())
                    except:
                        # If it fails, append as string
                        new_val = str(val)
                        if new_val.lower() == "nan":
                            new_val = ""

                        content.append(new_val)

                dataset[f"{index}"] = json.dumps({
                    "fieldname": str(column),
                    "data": content
                })
            return dataset
        except Exception as e:
            print(f"Error converting data points:\nColumn: '{col}' With Type '{type(col)}'\nAt Value '{v}': With Type '{type(v)}'\n", e)
            return []

    @staticmethod
    def submit_result(task_id: str, status: any, datasetIds: list) -> None:
        try:
            status_data = { 'taskId': task_id, 'status': status, 'datasetIds': datasetIds }
            requests.post(AlgorithmHandler.VIS_API_RECIEVER_URL, json=status_data)
        except Exception as e:
            raise(e)
    
    @staticmethod
    def submit_status(task_id: str, status: str, details: any):
        try:
            status_data = { 'taskId': task_id, 'status': status, 'details': details }
            requests.post(AlgorithmHandler.VIS_API_STATUS_UPDATER_URL, json=status_data)
        except Exception as e:
            raise(e)
    
    def __init__(self, execType: str, id: str, parameters: SliceParameters | CubeParameters):
        self.execType = "cube" if execType == None else execType
        self.task_id = id

        if (execType == "cube"):
            self.cube_file = parameters.cube_file if parameters.cube_file != None else globals.filename
            self.ra = parameters.ra
            self.dec = parameters.dec
            self.distance = parameters.distance
            self.cube_distance = parameters.cube_distance
        else:
            self.ulon = self.ulat = self.unlon = self.unlat = 'deg'
            self.udist = 'pc'
            self.frame = 'galactic'
            
            self.lon_orig = parameters.lon_orig
            self.lat_orig = parameters.lat_orig
            self.dist_orig = parameters.dist_orig
            self.lon_norm = parameters.lon_norm
            self.lat_norm = parameters.lat_norm

        print(f"Handler for task '{self.task_id}' initialized")
        
    def upload_result_data(self, id: str, result: dict) -> None:
        print(f"[TASK:{self.task_id}]: Uploading result data '{id}'")
        try:
            requests.post(AlgorithmHandler.VIS_DATA_API_RECIEVER_URL, headers={ 'x-dataset-id': id, 'x-update': 'true', 'x-task-id': self.task_id }, json=result)
        except Exception as e:
            raise(e)

    def generate_cube(self):
        visdata = []
        sc = SkyCoord(
            self.ra,
            self.dec,
            distance=self.distance,
            unit=('deg', 'deg', 'pc'),
            frame='galactic'
        )

        mid_point = sc.represent_as('cartesian').get_xyz().value
        distance_cube = tab3d.correct_cube_distance_per_axis(mid_point, self.cube_distance)
        
        AlgorithmHandler.submit_status(self.task_id, "processing", { "stage": 2, "stages": 4, "status": "Getting sampling rate", "progress": 1 / 4, "step": 2, "totalSteps": 4 })
        downsampling_rate = tab3d.get_suitable_downsampling(mid_point, distance_cube)
        
        AlgorithmHandler.submit_status(self.task_id, "processing", { "stage": 2, "stages": 4, "status": "Calculating cube data", "progress": 1 / 4, "step": 3, "totalSteps": 4 })
        if (downsampling_rate > 1):
            # Load downsampled cube

            file_name_base = os.path.splitext(os.path.basename(self.cube_file))[0]
            downsampled_file_name = file_name_base + "__" + str(downsampling_rate) + "X.h5"
            #hdf5file = os.path.join(globals.basepath + "/" + file_name_base + "/" + downsampled_file_name)
            hdf5file = os.path.join(globals.basepath, file_name_base, downsampled_file_name)
            headers, cube, axes, min_axes, max_axes, step, hw, points, s = tab3d.load_downsampled_cube(hdf5file)
        else:
            # Load non-downsampled cube

            hdf5file = os.path.join(globals.basepath, self.cube_file)
            headers, cube, axes, min_axes, max_axes, step, hw, points, s = load_cube(hdf5file)
            
        pos_x, pos_y, pos_z = tab3d.get_sub_cube_positons(axes, mid_point, distance_cube)
        sub_cube = cube[pos_x[0]:pos_x[1] + 1, pos_y[0]:pos_y[1] + 1, pos_z[0]:pos_z[1] + 1]
        sub_axes = [axes[0][pos_x[0]:pos_x[1] + 1], axes[1][pos_y[0]:pos_y[1] + 1], axes[2][pos_z[0]:pos_z[1] + 1]]
        visdata = tab3d.calculate3DData(sub_cube, sub_axes, True)
        
        # sleep(200)
        return visdata

    def generate_slice(self):
        AlgorithmHandler.submit_status(self.task_id, "processing", { "stage": 2, "stages": 4, "status": "Calculating slice", "progress": 1 / 4, "step": 2, "totalSteps": 4 })
        result, X, Y, Z = cube_cut(globals.cube, globals.hw, globals.step, globals.points, globals.s, 
                           self.lon_orig, self.ulon, self.lat_orig, self.ulat, self.frame, self.dist_orig, 
                           self.udist, self.lon_norm, self.unlon, self.lat_norm, self.unlat)
        
        AlgorithmHandler.submit_status(self.task_id, "processing", { "stage": 2, "stages": 4, "status": "Converting results", "progress": 1 / 4, "step": 3, "totalSteps": 4 })

        reformatted = []
        for xi in range(len(X)):
            for yi in range(len(Y)):
                reformatted.append([X[xi], Y[yi], Z[yi][xi]])
        
        data = pd.DataFrame(data=np.asarray(reformatted), columns=["x", "y", "value"])
        # sleep(200)
        return data

    def run_algorithm(self) -> None:
        try:
            print(f"Running for task '{self.task_id}': {self.execType}")
            
            """ Algo Start """
            AlgorithmHandler.submit_status(self.task_id, "processing", { "stage": 2, "stages": 4, "status": "Starting", "progress": 1 / 4, "step": 1, "totalSteps": 4 })
            # sleep(200)
            
            if (self.execType == "cube"):
                cube_data = self.generate_cube()
                results = { "cube_data.csv": cube_data }
            else:
                slice_data = self.generate_slice()
                results = { "slice_data.csv": slice_data }
            
            AlgorithmHandler.submit_status(self.task_id, "processing", { "stage": 2, "stages": 4, "status": "Preparing results for upload", "progress": 1 / 4, "step": 4, "totalSteps": 4 })
            # sleep(200)
            """ Algo End """

            print(f"Finished for task '{self.task_id}' | Converting results and submitting to Data API")
            # sleep(200)
            AlgorithmHandler.submit_status(self.task_id, "uploading", { "stage": 3, "stages": 4, "status": "Starting Upload", "progress": 0, "step": 0, "totalSteps": len(results) })
            # sleep(200)
            
            datasets = []
            step = 100 / 100 / len(results)
            for index, result_name in enumerate(results.keys()): 
                datasets.append(result_name)
                AlgorithmHandler.submit_status(self.task_id, "uploading", { "stage": 3, "stages": 4, "status": f"Uploading {result_name}", "progress": (index+1)*step, "step": index+1, "totalSteps": len(results) })

                dataset = AlgorithmHandler.create_dataset(results[result_name])
                self.upload_result_data(result_name, dataset)
            AlgorithmHandler.submit_result(self.task_id, { "stage": 4, "stages": 4, "text": "finished" }, datasets)
            AlgorithmHandler.remove_handler(self.task_id)
            return
        except Exception as e:
            print(f"Error running algorithm for task '{self.task_id}': {e}")
            AlgorithmHandler.submit_result(self.task_id, { "stage": 4, "stages": 4, "text": "failed" }, [])
            AlgorithmHandler.remove_handler(self.task_id)
            return