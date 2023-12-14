DOWNSAMPLE_RATE_ORIGIN = dict(
    x = 1,
    y = 1,
    z = 1,
    export_file_name = "origin"
)


DOWNSAMPLE_RATE_2X = dict(
    x = 2,
    y = 1,
    z = 1,
    export_file_name = "2X"
)

DOWNSAMPLE_RATE_4X = dict(
    x = 2,
    y = 2,
    z = 1,
    export_file_name = "4X"
)

DOWNSAMPLE_RATE_8X = dict(
    x = 2,
    y = 2,
    z = 2,
    export_file_name = "8X"
)

DOWNSAMPLE_RATE_27X = dict(
    x = 3,
    y = 3,
    z = 3,
    export_file_name = "27X"
)

DOWNSAMPLE_RATE_64X = dict(
    x = 4,
    y = 4,
    z = 4,
    export_file_name = "64X"
)


DOWNSAMPLE_RATE_125X = dict(
    x = 5,
    y = 5,
    z = 5,
    export_file_name = "125X"
)

DOWNSAMPLE_RATE_216X = dict(
    x = 6,
    y = 6,
    z = 6,
    export_file_name = "216X"
)


DOWNSAMPLE_RATE_343X = dict(
    x = 7,
    y = 7,
    z = 7,
    export_file_name = "343X"
)

DOWNSAMPLE_RATE_512X = dict(
    x = 8,
    y = 8,
    z = 8,
    export_file_name = "512X"
)

DOWNSAMPLE_RATE_1000X = dict(
    x = 10,
    y = 10,
    z = 10,
    export_file_name = "1000X"
)

'''

DOWNSAMPLE_RATE_10X = dict(
    x = 10,
    y = 10,
    z = 4,
    export_file_name = "10X"
)


DOWNSAMPLE_RATE_12X = dict(
    x = 12,
    y = 12,
    z = 12,
    export_file_name = "12X"
)

DOWNSAMPLE_RATE_16X = dict(
    x = 16,
    y = 16,
    z = 16,
    export_file_name="16X"
)

DOWNSAMPLE_RATE_20X = dict(
    x = 20,
    y = 20,
    z = 20,
    export_file_name="20X"
)
'''

DOWNSAMPLE_METHOD = dict(
    AVERAGE = "AVERAGE"
)

EXPORT_FILE_TYPE = dict(
    CSV = "CSV",
    HDF5 = "HDF5"
)

EXPORT_BASE_PATH = "./"
EXPORT_FILENMAME_PREFIX = "downsampled_"
DATE_FORMAT = "%Y%m%dT%H%M%S"

'''
def get_optimal_downsample_rate(shape):
    x = 0
    y = 0
    z = 0

    # TODO find optimal downsample_rate based on shape
    optimal_download_rate = dict(
        x=0,
        y=0,
        z=0,
        export_file_name="OPTIMAL"
    )
    return optimal_download_rate;

'''

def get_or_create_downsampling_rate(rate):
    if(rate == 1):
        return DOWNSAMPLE_RATE_ORIGIN
    if(rate == 2):
        return DOWNSAMPLE_RATE_2X
    elif(rate == 4):
        return DOWNSAMPLE_RATE_4X
    elif(rate == 8):
        return DOWNSAMPLE_RATE_8X
    elif(rate == 27):
        return DOWNSAMPLE_RATE_27X
    elif(rate == 125):
        return DOWNSAMPLE_RATE_125X
    elif(rate == 216):
        return DOWNSAMPLE_RATE_216X
    elif(rate == 343):
        return DOWNSAMPLE_RATE_343X
    elif(rate == 512):
        return DOWNSAMPLE_RATE_512X
    elif(rate == 1000):
        return DOWNSAMPLE_RATE_1000X
    else:
        return dict(
            x=rate,
            y=rate,
            z=rate,
            export_file_name=str(rate) + "X"
        )

def get_downsampling_rates(downsampling_rates):
    downsampling_rate_list = []
    for r in downsampling_rates:
        downsampling_rate =get_or_create_downsampling_rate(r)
        downsampling_rate_list.append(downsampling_rate)
    return downsampling_rate_list