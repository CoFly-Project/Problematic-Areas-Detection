import numpy as np
import cv2
from scipy import io
import os
import glob
from scipy import ndimage
from skimage import morphology, measure, filters
import re
import sys
from osgeo import gdal, osr
import json
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabasz_score

# -- Thresholding the index array -- #
def threshold_index(index, tresh_value):
	_, areas_mask = cv2.threshold(index, tresh_value, 1, cv2.THRESH_BINARY_INV)
	areas_mask[areas_mask > 0] = 255
	return areas_mask

# -- Find the number of clusters based on the maximization of the Calinski-Harabasz score, in the interval [2, 10] -- #
def find_optimal_K(centers, num_pixels):
	metric = 'calinski'
	scores = []
	if np.shape(centers)[0] < 10:
		clusters = np.arange(2, np.shape(centers)[0])
	else:
		clusters = [2, 3, 4, 5, 6, 7, 8, 9, 10]
	for n_clusters in clusters:
		cluster = KMeans(n_clusters=n_clusters, random_state=10)
		cluster_labels = cluster.fit_predict(centers, sample_weight=num_pixels[1:])
		if metric == 'silhouette':
			scores.append(silhouette_score(centers, cluster_labels))
		elif metric == 'calinski':
			scores.append(calinski_harabasz_score(centers, cluster_labels))
		else:
			print('Unknown score')

	opt_K = clusters[np.argmax(scores)]
	return opt_K

def find_areas(index):
	# -- Mask nan Values -- #
	index_clear = index[~np.isnan(index)]
	lower = np.min(index_clear)
	upper = np.max(index_clear)
	empty_space = index != index
	
	# -- Find Regions -- #
	thres = (lower + (upper + lower) / 2) / 2 # -- 25% range -- # 
	mask = threshold_index(index, thres)
	mask = (mask / 255).astype(np.uint8)

	mask = ndimage.morphology.binary_closing(mask, np.ones((5, 5)), iterations=1).astype(np.uint8)
	mask = ndimage.morphology.binary_opening(mask, np.ones((5, 5)), iterations=1).astype(np.uint8)
	
	# -- Create binary image -- #
	mask_white = np.copy(mask)
	mask_white[empty_space] = 1
	
	# -- A connected components analysis is applied in order to detect connected components on the binary image of the problematic areas -- #
	labels, nlabels = measure.label(mask, connectivity=2, background=0, return_num=True)
	
	# -- Find the center of each calculated area -- #
	centers = ndimage.center_of_mass(mask, labels, np.arange(nlabels) + 1)
	centers = np.array(centers)

	_, num_pixels = np.unique(labels, return_counts=True)
	
	# -- Cluster centers -- #
	opt_K = find_optimal_K(centers, num_pixels)
	kmeans = KMeans(n_clusters=opt_K, random_state=0).fit(centers, sample_weight=num_pixels[1:])
	centers_cluster = kmeans.cluster_centers_

	return centers_cluster

# -- Find the geolocation of the points of interest (centers) -- #
def find_Lat_Lon(raster, centers):
	gt = raster.GetGeoTransform()
	old_cs= osr.SpatialReference()
	old_cs.ImportFromWkt(raster.GetProjectionRef())

	wgs84_wkt = """
	GEOGCS["WGS 84",
		DATUM["WGS_1984",
			SPHEROID["WGS 84",6378137,298.257223563,
				AUTHORITY["EPSG","7030"]],
			AUTHORITY["EPSG","6326"]],
		PRIMEM["Greenwich",0,
			AUTHORITY["EPSG","8901"]],
		UNIT["degree",0.01745329251994328,
			AUTHORITY["EPSG","9122"]],
		AUTHORITY["EPSG","4326"]]"""

	new_cs = osr.SpatialReference()
	new_cs.ImportFromWkt(wgs84_wkt)
	transform = osr.CoordinateTransformation(old_cs,new_cs)

	centers_lat_lon = []
	for y_pixel, x_pixel in centers:
		gt = ds.GetGeoTransform()
		xoff, a, b, yoff, d, e = gt
		xp = a * x_pixel + b * y_pixel + xoff
		yp = d * x_pixel + e * y_pixel + yoff
		(lat, lon, z) = transform.TransformPoint(xp, yp)
		centers_lat_lon.append([lat, lon])

	return np.array(centers_lat_lon)

def winapi_path(dos_path, encoding=None):
    if (not isinstance(dos_path, str) and encoding is not None): 
        dos_path = dos_path.decode(encoding)
    path = os.path.abspath(dos_path)
    if path.startswith(u"\\\\"):
        return u"\\\\?\\UNC\\" + path[2:]
    return u"\\\\?\\" + path

project_path = winapi_path(sys.argv[1])
txt_file = winapi_path(sys.argv[2])
os.environ['GDAL_DATA'] = winapi_path(os.path.join(os.getcwd(), 'gdal'))
os.environ['PROJ_LIB'] = winapi_path(os.path.join(os.getcwd(), 'proj'))

with open(txt_file) as f:
	names = f.read().splitlines()
	lat = [float(i) for i in ([re.findall(r"\d+\.\d+", i)[0] for i in names])]
	lon = [float(i) for i in ([re.findall(r"\d+\.\d+", i)[1] for i in names])]
	f.close()
	
coordinates = np.array(list(zip(lat, lon)))

for tiff_file in glob.glob(os.path.join(project_path, '*tif')):
	path, _ = os.path.splitext(tiff_file)
	index_name = os.path.basename(path)

	ds = gdal.Open(os.path.join(project_path, tiff_file), gdal.GA_ReadOnly)
	index_array = np.load(os.path.join(project_path, index_name + '.npy'))
		
	centers_clusters = find_areas(index_array)
	centers_geo = find_Lat_Lon(ds, centers_clusters)
	
	# -- KNN method in order to find the nearest image of each center -- #
	knn = NearestNeighbors(n_neighbors=1, metric='haversine').fit(coordinates)
	dist, idxs = knn.kneighbors(centers_geo)

	data = []
	for center, idx in zip(centers_geo, idxs.flatten()):
		data.append({"Lat": center[0], "Lon": center[1], "Nearest_image": names[idx]})
	
	# -- Save a *.json file with the name of each VI in ~PROJECT_PATH -- #
	with open(os.path.join(project_path, str(index_name)+'.json'), "w") as file:
		json.dump(data, file, indent=4)
	
print('Done!')
