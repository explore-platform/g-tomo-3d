import os
from flask import Flask, request

from scripts import run_clustering_3d

app = Flask(__name__)

@app.route("/testing", methods=['POST'])
def test():
    path = request.args.get("data_filename") #TODO: change to API names
    if os.path.exists(path):
        return "ok"
    else:
        return "nope"

@app.route("/compute_clusters_2d", methods=['POST'])
def compute_clusters_2d():
    #FIXME: how are the slices passed? as file (h5?)? or as data?
    pass

@app.route("/compute_clusters_3d", methods=['POST'])
def compute_clusters_3d():
    datacube_path = request.args.get("data_filename") #TODO: change to API names
    hp_dict = {
        "points_m": request.args.get("points_m", None),
        "points_threshold": request.args.get("points_threshold", None),
        "min_cluster_size": request.args.get("min_cluster_size", None),
        "min_samples": request.args.get("min_samples", None),
        "cluster_selection_epsilon": request.args.get("cluster_selection_epsilon", None),
        "metric": request.args.get("metric", None),
        "cluster_selection_method": request.args.get("cluster_selection_method", None),
        }
    hp_dict = {k: v for k, v in hp_dict.items() if v is not None}
    clusters_verts = run_clustering_3d(datacube_path, hp_dict)
    clusters_verts = {k: v.tolist() for k, v in clusters_verts.items()}
    return clusters_verts


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)