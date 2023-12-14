# Downsampling-Script



## Config file 

The file *downsamplerConfig.py* contains several definitions of downsampling rates. The configuration file can be configured with additional downsampling rates, but the function "get_or_create_downsampling_rate" must be additionally extended for each new configuration. 

## Run dowsampling via the console 
Run the script, where the first argument is the name of the script file that contains the implementation logic for downsampling. 
The second argument is the path to the file ("h5" format) that contains the compressed cube data. The other subsequent arguments are the downsampling rates. 

Example: 
```
python downsampler.py explore_cube_density_values_050pc_v1.h5 2 4 8 16 64 
```

After executing the script, the script reads the cube data, performs downsampling at the specified downsampling rates and exports it to a file in "h5" format. 


## Run downsampling via importing script files
Import following scripts
```
from scripts.load_cube import load_cube
from downsampler import Downsampler
import downsamplerConfig as config
```
Loading the cube data for downsampling from an hdf file containing compressed cube data  
```
hdf5file = os.path.join('', file_path)
global headers, cube, axes, min_axes, max_axes, step, hw, points, s, data
headers, cube, axes, min_axes, max_axes, step, hw, points, s = load_cube(hdf5file)
data = np.array(cube)
```

Define specific downsampling rates to export the downsampled cube data for each downsampling rate to a file in h5 format.  
```
downsample_rate_list = config.get_downsampling_rates([125,216,343,512,1000])
```

Execute following steps for downsampling and export
```
file_base = os.path.basename(file_path)
file_name = os.path.splitext(file_base)[0] + "_"
downsampler = Downsampler(headers, axes, data.shape, min_axes=min_axes, max_axes=max_axes, export_filename_prefix=file_name)

downsampled_data_list = []
for downsample_rate in downsample_rate_list:
    downsampler.run(data, downsample_rate, True)
```

## Downsample and visually compare the result
Use the script "downsamplerTest.py" to downsample cube data with different downsampling rates and compare them visually afterwards. 
