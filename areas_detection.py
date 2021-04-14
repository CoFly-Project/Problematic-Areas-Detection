import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy import io
import os
from scipy import ndimage
from skimage import morphology, measure, filters

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabasz_score

class Indexes:
	def __init__(self, img):
		self.img = img
		# self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
		self.R = self.img[:, :, 2].astype(np.float32)
		self.G = self.img[:, :, 1].astype(np.float32)
		self.B = self.img[:, :, 0].astype(np.float32)

	def VARI(self):
		vari = np.divide((self.G - self.R), (self.G + self.R - self.B + 0.00001))
		return np.clip(vari, -1, 1)

	def GLI(self):
		gli = np.divide((2 * self.G - self.R - self.B), (2 * self.G + self.R + self.B + 0.00001))
		return np.clip(gli, -1, 1)

	def Visual_NDVI(self): # Normalized green red difference index
		v_ndvi = np.divide((self.G - self.R), (self.G + self.R + 0.00001))
		return np.clip(v_ndvi, -1, 1)

	def NGBDI(self):
		ngbdi = (self.G - self.B) / (self.G + self.B + 0.00001)
		ngbdi = np.clip(ngbdi, -1, +1)
		return ngbdi

	def TGI(self):
		tgi = -0.5 * (190 * (self.R - self.G) - 120 * (self.R - self.B))  # Triangular greenness index
		# tgi = np.clip(tgi, -1, +1)
		# return tgi
		mask = np.not_equal(self.G - self.R + self.B - 255.0, 0.0)
		tgi =  np.choose(mask, (-9999.0, np.subtract(self.G, np.multiply(0.39, self.R), np.multiply(0.61, self.B))))
		tgi = tgi/127 - 1
		return np.clip(tgi, -1, 1)



	def get_index(self, index_name):
		if index_name == 'vari':
			return self.VARI()
		elif index_name == 'gli':
			return self.GLI()
		elif index_name == 'vndvi':
			return self.Visual_NDVI()
		elif index_name == 'ngbdi':
			return self.NGBDI()
		elif index_name == 'tgi':
			return self.TGI()
		else:
			print('Uknown index')


def find_real_min_max(perc, edges, index_clear):
	mask = perc > (0.05 * len(index_clear))
	edges = edges[:-1]
	min_v = edges[mask].min()
	max_v = edges[mask].max()
	return min_v, max_v

def mask_empty_space(img):
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
	# plt.figure()
	# plt.title('binary threshold to 0')
	# plt.imshow(thresh, cmap='gray')
	# plt.show()

	# Close contour
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
	close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

	# Find outer contour and fill with white
	cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]
	cv2.fillPoly(close, cnts, [255,255,255])
	# plt.figure()
	# plt.title('mask')
	# plt.imshow(close, cmap='gray')
	# plt.show()

	img = img.astype(np.float)
	img[close == 0] = np.nan
	return  img

# def threshold_index(index, tresh_value):
# 	_, bin_zero = cv2.threshold(index, 0, 1, cv2.THRESH_BINARY_INV)
# 	_, bin_min  = cv2.threshold(index, tresh_value, 1, cv2.THRESH_BINARY_INV)
# 	areas_mask = bin_zero + bin_min
# 	areas_mask[areas_mask > 0 ] = 255
#
# 	return areas_mask

def threshold_index(index, tresh_value):
	_, areas_mask  = cv2.threshold(index, tresh_value, 1, cv2.THRESH_BINARY_INV)
	areas_mask[areas_mask > 0 ] = 255
	return areas_mask



def mask_empty_space(img):
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
	# Close contour
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
	close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

	# Find outer contour and fill with white
	cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]
	cv2.fillPoly(close, cnts, [255,255,255])

	img = img.astype(np.float)
	img[close == 0] = np.nan
	return img



def find_optimal_K(centers, num_pixels):
	metric = 'calinski'
	scores = []
	if np.shape(centers)[0] < 10:
		clusters = np.arange(2,np.shape(centers)[0])
	else:
		clusters = [2,3,4,5,6,7,8,9,10]
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



def index_analysis(Idx, index_name, empty_space):

	index = Idx.get_index(index_name)

	# -- Calculate index histogram -- #
	# _ = plt.hist(index.flatten(), bins=[-0.5, 0.2, 0.3, 0.6, 1.], color = 'darkcyan', edgecolor='black')
	index_clear = index[~np.isnan(index)]
	print('Mean: {}'.format(np.mean(index_clear)))
	print('Median: {}'.format(np.median(index_clear)))

