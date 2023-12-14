import numpy as np
import os
import downsamplerConfig as config
import h5py
import datetime
import sys
from load_cube import load_cube
import time

class Downsampler:
    def __init__(self, hdf5_headers, axes, origin_shape, min_axes = [1,1,1], max_axes = [10,10,10], base_export_path = config.EXPORT_BASE_PATH, export_filename_prefix = config.EXPORT_FILENMAME_PREFIX):
      self.base_export_path = base_export_path
      self.export_filename_prefix = export_filename_prefix
      self.axes = axes
      self.origin_shape = origin_shape
      self.min_axes = min_axes
      self.max_axes = max_axes
      self.downsample_rate = None
      self.downsampled_data = None
      self.downsample_min_axes = None
      self.downample_max_axes = None
      self.hdf5_headers = hdf5_headers.copy()

      self.downsample_method = None


    def set_data(self, downsample_data, downsample_rate):
        self.downsampled_data = downsample_data,
        self.downsample_rate = downsample_rate

    def run(self, data, downsample_rate, export=False, downsample_method = config.DOWNSAMPLE_METHOD['AVERAGE']):
        self.downsample_method = downsample_method
        if(downsample_method == config.DOWNSAMPLE_METHOD['AVERAGE']):
            self.downsample_rate = downsample_rate
            self._avg_based_downsampling(data, downsample_rate)
        if(export == True):
            self.export_as_hdf5()

        return self.get_data()#self.downsampled_data

    def _get_export_filename_path(self, base_path=None, file_name=None):

        if (self.downsample_rate == None):
            return None

        current_base_path = self.base_export_path
        if (base_path != None):
            current_base_path = base_path

        current_file_name = self.downsample_rate["export_file_name"]
        if (file_name != None):
            current_file_name == file_name

        if (len(self.export_filename_prefix) > 0):
            current_file_name = self.export_filename_prefix + "_" + current_file_name + ".h5"
        current_file_name = os.path.join(current_base_path, current_file_name)

        return current_file_name

    def export_as_hdf5(self, base_path=None, file_name = None):
        if(self.downsample_rate == None and self.downsampled_data == None):
            return
        export_file_name = self._get_export_filename_path(base_path, file_name)
        if(export_file_name == None):
            return
        with h5py.File(export_file_name, "w") as hdf:
            final = hdf.create_dataset("explore/cube_datas", data=self.downsampled_data)
            headers = self._get_headers()
            for attr_key in headers:
                final.attrs[attr_key] = headers[attr_key]

    def _get_headers(self):
        x_axes = self.get_downsample_axes("x")
        y_axes = self.get_downsample_axes("y")
        z_axes = self.get_downsample_axes("z")
        hdf5_headers = self.hdf5_headers.copy()

        hdf5_headers["creation_date"] =  datetime.datetime.now().strftime(config.DATE_FORMAT)
        hdf5_headers["is_downsampled"] = True
        hdf5_headers["downsample_rate_x"] = self.downsample_rate["x"]
        hdf5_headers["downsample_rate_y"] = self.downsample_rate["y"]
        hdf5_headers["downsample_rate_z"] = self.downsample_rate["z"]
        hdf5_headers["downsample_method"] = self.downsample_method
        hdf5_headers["downsampled_min_axes"] = [x_axes[0], y_axes[0], z_axes[0]]
        hdf5_headers["downsampled_max_axes"] = [x_axes[1], y_axes[1], z_axes[1]]
        return hdf5_headers


    def export_as_csv(self, base_path=None, file_name = None):
        export_file_name = self._get_export_filename_path(base_path, file_name)
        if(export_file_name == None):
            return

    def get_downsample_axes(self, axis):
        axis_index = 0
        if(axis == "y"):
            axis_index = 1
        elif(axis == "z"):
            axis_index = 2
        if(self.downsample_rate[axis] == 1):
            return [self.min_axes[axis_index], self.max_axes[axis_index]]

        min_value = 0
        max_value = 0

        curr_axes =  np.linspace(self.min_axes[axis_index], self.max_axes[axis_index], self.origin_shape[axis_index])
        #curr_axes = []
        axes_size = self.downsampled_data.shape[axis_index] * self.downsample_rate[axis]
        for i in range(0, self.downsample_rate[axis]):
            min_value = min_value + curr_axes[i] #self.axes[axis_index][i]
        for i in range(axes_size - self.downsample_rate[axis], axes_size):
            max_value = max_value + curr_axes[i] #self.axes[axis_index][i]

        min_value = min_value / self.downsample_rate[axis]
        max_value = max_value / self.downsample_rate[axis]

        return [min_value, max_value]

    def get_data(self):

        x_axes = self.get_downsample_axes("x")
        y_axes = self.get_downsample_axes("y")
        z_axes = self.get_downsample_axes("z")
        return dict(
            downsample_rate= self.downsample_rate,
            name = self.downsample_rate["export_file_name"],
            data= self.downsampled_data,
            min_axes= self.min_axes,
            max_axes = self.max_axes,
            downsampled_min_axes = [x_axes[0], y_axes[0], z_axes[0]],
            downsampled_max_axes=[x_axes[1], y_axes[1], z_axes[1]]
        )

    def _avg_based_downsampling(self, data, downsample_rate):
        self.downsampled_data = None
        original_width, original_height, original_depth = data.shape
        new_width = int(original_width / downsample_rate['x'])
        new_height = int(original_height / downsample_rate['y'])
        new_depth = int(original_depth / downsample_rate['z'])

        self.downsampled_data = np.zeros(shape=(new_width, new_height, new_depth))

        for z in range(new_depth):
            for x in range(new_width):
                for y in range(new_height):
                    downsampled_value = 0
                    for xx in range(downsample_rate['x']):
                        for yy in range(downsample_rate['y']):
                            for zz in range(downsample_rate['z']):
                                downsampled_value += data[x * downsample_rate['x'] + xx, y * downsample_rate['y'] + yy, z * downsample_rate['z'] + zz]
                    self.downsampled_data[x, y, z] = downsampled_value / (downsample_rate['x'] * downsample_rate['y'] * downsample_rate['z'])


