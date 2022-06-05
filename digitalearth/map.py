from typing import Any, List, Tuple, Union
from collections import OrderedDict

import geoplot as gplt
import geoplot.crs as gcrs
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
from geopandas import GeoDataFrame
from loguru import logger
from osgeo import gdal
from osgeo.gdal import Dataset

from pyramids.catchment import Catchment as GC
from pyramids.raster import Raster
# from Hapi.plot.visualizer import MidpointNormalize, Map
from statista.tools import Tools as ST


class Map:
    """
    Map
    """
    figure_default_options = dict(
        ylabel="",
        xlabel="",
        legend="",
        legend_size=10,
        figsize=(10, 8),
        labelsize=10,
        fontsize=10,
        name="hist.tif",
        color1="#3D59AB",
        color2="#DC143C",
        linewidth=3,
        Axisfontsize=15,
    )


    linestyles = OrderedDict(
        [
            ("solid", (0, ())),  # 0
            ("loosely dotted", (0, (1, 10))),  # 1
            ("dotted", (0, (1, 5))),  # 2
            ("densely dotted", (0, (1, 1))),  # 3
            ("loosely dashed", (0, (5, 10))),  # 4
            ("dashed", (0, (5, 5))),  # 5
            ("densely dashed", (0, (5, 1))),  # 6
            ("loosely dashdotted", (0, (3, 10, 1, 10))),  # 7
            ("dashdotted", (0, (3, 5, 1, 5))),  # 8
            ("densely dashdotted", (0, (3, 1, 1, 1))),  # 9
            ("loosely dashdotdotted", (0, (3, 10, 1, 10, 1, 10))),  # 10
            ("dashdotdotted", (0, (3, 5, 1, 5, 1, 5))),  # 11
            ("densely dashdotdotted", (0, (3, 1, 1, 1, 1, 1))),  # 12
            ("densely dashdotdottededited", (0, (6, 1, 1, 1, 1, 1))),# 13
        ]
    )


    marker_style_list = [
        "--o",
        ":D",
        "-.H",
        "--x",
        ":v",
        "--|",
        "-+",
        "-^",
        "--s",
        "-.*",
        "-.h",
    ]
    def __init__(self):
        pass

    @staticmethod
    def lineStyle(style: Union[str, int] = "loosely dotted"):
        """LineStyle.

        Line styles for plotting

        Parameters
        ----------
        style : TYPE, optional
            DESCRIPTION. The default is 'loosely dotted'.

        Returns
        -------
        TYPE
            DESCRIPTION.
        """
        if isinstance(style, str):
            try:
                return Map.linestyles[style]
            except KeyError:
                msg = (
                    " The style name you entered-{0}-does not exist please"
                    "choose from the available styles"
                ).format(style)
                print(msg)
                print(list(Map.linestyles))
        else:
            return list(Map.linestyles.items())[style][1]


    @staticmethod
    def markerStyle(style: int):
        """MarkerStyle.

        Marker styles for plotting

        Parameters
        ----------
        style : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        if style > len(Map.marker_style_list) - 1:
            style = style % len(Map.marker_style_list)
        return Map.marker_style_list[style]



    @staticmethod
    def plotGeo(
            src: Union[Dataset, np.ndarray],
            point_color: str = "red",
            point_size: Union[int, float] = 100,
            pid_color="blue",
            pid_size: Union[int, float] = 10,
            **kwargs
    ):
        """PlotArray.

            plot an array/ gdal dataset

        Parameters
        ----------
        src : [array/gdal.Dataset]
            the array/gdal raster you want to plot.
        point_color : [str], optional
            color of the points. The default is 'red'.
        point_size : [integer], optional
            size of the points. The default is 100.
        pid_color : [str]
            the ID of the Point.The default is "blue".
        pid_size : [integer]
            size of the ID text. The default is 10.
        pid_color : []

        rotation : []

        midpoint : []

        **kwargs : [dict]
            keys:
                nodataval: Union[int, float] = np.nan,
            figsize: Tuple[int, int] = (8, 8),
            title: Any = "Total Discharge",
            title_size: Union[int, float] = 15,
            cbar_length: Union[int, float] = 0.75,
            orientation: str = "vertical",
            cbar_label_size: Union[int, float] = 12,
            cbar_label: str = "Color bar label",
            rotation: Union[int, float] = -90,
            ticks_spacing: Union[int, float] = 5,
            num_size: Union[int, float] = 8,
            color_scale: int = 1,
            cmap: str = "coolwarm_r",
            gamma: Union[int, float] = 0.5,
            linscale: Union[int, float] = 0.001,
            linthresh: Union[int, float] = 0.0001,
            midpoint: int = 0,
            display_cellvalue: bool = False,
            background_color_threshold=None,

        Returns
        -------
        axes: [figure axes].
            the axes of the matplotlib figure
        fig: [matplotlib figure object]
            the figure object
        """

        arr, nodataval = Raster.getRasterData(src)
        arr = arr.astype(np.float32)
        arr[np.isclose(arr, nodataval, rtol=0.001)] = np.nan

        if "points" in kwargs.keys():
            points = kwargs["points"]
            points["row"] = np.nan
            points["col"] = np.nan
            # to locte the points in the array
            points.loc[:, ["row", "col"]] = GC.nearestCell(
                src, points[["x", "y"]][:]
            ).values

        fig, ax = Map.plotArray(arr,nodataval)
        PoitsID = list()
        if "points" in kwargs.keys():
            row = points.loc[:, "row"].tolist()
            col = points.loc[:, "col"].tolist()
            IDs = points.loc[:, "id"].tolist()
            Points = ax.scatter(col, row, color=point_color, s=point_size)

            for i in range(len(row)):
                PoitsID.append(
                    ax.text(
                        col[i],
                        row[i],
                        IDs[i],
                        ha="center",
                        va="center",
                        color=pid_color,
                        fontsize=pid_size,
                    )
                )

        # # Normalize the threshold to the images color range.
        # if background_color_threshold is not None:
        #     background_color_threshold = im.norm(background_color_threshold)
        # else:
        #     background_color_threshold = im.norm(np.nanmax(arr)) / 2.0

        return fig, ax


    @staticmethod
    def plotCatchment(
            points: GeoDataFrame,
            column_name: Any,
            poly: GeoDataFrame,
            line: GeoDataFrame,
            scheme: Any = None,
            scale_func: Any = '',
            cmap: str = "viridis",
            legend_values: List = [],
            legend_labels: List = [],
            figsize: Tuple = (8, 8),
            title: Any = 'title',
            title_size: int = 500,
            save: Union[bool, str] = False,
    ):
        """PlotCatchment.

        Inputs:
        ------
        points:[GeoDataFrame]
            geodataframe contains values to plot in one of its columns.
        column_name: [str]
            name of the column you want to plot its values.
        poly: [GeoDataFrame]
            geodataframe contains polygon geometries.
        line: [GeoDataFrame]
            geodataframe contains linestring geometries.
        figsize: [Tuple]
            fize oif the figure.
        title:[str]
            title of the figure.
        save: [bool/str]
            if you want to save the plot provide the path with the extention,
            Default is False.
        """
        # unify the projection
        if not poly.crs.is_geographic:
            logger.debug("The coordinate system of the poly geodataframe is not geographic"
                         "SO, it will be reprojected to WGS-84")
            poly.to_crs(4326, inplace=True)

        epsg = poly.crs.to_json()
        line.to_crs(epsg, inplace=True)
        points.to_crs(epsg, inplace=True)

        pointplot_kwargs = {'edgecolor': 'white', 'linewidth': 0.9}  # 'color': "crimson"

        # make sure that the plotted column is numeric
        points[column_name] = points[column_name].map(float)

        fig, ax = plt.subplots(1, 1, figsize=figsize, subplot_kw={'projection': gcrs.AlbersEqualArea()})
        if scheme:

            gplt.pointplot(points, projection=gcrs.AlbersEqualArea(),
                           hue=column_name, cmap=cmap,
                           scale=column_name, limits=(4, 20),
                           scheme=scheme,
                           # scale_func = scale_func,
                           legend=True,
                           legend_var='scale',
                           legend_kwargs={  # 'loc': 'upper right',
                               'bbox_to_anchor': (1, 0.35)},
                           ax=ax, **pointplot_kwargs  # ,
                           )
        else:
            gplt.pointplot(points, projection=gcrs.AlbersEqualArea(),
                           hue=column_name, cmap=cmap,
                           scale=column_name, limits=(4, 20),
                           scale_func=scale_func,
                           legend=True,
                           legend_var='scale',
                           legend_values=legend_values,
                           legend_labels=legend_labels,
                           legend_kwargs={  # 'loc': 'upper right',
                               'bbox_to_anchor': (1, 0.35)},
                           ax=ax, **pointplot_kwargs  # ,
                           )

        gplt.polyplot(poly, ax=ax, edgecolor='grey', facecolor='grey',  # 'lightgray',
                      linewidth=0.5, extent=poly.total_bounds)  # # , zorder=0

        gplt.polyplot(line, ax=ax, linewidth=10)

        plt.title(title, fontsize=title_size)
        # plt.subplots_adjust(top=0.99999, right=0.9999, left=0.000005, bottom=0.000005)
        if save:
            plt.savefig(save, bbox_inches='tight', transparent=True)

        return fig, ax


class Scale:

    def __init__(self):
        pass


    def log_scale(minval, maxval):
        def scalar(val):
            val = val + abs(minval) + 1
            return np.log10(val)


        return scalar


    def power_scale(minval, maxval):
        def scalar(val):
            val = val + abs(minval) + 1
            return (val / 1000) ** 2


        return scalar


    def identity_scale(minval, maxval):
        def scalar(val):
            return 2


        return scalar


class MidpointNormalize(colors.Normalize):
    """MidpointNormalize.

    !TODO needs docs

    """

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        """MidpointNormalize.

        ! TODO needs docs

        Parameters
        ----------
        value : TYPE
            DESCRIPTION.
        clip : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]

        return np.ma.masked_array(np.interp(value, x, y))
