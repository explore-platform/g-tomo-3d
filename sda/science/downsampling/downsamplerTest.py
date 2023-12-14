import os
from load_cube import load_cube
import numpy as np
import plotly.graph_objects as go
from downsampler import Downsampler
import downsamplerConfig as config
from plotly.subplots import make_subplots
import h5py
def generate_data_2D():
    data = np.arange(1, 101, 1).reshape((10, 10, 1))
    data_generated = dict(
        data = data,
        name = "origin",
        min_axes = [1,1,1],
        max_axes = [10,10,10]
    )

    return data_generated


def generate_data_3D():
    data_list = []
    start = 1
    for i in range(1,11):
        end = start + 100
        d = np.arange(start, end, 1).reshape((10, 10))
        data_list.append(d)
        start = end
    data =  np.hstack(data_list).reshape((10, 10, 10), order='F')
    data_generated =  dict(
        data = data,
        name = "origin",
        min_axes = [1,1,1],
        max_axes = [10,10,10]
    )
    return data_generated

def render(volume_data_list):
    rows = 1
    cols = 1
    specs = [[{"type": "volume"}]]
    if(len(volume_data_list) == 2):
        cols = 2
        specs = [[{"type": "volume"}, {"type": "volume"}]]
    elif(len(volume_data_list) == 3):
        cols = 3
        specs = [[{"type": "volume"}, {"type": "volume"},  {"type": "volume"}]]
    elif(len(volume_data_list) == 4):
        rows = 2
        cols = 2
        specs = [[{"type": "volume"}, {"type": "volume"}],
                 [{"type": "volume"}, {"type": "volume"}]]
    elif (len(volume_data_list) == 5):
        rows = 2
        cols = 3
        specs = [[{"type": "volume"}, {"type": "volume"}, {"type": "volume"}],
                 [{"type": "volume"}, {"type": "volume"}]]
    elif(len(volume_data_list) == 6):
        rows = 2
        cols = 3
        specs = [[{"type": "volume"}, {"type": "volume"}, {"type": "volume"}],
                 [{"type": "volume"}, {"type": "volume"}, {"type": "volume"}]]
    elif(len(volume_data_list) == 7):
        rows = 3
        cols = 3
        specs = [[{"type": "volume"}, {"type": "volume"}, {"type": "volume"}],
                 [{"type": "volume"}, {"type": "volume"}, {"type": "volume"}],
                 [{"type": "volume"}]]
    elif(len(volume_data_list) == 8):
        rows = 3
        cols = 3
        specs = [[{"type": "volume"}, {"type": "volume"}, {"type": "volume"}],
                 [{"type": "volume"}, {"type": "volume"}, {"type": "volume"}],
                 [{"type": "volume"}, {"type": "volume"}]]

    fig = make_subplots(
        rows=rows,
        cols=cols,
        specs=specs
    )

    for row in range(1, rows+1, 1):
        for col in range(1, cols + 1, 1):
            if(len(volume_data_list) == 0):
                break
            volume = volume_data_list.pop(0)
            values = volume['data'].flatten()
            #axes = get_axes(volume["min_axes"], volume["max_axes"], volume["data"].shape)
            min_axes = volume['min_axes']
            max_axes = volume['max_axes']
            if('downsampled_min_axes' in volume):
                min_axes = volume['downsampled_min_axes']
            if('downsampled_max_axes' in volume):
                max_axes = volume['downsampled_max_axes']
            axes = (
                np.linspace(min_axes[0], max_axes[0], volume['data'].shape[0]),
                np.linspace(min_axes[1], max_axes[1], volume['data'].shape[1]),
                np.linspace(min_axes[2], max_axes[2], volume['data'].shape[2])
            )

            print(volume['name'])
            print(axes[0])
            print(axes[1])
            print(axes[2])
            print("------------------------------")

            X, Y, Z = np.meshgrid(axes[0], axes[1], axes[2])
            fig.add_trace(
                go.Volume(
                    name=volume["name"],
                    x=X.flatten(),
                    y=Y.flatten(),
                    z=Z.flatten(),
                    value=values,
                    opacity=0.1,  # needs to be small to see through all surfaces
                    surface_count=21,  # needs to be a large number for good volume rendering
                ),
                row=row, col=col
            )
        if (len(volume_data_list) == 0):
            break

    fig.show()

def get_axes(min, max, data_shape):
    axes = (
        np.linspace(min, max, data_shape[0]),
        np.linspace(min, max, data_shape[1]),
        np.linspace(min, max, data_shape[2])
    )
    return axes

def test_random(export=False):
    generated_data = generate_data_2D()
    hdf5_headers = dict()

    downsampler = Downsampler(hdf5_headers, min_axes = 1, max_axes= 10, export_filename_prefix="random_")



    downsample_rate_list = [config.DOWNSAMPLE_RATE_2X, config.DOWNSAMPLE_RATE_4X]
    downsampled_data_list = []
    for downsample_rate in downsample_rate_list:
        downsampled_data = downsampler.run(generated_data['data'], downsample_rate, export)
        downsampled_data_list.append(downsampled_data)




    render(downsampled_data_list)

