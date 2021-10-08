import numpy as np
import cv2
from scipy import io
import os
from scipy import ndimage
from skimage import morphology, measure, filters
from exif import Image
import sys
from osgeo import gdal, osr
import json
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabasz_score


def threshold_index(index, tresh_value):
	_, areas_mask = cv2.threshold(index, tresh_value, 1, cv2.THRESH_BINARY_INV)
	areas_mask[areas_mask > 0] = 255
	return areas_mask


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
	index_clear = index[~np.isnan(index)]
	lower = np.min(index_clear)
	upper = np.max(index_clear)
	empty_space = index != index

	thres = (lower + (upper + lower) / 2) / 2
	mask = threshold_index(index, thres)
	mask = (mask / 255).astype(np.uint8)

	mask = ndimage.morphology.binary_closing(mask, np.ones((5, 5)), iterations=1).astype(np.uint8)
	mask = ndimage.morphology.binary_opening(mask, np.ones((5, 5)), iterations=1).astype(np.uint8)

	mask_white = np.copy(mask)
	mask_white[empty_space] = 1

	labels, nlabels = measure.label(mask, connectivity=2, background=0, return_num=True)
	centers = ndimage.center_of_mass(mask, labels, np.arange(nlabels) + 1)
	centers = np.array(centers)

	_, num_pixels = np.unique(labels, return_counts=True)

	opt_K = find_optimal_K(centers, num_pixels)
	kmeans = KMeans(n_clusters=opt_K, random_state=0).fit(centers, sample_weight=num_pixels[1:])
	centers_cluster = kmeans.cluster_centers_
	return centers_cluster


def find_Lat_Lon(img, centers):
	ds = gdal.Open(img)
	gt = ds.GetGeoTransform()
	old_cs= osr.SpatialReference()
	old_cs.ImportFromWkt(ds.GetProjectionRef())

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
	width = ds.RasterXSize
	height = ds.RasterYSize

	centers_lat_lon = []
	for y_pixel, x_pixel in centers:
		gt = ds.GetGeoTransform()
		xoff, a, b, yoff, d, e = gt
		xp = a * x_pixel + b * y_pixel + xoff
		yp = d * x_pixel + e * y_pixel + yoff
		(lat, lon, z) = transform.TransformPoint(xp, yp)
		centers_lat_lon.append([lat, lon])
	return np.array(centers_lat_lon)

def decimal_coords(coords, ref):
	decimal_degrees = coords[0] + (coords[1] / 60) + (coords[2] / 3600)
	if ref == "N" or ref == "E":
		decimal_degrees = decimal_degrees
	else:
		decimal_degrees = -decimal_degrees
	return decimal_degrees


def winapi_path(dos_path, encoding=None):
    if (not isinstance(dos_path, str) and encoding is not None): 
        dos_path = dos_path.decode(encoding)
    path = os.path.abspath(dos_path)
    if path.startswith(u"\\\\"):
        return u"\\\\?\\UNC\\" + path[2:]
    return u"\\\\?\\" + path


img_path = winapi_path(sys.argv[1])
save_dir = winapi_path(sys.argv[2])
images_dir = winapi_path(sys.argv[3])
os.environ['GDAL_DATA'] = './gdal'
os.environ['PROJ_LIB'] = './proj'

lat_lon_imgs = []
for image in os.listdir(images_dir):
	img = Image(os.path.join(images_dir, image))
	if img.has_exif:
		try:
			lat_, lon_ = decimal_coords(img.gps_latitude,img.gps_latitude_ref), decimal_coords(img.gps_longitude,img.gps_longitude_ref)
			data = {'Lat': lat_, 'Lon': lon_, 'Image': image}
			lat_lon_imgs.append(data)
		except AttributeError:
		  print('The {} has no metadata'.format(image))
	else:
		print('All the necessary info has been saved')


lat_lon_imgs = pd.DataFrame(lat_lon_imgs)
index_names = ['vari', 'ngrdi', 'gli', 'ngbdi']

for index_name in index_names:
	index = np.load(os.path.join(save_dir, index_name + '_clipped.npy'))
	centers_cluster = find_areas(index)
	centers_geo = find_Lat_Lon(img_path, centers_cluster)

	knn = NearestNeighbors(n_neighbors=1, metric='haversine').fit(lat_lon_imgs[['Lat', 'Lon']])
	dist, idxs = knn.kneighbors(centers_geo)

	data = []
	for center, index in zip(centers_geo, idxs):
		data.append({"Lat": center[0], "Lon": center[1], "Nearest_image": lat_lon_imgs['Image'].iloc[index].item()})

	with open(os.path.join(save_dir, str(index_name)+'.json'), "w") as file:
		json.dump(data, file, indent=4)

print('Done!')
