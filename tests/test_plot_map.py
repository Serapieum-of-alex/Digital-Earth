import pandas as pd
from matplotlib.figure import Figure
from osgeo.gdal import Dataset

from digitalearth.static import Map


class TestPlotArray:
    def test_plot(self, src: Dataset):
        fig, ax = Map.plot(src, title="Flow Accumulation")
        assert isinstance(fig, Figure)

    def test_plot_with_points(
        self,
        src: Dataset,
        display_cellvalue: bool,
        points: pd.DataFrame,
        num_size: int,
        background_color_threshold,
        ticks_spacing: int,
        pid_size: int,
        pid_color: str,
        point_size: int,
        point_color: str,
    ):
        fig, ax = Map.plot(
            src,
            point_color=point_color,
            point_size=point_size,
            pid_color=pid_color,
            pid_size=pid_size,
            points=points,
            display_cellvalue=display_cellvalue,
            num_size=num_size,
            background_color_threshold=background_color_threshold,
            ticks_spacing=ticks_spacing,
        )

        assert isinstance(fig, Figure)
