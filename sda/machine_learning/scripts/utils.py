from __future__ import print_function
from scipy.interpolate import interp1d
import sys
import numpy as np
import h5py

def load_h5_file(path):
    with h5py.File(path, "r") as h5:
        ds = h5['explore']['cube_datas']
        arr = ds[()]
    return arr

def normlized_datacube(cube):
    return (cube - cube.min()) / (cube.max() - cube.min())


def delete_close_verts_dynamic_2d(verts, n_std=1):
    xs, ys = verts[:, 0], verts[:, 1]
    # get an outer matrix of euclidian distances
    dist_mat = np.sqrt(np.power(np.subtract.outer(xs, xs), 2) + np.power(np.subtract.outer(ys, ys), 2))
    threshold = dist_mat.mean() - n_std * dist_mat.std()
    inds = np.array(np.where(dist_mat < threshold))  # apply threshold
    # check where indices are not (i,i), and sort+unique to remove duplicate entries: (i,j) <-> (j,i)
    delete_indices = np.unique(np.sort(inds[:, np.where(inds[0] != inds[1])[0]], axis=0), axis=1)[0]
    return np.delete(verts, delete_indices, axis=0)


def smooth_cluster_boundries(verts, upscale):
    x = verts[:, 0]
    y = verts[:, 1]
    orig_len = len(x)

    x = np.concatenate((x[-2:], x, x[:2]))
    y = np.concatenate((y[-2:], y, y[:2]))

    t = np.arange(len(x))
    ti = np.linspace(1, orig_len + 1, upscale * orig_len)
    xi = interp1d(t, x, kind='quadratic')(ti)
    yi = interp1d(t, y, kind='quadratic')(ti)
    return np.vstack((xi, yi)).T


def delete_close_verts_dynamic_3D(verts, n_std=1):
    xs, ys = verts[:, 0], verts[:, 1], verts[:, 2]
    # get an outer matrix of euclidian distances
    dist_mat = np.sqrt(
        np.power(np.subtract.outer(xs, xs), 2) +
        np.power(np.subtract.outer(ys, ys), 2) +
        np.power(np.subtract.outer(ys, ys), 2)
    )

    threshold = dist_mat.mean() - n_std * dist_mat.std()
    inds = np.array(np.where(dist_mat < threshold))  # apply threshold
    # check where indices are not (i,i), and sort+unique to remove duplicate entries: (i,j) <-> (j,i)
    delete_indices = np.unique(np.sort(inds[:, np.where(inds[0] != inds[1])[0]], axis=0), axis=1)[0]
    return np.delete(verts, delete_indices, axis=0)