# thres = np.mean(index_clear)

	plt.figure()
	perc, edges, _ = plt.hist(index_clear, bins=100, range=(-1, 1), color = 'darkcyan', edgecolor='black')
	plt.title("Histogram")
	plt.xlim(-1, 1)
	plt.savefig('{}/{}_hist.png'.format(save_dir, index_name),pad_inches=0)
	plt.close()



	# -- Plot index (-1, 1) -- #
	plt.figure()
	plt.imshow(index, cmap="RdYlGn", vmin=-1, vmax=1)
	plt.colorbar()
	plt.savefig('{}/{}_-1_1.png'.format(save_dir, index_name),pad_inches=0)
	plt.close()

	# -- Plot index (min, max) -- #
	lower, upper = find_real_min_max(perc, edges, index_clear)
	print('Min: {}'.format(lower))
	print('Max: {}'.format(upper))
	plt.figure()
	plt.imshow(np.clip(index, lower, upper), cmap="RdYlGn")
	plt.colorbar()
	plt.savefig('{}/{}_min_max.png'.format(save_dir, index_name),pad_inches=0)
	plt.close()

	# -- Find Regions -- #
	thres = (lower + (upper + lower)/2)/2 # 25% range
	# thres = (lower + upper)/2    # 50% range
	# thres = filters.threshold_otsu(index_clear)
	print('Threshold value: {}'.format(thres))
	mask = threshold_index(index, thres)
	mask = (mask/255).astype(np.uint8)

	index_clear = index[~np.isnan(index)]
	# # mask = morphology.binary_opening(mask, np.ones((3,3)), iterations= 1).astype(np.uint8)
	# mask = ndimage.morphology.binary_opening(mask, np.ones((3,3)), iterations= 3).astype(np.uint8)
	# mask = ndimage.morphology.binary_closing(mask, np.ones((3,3)), iterations= 1).astype(np.uint8)
	# # mask = ndimage.morphology.binary_opening(mask, np.ones((3,3)), iterations= 1).astype(np.uint8)



	# mask = morphology.binary_opening(mask, np.ones((3,3)), iterations= 1).astype(np.uint8)


	mask = ndimage.morphology.binary_closing(mask, np.ones((5,5)), iterations= 1).astype(np.uint8)
	mask = ndimage.morphology.binary_opening(mask, np.ones((5,5)), iterations= 1).astype(np.uint8)

	# hat = morphology.white_tophat(mask, np.ones((9,9)))
	# mask = mask - hat
	# mask = ndimage.morphology.binary_dilation(mask, np.ones((5,5)), iterations= 1).astype(np.uint8)

	#

	# plt.figure()
	# plt.imshow(mask, cmap="gray")
	# plt.colorbar()
	# plt.savefig('{}/{}_areas.png'.format(save_dir, index_name),pad_inches=0)
	# plt.close()

	# -- Plot binary image -- #
	mask_white = np.copy(mask)
	mask_white[empty_space]=1
	f = plt.figure()
	print(f.get_dpi())
	f.set_figheight(index.shape[0]/f.get_dpi())
	f.set_figwidth(index.shape[1]/f.get_dpi())
	ax = plt.Axes(f, [0., 0., 1., 1.])
	ax.set_axis_off()
	f.add_axes(ax)
	ax.imshow(mask_white, cmap="gray", aspect='auto')
	f.savefig('{}/{}_areas.png'.format(save_dir, index_name))
	plt.close()

	# mask = morphology.binary_opening(mask, np.ones((3,3))).astype(np.uint8)
	# labels, nlabels = ndimage.label(mask, structure=np.ones((3,3)), background=0)
	labels, nlabels = measure.label(mask, connectivity=2, background=0, return_num=True)
	centers = ndimage.center_of_mass(mask, labels, np.arange(nlabels) + 1)
	centers = np.array(centers)

	_, num_pixels =  np.unique(labels, return_counts=True)


	# -- Plot labeled areas -- #
	f = plt.figure()
	print(f.get_dpi())
	f.set_figheight(index.shape[0]/f.get_dpi())
	f.set_figwidth(index.shape[1]/f.get_dpi())
	ax = plt.Axes(f, [0., 0., 1., 1.])
	ax.set_axis_off()
	f.add_axes(ax)
	ax.imshow(labels, cmap="nipy_spectral", aspect='auto')
	f.savefig('{}/{}_labeled_areas.png'.format(save_dir, index_name))
	plt.close()


	spot_size = np.sqrt(np.shape(index)[0]**2 + np.shape(index)[1]**2)
	# -- Plot all centers -- #
	f = plt.figure()
	print(f.get_dpi())
	f.set_figheight(index.shape[0]/f.get_dpi())
	f.set_figwidth(index.shape[1]/f.get_dpi())
	ax = plt.Axes(f, [0., 0., 1., 1.])
	ax.set_axis_off()
	f.add_axes(ax)
	aa = ax.imshow(np.clip(index, lower, upper), cmap="RdYlGn", aspect='auto')
	ax.scatter(centers[:,1], centers[:,0], s = 0.3*spot_size, c='cyan', edgecolors='black')
	# f.colorbar(aa)
	f.savefig('{}/{}_all_centers.png'.format(save_dir,index_name))



	print(np.shape(centers)[0])
	opt_K = find_optimal_K(centers, num_pixels)
	kmeans = KMeans(n_clusters=opt_K, random_state=0).fit(centers, sample_weight=num_pixels[1:])
	centers_cluster = kmeans.cluster_centers_

	f = plt.figure()
	print(f.get_dpi())
	f.set_figheight(index.shape[0]/f.get_dpi())
	f.set_figwidth(index.shape[1]/f.get_dpi())
	ax = plt.Axes(f, [0., 0., 1., 1.])
	ax.set_axis_off()
	f.add_axes(ax)
	ax.imshow(np.clip(index, lower, upper), cmap="RdYlGn", aspect='auto')
	ax.scatter(centers_cluster[:,1], centers_cluster[:,0], s = 0.5 * spot_size, c='dodgerblue', edgecolors='black', linewidth=5) #dodgerblue
	# f.colorbar()
	f.savefig('{}/{}_centers.png'.format(save_dir, index_name))
	plt.close()


	f = plt.figure()
	print(f.get_dpi())
	f.set_figheight(index.shape[0]/f.get_dpi())
	f.set_figwidth(index.shape[1]/f.get_dpi())
	ax = plt.Axes(f, [0., 0., 1., 1.])
	ax.set_axis_off()
	f.add_axes(ax)
	ax.imshow(np.clip(index, lower, upper), cmap="RdYlGn", aspect='auto')
	f.savefig('{}/{}.png'.format(save_dir, index_name))
	plt.close()


	print('Spot size: {}'.format(spot_size))



