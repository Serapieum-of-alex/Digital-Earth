from typing import List

import numpy as np
import pandas as pd
import pytest
from osgeo import gdal
from osgeo.gdal import Dataset


@pytest.fixture(scope="module")
def src() -> Dataset:
    return gdal.Open("examples/data/acc4000.tif")


@pytest.fixture(scope="module")
def display_cellvalue() -> bool:
    return True


@pytest.fixture(scope="module")
def background_color_threshold():
    return None


@pytest.fixture(scope="module")
def num_size() -> int:
    return 8


@pytest.fixture(scope="module")
def ticks_spacing() -> int:
    return 500


@pytest.fixture(scope="module")
def points() -> pd.DataFrame:
    return pd.read_csv("examples/data/points.csv")


@pytest.fixture(scope="module")
def pid_size() -> int:
    return 20


@pytest.fixture(scope="module")
def pid_color() -> str:
    return "green"


@pytest.fixture(scope="module")
def point_size() -> int:
    return 100


@pytest.fixture(scope="module")
def point_color() -> str:
    return "blue"
