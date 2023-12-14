from __future__ import print_function
import sys
import h5py
import numpy as np
from numpy.random import choice
from random import choices, random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import normalize
import hdbscan
from scipy.spatial import ConvexHull
from shapely import geometry
from math import floor, ceil

from machine_learning.scripts.utils import *

def get_hull_vert(points):
    hull = ConvexHull(points)
    return points[hull.vertices]


def generate_point_cloud(density_map, m=1, threshold=0):
    print(f"\n\n=== densitiy map shape: {density_map.shape}===\n\n", file=sys.stderr)
    density_map[density_map < threshold] = 0
    rand_arr = np.random.rand(*density_map.shape) * m
    mask = density_map > rand_arr
    print(f"\n\n=== mask shape: {mask.shape}===\n\n", file=sys.stderr)
    points = np.argwhere(mask)
    return points


def get_clusters_vert_2d(points, labels, upscale=3):
    res = {}
    for label in range(labels.max() + 1):
        cluster_points = points[labels == label]
        vert = get_hull_vert(cluster_points)
        vert = delete_close_verts_dynamic_2d(vert)
        smooth_vert = smooth_cluster_boundries(vert, upscale)
        res[label] = smooth_vert
    return res


def get_clusters_vert_3D(points, labels):
    res = {}
    for label in range(labels.max() + 1):
        cluster_points = points[labels == label]
        try:
            vert = get_hull_vert(cluster_points)
        except:
            print(f"error on label {label}")
            continue
        vert = delete_close_verts_dynamic_3D(vert)
        res[label] = vert
    return res

def run_clustering_3d(datacube_path: str, hp_dict: dict):
    points_m, points_threshold = hp_dict.pop('points_m', 1), hp_dict.pop('points_threshold', 1)
    datacube = load_h5_file(datacube_path)
    norm_cube = normlized_datacube(datacube)
    points = generate_point_cloud(norm_cube, m=points_m, threshold=points_threshold)
    print(f"\n\n========== points shape: {points.shape} ==========\n\n", file=sys.stderr)
    scanner = hdbscan.HDBSCAN(**hp_dict)
    scanner.fit_predict(points)
    vert_dict = get_clusters_vert_3D(points, scanner.labels_)
    return vert_dict