# img_path = '/home/mikrestenitis/Databases/Weedmap/orthophoto/000/composite-png/RGB.png'
# img_path = '/home/mikrestenitis/Databases/Weedmap/000/groundtruth/000_frame0021.png'
# img_path = '/home/mikrestenitis/Downloads/RGB.jpg'
# img_path = '/home/mikrestenitis/CoFly/Data/Sep_exp/atkap@12_09_2019_14_45_40/dji.phantom.4.pro.hawk.1/stitched_L1/001_3.jpg'
# img_path = '/home/mikrestenitis/Databases/Pix4D dataset/example_rostock_soda_rgb/images/EP-11-29590_0007_0136.JPG' #EP-11-29590_0007_0173.JPG' #
# img_path = '/home/mikrestenitis/CoFly/Indexes Inspection/img_007.jpg'
# img_path = '/home/mikrestenitis/CoFly/Indexes Inspection/certh_area.tif'
# img_path = '/home/mikrestenitis/Databases/Pix4D dataset/example_rostock_soda_rgb/area_1.jpg'
img_path = './real_life_exp/cropped_larisa_july.tif'

img_name = 'lofiskos_jul'
save_dir = './results/{}'.format(img_name)
os.makedirs(save_dir, exist_ok=True)


img_4ch = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
img = img_4ch[:, :, :3].astype(np.float)
img[img_4ch[:, :, 3] == 0] = np.nan
empty_space = img_4ch[:, :, 3] == 0

# img = cv2.imread('./mat_files/img_004/img_004.jpg')
# img = mask_empty_space(img)

print('Processing image wthi shape {} x {}'.format(img.shape[0], img.shape[1]))

# -- Calculate index -- #
# img = np.ma.masked_invalid(img)
Idx = Indexes(img)
index_names = ['vari', 'ngbdi'] #, 'gli', 'vndvi', 'ngbdi']

for index_name in index_names:
	index_analysis(Idx,index_name, empty_space)
