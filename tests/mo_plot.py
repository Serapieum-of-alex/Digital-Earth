import matplotlib
matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt
from digitalearth.map import Map
from osgeo import gdal

#%%
src = gdal.Open("examples/data/acc4000.tif")
src_arr = src.ReadAsArray()
src_no_data_value = src.GetRasterBand(1).GetNoDataValue()
cmap = "terrain"
#%%
fig, ax = Map.plotGeo(src, Title="Flow Accumulation")
#%%
fig, ax = Map.plotArray(src_arr, nodataval=src_no_data_value, Title="Flow Accumulation")

#%%

