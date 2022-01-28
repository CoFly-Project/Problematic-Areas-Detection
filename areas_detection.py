import numpy as np
import cv2
from scipy import io
import os
import glob
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import morphology, measure, filters
import re
import argparse
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

	# -- Plot the VI map and save it in ~PROJECT_PATH -- #
	spot_size = np.sqrt(np.shape(index)[0] ** 2 + np.shape(index)[1] ** 2)
	f = plt.figure()
	f.set_figheight(index.shape[0] / f.get_dpi())
	f.set_figwidth(index.shape[1] / f.get_dpi())
	ax = plt.Axes(f, [0., 0., 1., 1.])
	ax.set_axis_off()
	f.add_axes(ax)
	ax.imshow(np.clip(index, lower, upper), cmap="RdYlGn", aspect='auto')
	ax.scatter(centers_cluster[:, 1], centers_cluster[:, 0], s=0.5 * spot_size, c='dodgerblue', edgecolors='black', linewidth=5)
	f.savefig('{}/{}_centers.png'.format(save_dir, index_name), transparent = True)
	plt.close()

	return centers_cluster

# -- Find the geolocation of the points of interest (centers) -- #
def find_Lat_Lon(raster, centers):
	xoff, a, b, yoff, d, e = raster.GetGeoTransform()
	crs = osr.SpatialReference()
	crs.ImportFromWkt(raster.GetProjectionRef())
	
	crsGeo = osr.SpatialReference()
	crsGeo.ImportFromProj4('+proj=longlat +datum=WGS84 +no_defs')
	transform = osr.CoordinateTransformation(crs, crsGeo)

	centers_lat_lon = []
	for x_pixel, y_pixel in centers:
		xp = a * x_pixel + b * y_pixel + a * 0.5 + b * 0.5 + xoff
		yp = d * x_pixel + e * y_pixel + d * 0.5 + e * 0.5 + yoff
		(lat, lon, z) = transform.TransformPoint(xp, yp)
		centers_lat_lon.append([lat, lon])

	centers_geo = np.array(centers_lat_lon)
	centers = np.fliplr(centers_geo)
	return centers

# -- Read the given arguments -- #
parser = argparse.ArgumentParser()
parser.add_argument('--input_image', required=True, help="Please enter the absolute path of the image.")
parser.add_argument('--index', required=True, help="Please enter the absolute path of the *.npy file that corresponds to the input image.")
args = parser.parse_args()

save_dir = os.path.dirname(args.input_image)
index_name, extension = os.path.splitext(os.path.basename(args.index))
index_array = np.load(args.index)

ds = gdal.Open(args.input_image, gdal.GA_ReadOnly)
centers_clusters = find_areas(index_array)

data = []
prj = ds.GetProjection()

if prj: 
	centers_geo = find_Lat_Lon(ds, centers_clusters)
	for center in centers_geo:
		data.append({"Lattitude": center[0], "Longtitude": center[1]})
else:
	centers_pixel_level = centers_clusters
	for center in centers_pixel_level:
		data.append({"X_pixel": center[1], "Y_pixel": center[0]})

with open(os.path.join(save_dir, str(index_name)+'.json'), "w") as file:
	json.dump(data, file, indent=4)

print('Done!')
