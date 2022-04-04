import numpy as np
import re
import os
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from osgeo import gdal, ogr, osr
from scipy.spatial import ConvexHull
from geojson import Polygon, dump
import sys

#sys.exit("Breaker Triggered")

in_dir = sys.argv[1] #Directory containing input geotiff files

def getContextExtent(ds):
    """ Return list of corner coordinates from a gdal Dataset """
    xmin, xpixel, _, ymax, _, ypixel = ds.GetGeoTransform()
    width, height = ds.RasterXSize, ds.RasterYSize
    xmax = xmin + width * xpixel
    ymin = ymax + height * ypixel

    return (xmin - 110, ymax + 110), (xmax + 110, ymax + 110), (xmax + 110, ymin - 110), (xmin - 110, ymin - 110)

def getExtent(ds):
    """ Return list of corner coordinates from a gdal Dataset """
    xmin, xpixel, _, ymax, _, ypixel = ds.GetGeoTransform()
    width, height = ds.RasterXSize, ds.RasterYSize
    xmax = xmin + width * xpixel
    ymin = ymax + height * ypixel

    return (xmin, ymax), (xmax, ymax), (xmax, ymin), (xmin, ymin)

OutSr = osr.SpatialReference()
OutSr.ImportFromEPSG(4326)

InSr = osr.SpatialReference()
InSr.ImportFromEPSG(32736)

def convertCoord(coord):
    Point = ogr.Geometry(ogr.wkbPoint)
    Point.AddPoint(coord[0], coord[1])
    Point.AssignSpatialReference(InSr)
    Point.TransformTo(OutSr)
    return(Point.GetY(), Point.GetX())

y = []
x = []
for filename in os.listdir(in_dir):
    parts = re.split('_|\.', filename)
#    points.append((int(parts[0]), int(parts[1])))
    y.append(int(parts[0]))
    x.append(int(parts[1]))

X = np.array(x)
Y = np.array(y)
kmeans = KMeans(n_clusters = 15, n_init=100).fit(np.stack((X, Y), axis=1))

u_labels = np.unique(kmeans.labels_)

for i in u_labels:
    if not os.path.exists(f"./clusters/{i}"):
        os.makedirs(f"./clusters/{i}")
    plt.figure()
    plt.scatter(X[np.array(kmeans.labels_ == i)], Y[np.array(kmeans.labels_ == i)], label = i)
    plt.xlim(0, 175)
    plt.ylim(0, 375)
    plt.legend()
    plt.savefig(f"./clusters/{i}/scatter")
    plt.close()


plt.figure()
for i in u_labels:
    plt.scatter(X[np.array(kmeans.labels_ == i)], Y[np.array(kmeans.labels_ == i)], label = i)
plt.legend()
plt.savefig(f"./clusters/scatter")
plt.close()

#save a list of coords
for i in u_labels:
    plt.figure()
    coords = []
    for x, y in np.stack((X, Y), axis=1)[kmeans.labels_ == i]:
        filename = f"boa_images/{y}_{x}.tif"
        ds = gdal.Open(filename)
        corners = getContextExtent(ds)
        coords.extend(corners)
    coords = np.array([*coords])

    hull = ConvexHull(coords)
    plt.plot(coords[:,0], coords[:,1], "o")
    for simplex in hull.simplices:
        plt.plot(coords[simplex, 0], coords[simplex, 1], "k-")
    last = coords[hull.vertices][-1:][0]
    plt.plot(last[0], last[1], "r+")
    plt.savefig(f"clusters/{i}/hull")

    print(np.flip(coords[hull.vertices], axis=0))

    convertedCoords = []
    for coord in np.flip(coords[hull.vertices], axis=0):
        convertedCoords.append(convertCoord(coord))
    print(convertedCoords)
    poly = Polygon([convertedCoords + [convertedCoords[0]]])
    with open(f"clusters/{i}/polygon.geojson", "w") as outfile:
        dump(poly, outfile, indent=4)