# -*- coding: utf-8 -*-

# future import statements
from __future__ import print_function
from __future__ import division

# version information
__project__ = "EXPLORE"
__author__  = "ACRI-ST"
__modifiers__ = '$Author: N. Cox $'
__date__ = '$Date: 2021-10-12 $'
__version__ = '$Rev: 1.0 $'
__license__ = '$Apache 2.0 $'

import numpy as np
import h5py



def load_downsampled_cube(hdf5file):
    """Load hdf5, calculate axes values corresponding to data.

    (original authors: N. Leclerc, G. Plum, S. Ferron)

    Args:
        hdf5file (str): full path for HDF5 file.

    Returns:
        dict: headers contains in HDF5 file.
        :func:`np.array`: 3D array which contains the extinction value.
        tuple: (x, y, z) where x,y,z contains array of axes
            corresponding to cube values.
        array: value min for x, y, z axes.
        array: value max for x, y, z axes.
        float: value of gridstep size
        float: value of half-width of the cube
        float: points (neeed??)
        float: value of scale (half-width*gridstep)
        step, hw, points, s

    """
    # read hdf5 file
    with h5py.File(hdf5file, 'r') as hf:
        cube = hf['explore/cube_datas'][:]
        dc = hf['explore/cube_datas']
        headers = {k: v for k, v in dc.attrs.items()}


    min_axes = headers['downsampled_min_axes']
    max_axes = headers['downsampled_max_axes']
    axes = (
        np.linspace(min_axes[0], max_axes[0], cube.shape[0]),
        np.linspace(min_axes[1], max_axes[1], cube.shape[1]),
        np.linspace(min_axes[2], max_axes[2], cube.shape[2])
    )

    step = []
    for axis_index in range(0,3):
        step.append(abs(max_axes[axis_index] - min_axes[axis_index]) / cube.shape[axis_index])

    step = np.array(step)

    hw = (np.copy(cube.shape) - 1) / 2.
    points = (
        np.arange(0, cube.shape[0]),
        np.arange(0, cube.shape[1]),
        np.arange(0, cube.shape[2])
    )
    s = hw * step

    return (headers, cube,
        axes, min_axes, max_axes,
        step, hw, points, s)

