# -*- coding: utf-8 -*-

# future import statements
from __future__ import print_function
from __future__ import division

# version information
__project__ = "EXPLORE"
__author__ = "ACRI-ST"
__modifiers__ = '$Author: N. Cox $'
__date__ = '$Date: 2021-10-12 $'
__version__ = '$Rev: 1.0 $'
__license__ = '$Apache 2.0 $'

import os
from load_cube import load_cube
import numpy as np

def initialise(cubename=None):
    global RENDERABLE_CUBE_DATA_POINTS, basepath, filename
    RENDERABLE_CUBE_DATA_POINTS = 100000
    """ CHANGE 'basepath' TO YOUR LOCAL PATH IN DEV ENVIRONMENT """
    # basepath = "C:/Users/lschober/Documents/Code/visualizers/SDA-GTOMO/_data/app_data"
    """ UNCOMMENT 'basepath' WHEN USING IN PRODUCTION (docker) ENVIRONMENT """
    basepath = os.environ.get('SERVICE_APP_DATA')
    #basepath = "/media/mrauch/data2/data/workspaces/explore/sda/g-tomo_merge/_data/app_data/"

    filename = "explore_cube_density_values_050pc_v1.h5"

    if cubename is None:
        hdf5file = os.path.join(basepath, "explore_cube_density_values_050pc_v1.h5")
        filename = "explore_cube_density_values_050pc_v1.h5"

    if cubename == 'cube1':
        hdf5file = os.path.join(basepath, "explore_cube_density_values_025pc_v1.h5")
        filename = "explore_cube_density_values_025pc_v1.h5"

    if cubename == 'cube2':
        hdf5file = os.path.join(basepath, "explore_cube_density_values_050pc_v1.h5")
        filename = "explore_cube_density_values_050pc_v1.h5"

    hdf5file = os.path.join(basepath, filename) # f"{basepath}/{filename}"
    # lab_data = os.environ.get('LAB_DATA')
    # hdf5file = os.path.join(lab_data, "stilism_cube_2.h5")

    """ path to local hdf5 data cube (testing) """
    # hdf5file = os.path.join("/home/nick/Sandbox/cube/", "stilism_cube_2.h5")

    """ set global variables """
    global headers, cube, axes, min_axes, max_axes, step, hw, points, s
    headers, cube, axes, min_axes, max_axes, step, hw, points, s = load_cube(hdf5file)

    """ read the density and extinction error cubes (one resolution only"""

    # hdf5file_densityerror = os.path.join(os.environ.get('SERVICE_APP_DATA'), "explore_cube_density_errors_050pc_v1.h5")
    # hdf5file_extincterror = os.path.join(os.environ.get('SERVICE_APP_DATA'), "explore_cube_extinct_errors_050pc_v1.h5")

    # hdf5file_densityerror = "/media/mrauch/data2/data/workspaces/explore/sda/g-tomo/_data/app_data/explore_cube_density_errors_050pc_v1.h5"
    # hdf5file_extincterror = "/media/mrauch/data2/data/workspaces/explore/sda/g-tomo/_data/app_data/explore_cube_extinct_errors_050pc_v1.h5"

    #hdf5file_densityerror = "C:/Users/ssingh/Documents/projekte/Explore/SDAs/gtomo/sda-gtomo2/_data/app_data/explore_cube_density_errors_050pc_v1.h5"
    #hdf5file_extincterror = "C:/Users/ssingh/Documents/projekte/Explore/SDAs/gtomo/sda-gtomo2/_data/app_data/explore_cube_extinct_errors_050pc_v1.h5"

    hdf5file_densityerror = f"{basepath}/explore_cube_density_errors_050pc_v1.h5"
    hdf5file_extincterror = f"{basepath}/explore_cube_extinct_errors_050pc_v1.h5"

    global headers_errdens, cube_errdens, axes_errdens, min_axes_errdens, max_axes_errdens, step_errdens, hw_errdens, points_errdens, s_errdens
    headers_errdens, cube_errdens, axes_errdens, min_axes_errdens, max_axes_errdens, step_errdens, hw_errdens, points_errdens, s_errdens = load_cube(
        hdf5file_densityerror)

    global headers_errext, cube_errext, axes_errext, min_axes_errext, max_axes_errext, step_errext, hw_errext, points_errext, s_errext
    headers_errext, cube_errext, axes_errext, min_axes_errext, max_axes_errext, step_errext, hw_errext, points_errext, s_errext = load_cube(
        hdf5file_extincterror)

    print("errdens:", np.nanmax(cube_errdens))
    print("errext:", np.nanmax(cube_errext))
