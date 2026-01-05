from pydualsense import pydualsense

# Create controller instance
ds = pydualsense()

# Initialize connection
ds.init()

# source: https://flok.github.io/pydualsense/ds_main.html#features
if ds.state.L2:
    print("Brakes hit")
    #TODO: Add screenshot mechanism and ensure that the the script is running unless manually stopped 