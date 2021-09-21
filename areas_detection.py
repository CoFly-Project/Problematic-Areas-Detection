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
    # -- Mask nan Values -- #
    index_clear = index[~np.isnan(index)]
    lower = np.min(index_clear)
    upper = np.max(index_clear)
    empty_space = index != index

    # -- Find Regions -- #
    thres = (lower + (upper + lower) / 2) / 2  # 25% range
    print('Threshold value: {}'.format(thres))
    mask = threshold_index(index, thres)
    mask = (mask / 255).astype(np.uint8)

    mask = ndimage.morphology.binary_closing(mask, np.ones((5, 5)), iterations=1).astype(np.uint8)
    mask = ndimage.morphology.binary_opening(mask, np.ones((5, 5)), iterations=1).astype(np.uint8)

    # -- Create binary image -- #
    mask_white = np.copy(mask)
    mask_white[empty_space] = 1

    # -- Find centers of all areas -- #
    labels, nlabels = measure.label(mask, connectivity=2, background=0, return_num=True)
    centers = ndimage.center_of_mass(mask, labels, np.arange(nlabels) + 1)
    centers = np.array(centers)

    _, num_pixels = np.unique(labels, return_counts=True)

    # -- Cluster centers -- #
    opt_K = find_optimal_K(centers, num_pixels)
    kmeans = KMeans(n_clusters=opt_K, random_state=0).fit(centers, sample_weight=num_pixels[1:])
    centers_cluster = kmeans.cluster_centers_

    # -- Plot (for tesing reasons) -- #
    spot_size = np.sqrt(np.shape(index)[0] ** 2 + np.shape(index)[1] ** 2)
    f = plt.figure()
    f.set_figheight(index.shape[0] / f.get_dpi())
    f.set_figwidth(index.shape[1] / f.get_dpi())
    ax = plt.Axes(f, [0., 0., 1., 1.])
    ax.set_axis_off()
    f.add_axes(ax)
    ax.imshow(np.clip(index, lower, upper), cmap="RdYlGn", aspect='auto')
    ax.scatter(centers_cluster[:, 1], centers_cluster[:, 0], s=0.5 * spot_size, c='dodgerblue', edgecolors='black',
               linewidth=5)  # dodgerblue
    # f.colorbar()
    f.savefig('{}/{}_centers.png'.format(save_dir, index_name))
    plt.close()

    return centers_cluster


img_name = 'larisa_jul'
input_dir = './output/{}'.format(img_name)
save_dir = './output/{}'.format(img_name)
os.makedirs(save_dir, exist_ok=True)

index_names = ['vari', 'ngbdi']  # , 'gli', 'vndvi', 'ngbdi']

for index_name in index_names:
    index = np.load(os.path.join(input_dir, index_name + '_clipped.npy'))
    centers_cluster = find_areas(index)


