import matplotlib

matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt
import pandas as pd
from osgeo import gdal

from digitalearth.static import Map

#%%
src = gdal.Open("examples/data/acc4000.tif")
src_no_data_value = src.GetRasterBand(1).GetNoDataValue()
cmap = "terrain"
#%%
fig, ax = Map.plot(src, title="Flow Accumulation", cbar_label="Flow Accumulation")
#%%
points = pd.read_csv("examples/data/points.csv")
# fig, ax = Map.plot(src, title="Flow Accumulation", points=points)

point_color = "blue"
point_size = 100
id_color = "yellow"
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
            title="Flow Accumulation",
            cbar_label="Flow Accumulation"
        )
import branca.colormap as cm
import folium

#%%
import geopandas as gpd
from folium import plugins
from folium.features import GeoJsonPopup, GeoJsonTooltip

rhine_basin = gpd.read_file("examples/data/rhine_basin.geojson")
rhine_river = gpd.read_file("examples/data/rhine_river_centerline.geojson")
# gauges = gpd.read_file("examples/data/rhine_gauges.geojson")
metrix = gpd.read_file("examples/data/MetricsHM_Q_Obs.geojson")


print(rhine_river.crs)
print(rhine_basin.crs)
print(metrix.crs)
# rhine_river.
# legend_values = [1, 0.8, 0.6, 0.4, 0.2, 0] # dicaharge nse
def scale_func(x):
    if x >= 1:
        return 10
    elif 0.6 <= x < 0.8:
        return 7
    elif 0.4 <= x < 0.6:
        return 5
    elif 0.2 <= x < 0.4:
        return 3
    elif 0.1 <= x < 0.2:
        return 2
    else:
        return 1

metrix["NSE"] = metrix["NSE"].map(float)
metrix["nse_size"] = metrix["NSE"].apply(scale_func)
colormap = cm.StepColormap(
    ["black", "lightblue", "brown","darkblue", "Orange", "green","#DC143C",],
    index=[0, 0.1, 0.2, 0.4, 0.6, 0.8, 1], caption="NSE",
    vmin=50, vmax=400,
)

datajson = metrix.to_json()
datadict = metrix.to_dict()
# fields are columns in the dataframe
# aliases are the names that will appear in the popup instead of the column names
popup = GeoJsonPopup(
    fields=["rcasiteid", "NSE"],
    aliases=["Site ID", "NSE"],
    localize=True,
    labels=True,
    style="background-color: yellow;",
)

tooltip = GeoJsonTooltip(
    fields=["rcasiteid", "NSE"],
    aliases=["Site ID", "NSE"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)


def color30(feature):
    # print("color30")
    # return datadict['color30'][int(feature['id'])]
    return colormap(feature['properties']['NSE'])

def size30(feature):
    return datadict['nse_size'][int(feature['id'])]

map = folium.Map([40, -100], zoom_start=5)

folium.GeoJson(
    datajson,
    name="Water Level NSE - Markers",
    marker=folium.CircleMarker(fill_color='orange', radius=4,
                               fill_opacity=0.7, color="black", weight=1),
    popup=popup,
    tooltip=tooltip,
    style_function=lambda feature: {
        "fillColor": color30(feature),
        "radius": size30(feature),
    },
    highlight_function=lambda x: {"fillOpacity": 0.8},
    zoom_on_click=True,
).add_to(map)

map.add_child(folium.LatLngPopup())
# Gen_lat , Gen_long are the latitude and logitude for the points
# size100 is the calculated size of the points
# location_data = data.loc[:, ['Gen_lat', 'Gen_long', 'size100']].values
# map.add_child(plugins.HeatMap(location_data, radius=10, name="SOCstock100 - Heat Map ", ))

folium.TileLayer('cartodbpositron').add_to(map)
folium.TileLayer('cartodbdark_matter').add_to(map)
folium.TileLayer('Stamen Terrain').add_to(map)
folium.TileLayer('Stamen Toner').add_to(map)
folium.TileLayer('Stamen Water Color').add_to(map)
print("- Create Layer control")
folium.LayerControl().add_to(map)
map.save('src/RCS.html')
