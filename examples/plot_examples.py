import matplotlib

matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt
import pandas as pd
from osgeo import gdal

from digitalearth.map import Map

#%%
src = gdal.Open("examples/data/acc4000.tif")
src_no_data_value = src.GetRasterBand(1).GetNoDataValue()
cmap = "terrain"
#%%
# fig, ax = Map.plot(src, title="Flow Accumulation")
#%%
points = pd.read_csv("examples/data/points.csv")
# fig, ax = Map.plot(src, title="Flow Accumulation", points=points)

point_color = "blue"
point_size = 100
id_color = "green"
id_size = 20

display_cellvalue = True
num_size = 8
background_color_threshold = None
ticks_spacing = 500

fig, ax = Map.plot(
            src,
            point_color=point_color,
            point_size=point_size,
            pid_color=id_color,
            pid_size=id_size,
            points=points,
            display_cellvalue=display_cellvalue,
            num_size=num_size,
            background_color_threshold=background_color_threshold,
            ticks_spacing=ticks_spacing,
        )
