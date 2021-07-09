import math
import rasterio
from rasterio.transform import from_origin
from rasterio.crs import CRS
import numpy as np

# Options

output_file = "output.tif"
# Could be lzw, deflate, packbits, or none
compression_method = "none"

######

# Import the CSV file all.csv to a numpy array

with open("all.csv", "rb") as inputfile:
    rawdata = np.genfromtxt(inputfile, delimiter=",", names=True)

######

# Create a numpy array that is the shape of our output GeoTIFF

# This is the "Level of Detail" as defined by the Bing Maps Tile System
# https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system
level = 6

# https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system#pixel-coordinates
gridwidth = gridheight = 256 * (2 ** level) - 1

# Create a new numpy array that is our desired shape
gridarray = np.full((gridwidth, gridheight), None, dtype="float32")

######

# Insert each RWI value into its appropriate element of our array

for point in rawdata:
    # These functions are also from Bing Tile System documentation
    # https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system#pixel-coordinates
    sinLatitude = math.sin(point["latitude"] * math.pi / 180)
    cellX = math.floor(
        (0.5 - math.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * math.pi))
        * 256
        * 2 ** 6
    )
    cellY = math.floor(((point["longitude"] + 180) / 360) * 256 * 2 ** 6)
    gridarray[cellX][cellY] = point["rwi"]

######

# Write array to GeoTiff

with rasterio.Env():

    # "The WGS 84 datum surface is an oblate spheroid with equatorial radius a = 6378137m"
    # https://en.wikipedia.org/wiki/World_Geodetic_System#Definition
    proj_bounds = 6378137 * math.pi

    # 2445.9849 is from this table, Level of Detail = 6:
    # https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system#ground-resolution-and-map-scale
    # I am concerned that I am making an error, because proj_bounds / gridwidth * 2 != 2445.9849
    # print(proj_bounds / gridwidth * 2)
    ground_res = 2445.9849

    transform = from_origin(-proj_bounds, proj_bounds, ground_res, ground_res)

    profile = {
        "driver": "GTiff",
        "width": gridwidth,
        "height": gridheight,
        "count": 1,
        "dtype": "float32",
        "crs": CRS.from_epsg(3857),
        "transform": transform,
        "compress": compression_method,
    }

    with rasterio.open(output_file, "w", **profile) as dst:
        dst.write(gridarray, 1)