def get_arguments(arguments):
    parsed_arguments = dict(
        hdfile="",
        downsample_rate_list = []
    )
    arguments = sys.argv
    if (len(arguments) < 3):
        print("Please provide the HDFile and the downsampling rate as arguments")

        return None
    if (isinstance(arguments[1], str) == False):
        print("Please provide the argument HDFile as a string")
        return None
    if(os.path.exists(arguments[1]) == False):
        print("Provided path as an argument for HDFile does not exist: " + arguments[1])
        return None
    parsed_arguments['hdfile'] = arguments[1]
    for i in range(2, len(arguments)):
        downsample_rate = config.get_or_create_downsampling_rate(int(arguments[i]))
        parsed_arguments['downsample_rate_list'].append(downsample_rate)

    return parsed_arguments

if __name__ == "__main__":
    arguments = get_arguments(sys.argv)
    if arguments != None:
        file_path = arguments['hdfile']
        downsample_rate_list = arguments['downsample_rate_list']
        hdf5file = os.path.join('', file_path)
        global headers, cube, axes, min_axes, max_axes, step, hw, points, s, data
        headers, cube, axes, min_axes, max_axes, step, hw, points, s = load_cube(hdf5file)
        data = np.array(cube)
        file_base = os.path.basename(file_path)
        file_name = os.path.splitext(file_base)[0] + "_"
        downsampler = Downsampler(headers, axes, data.shape, min_axes=min_axes, max_axes=max_axes, export_filename_prefix=file_name)

        print("Downsampling is running .... ")
        start = time.time()
        for downsample_rate in downsample_rate_list:
            downsampler.run(data, downsample_rate, True)
            print("  Exported: " + file_name + downsample_rate["export_file_name"] + ".h5")

        end = time.time()
        print("Downsampling is finished, required time: " + str(end - start) + "seconds")