def test_random_3d(export=False, render_active=True):
    data_generated = generate_data_3D()
    hdf5_headers = dict()
    axes = get_axes(data_generated['min_axes'], data_generated['min_axes'], data_generated['data'].shape)
    downsampler = Downsampler(hdf5_headers, axes,data_generated['data'].shape, min_axes = data_generated['min_axes'], max_axes= data_generated['max_axes'], export_filename_prefix="3D_")
    if(export == True):
        with h5py.File("3D__origin.h5", "w") as hdf:
            hdf.create_dataset("explore/cube_datas", data=data_generated['data'])

    downsample_rate_list = [config.DOWNSAMPLE_RATE_2X, config.DOWNSAMPLE_RATE_4X, config.DOWNSAMPLE_RATE_8X, config.DOWNSAMPLE_RATE_27X, config.DOWNSAMPLE_RATE_64X]

    #downsample_rate_list = [config.DOWNSAMPLE_RATE_2X, config.DOWNSAMPLE_RATE_8X]
    #downsample_rate_list = [config.DOWNSAMPLE_RATE_27X, config.DOWNSAMPLE_RATE_64X]

    downsampled_data_list = [data_generated]
    for downsample_rate in downsample_rate_list:
        downsampled_data = downsampler.run(data_generated['data'], downsample_rate, export)
        downsampled_data_list.append(downsampled_data)

    #render([data_generated])
    if(render_active == True):
        render(downsampled_data_list)

def test_rendom_hdf5():

    hdf5file = os.path.join('', "explore_cube_density_errors_050pc_v1.h5")
    global headers, cube, axes, min_axes, max_axes, step, hw, points, s, data
    headers, cube, axes, min_axes, max_axes, step, hw, points, s = load_cube(hdf5file)
    data = np.array(cube)

    hdf5_headers = dict()

    downsampler = Downsampler(headers,  axes, data.shape, min_axes = min_axes, max_axes= max_axes, export_filename_prefix="hdf5_3D_")
    #downsampled_data_10X = downsampler.run(data_generated["data"], config.DOWNSAMPLE_RATE_10X)
    #downsampler.export_as_hdf5();

    downsampled_data_2X = downsampler.run(data, config.DOWNSAMPLE_RATE_2X)
    downsampled_data_4X = downsampler.run(data, config.DOWNSAMPLE_RATE_4X)
    downsampled_data_6X = downsampler.run(data, config.DOWNSAMPLE_RATE_6X)
    #downsampler.export_as_hdf5();
    render([downsampled_data_2X, downsampled_data_4X, downsampled_data_6X])

def render1(cube, axes):
    values = cube.flatten()
    X,Y,Z=np.meshgrid(axes[0],axes[1],axes[2])
    caps_on = False

    fig = go.Figure(data=go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=values,
        opacity=0.1,  # needs to be small to see through all surfaces
        surface_count=21,  # needs to be a large number for good volume rendering
    ))
    fig.show()

def run_test_with_generated_data(data_type= "3D", export = False, render_active = True):
    data = generate_data_3D()
    if(data_type == "2D"):
        data = generate_data_2D()
    headers = dict()

    downsampler = Downsampler(headers, min_axes=data["min_axes"], max_axes=data["max_axes"], export_filename_prefix="generated_data_")
    downsampled_data_origin = downsampler.run(data["data"], config.DOWNSAMPLE_RATE_ORIGIN, export)
    downsampled_data_2X = downsampler.run(data["data"], config.DOWNSAMPLE_RATE_2X, export)
    downsampled_data_4X = downsampler.run(data["data"], config.DOWNSAMPLE_RATE_4X, export)
    #downsampled_data_6X = downsampler.run(data["data"], config.DOWNSAMPLE_RATE_6X, export)


    if(render_active == True):
        render([data, downsampled_data_2X, downsampled_data_4X])
def run_test_with_hdf5_file(file_path, export = False, render_active = True):
    hdf5file = os.path.join('', file_path)
    global headers, cube, axes, min_axes, max_axes, step, hw, points, s, data
    headers, cube, axes, min_axes, max_axes, step, hw, points, s = load_cube(hdf5file)
    data = np.array(cube)
    file_base = os.path.basename(file_path)
    file_name = os.path.splitext(file_base)[0] + "_"


    downsampler = Downsampler(headers, axes, data.shape, min_axes=min_axes, max_axes=max_axes, export_filename_prefix=file_name)
    downsample_rate_list = config.get_downsampling_rates([125,216,343,512,1000])
    downsampled_data_list = []
    for downsample_rate in downsample_rate_list:
        downsampled_data = downsampler.run(data, downsample_rate, export)
        downsampled_data_list.append(downsampled_data)


    if(render_active == True):
        render(downsampled_data_list)
        #render([downsampled_data_4X, downsampled_data_8X, downsampled_data_12X, downsampled_data_16X])


if __name__ == '__main__':
    #test_random();
    #test_random_3d(export=True, render_active=True);


    #'''
    file_path= "explore_cube_density_values_025pc_v1.h5"
    run_test_with_hdf5_file(file_path = file_path, export=True, render_active =False);
    #'''