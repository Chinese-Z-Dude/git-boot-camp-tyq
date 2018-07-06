import numpy as np
from sklearn.cluster import KMeans
import cv2

K = [2, 6, 50]

# kmeans segmetation on img with cluster number k
def seg(img, k):

    # reshape the image into 2d array of pixel and channel
    reshaped = img.reshape(img.shape[0] * img.shape[1], img.shape[2])

    # performing the clustering of data points
    kmeans = KMeans(n_clusters = k, n_init = 40, max_iter = 500).fit(reshaped)

    # reshape the clustering result back to 2d array
    clustering = np.reshape(np.array(kmeans.labels_, dtype = np.uint8),
                            (img.shape[0], img.shape[1]))

    # regroup the data points by its label
    labels = sorted([n for n in range(k)],
                          key = lambda x: -np.sum(clustering == x))

    # reconstruct the picture with new color scheme
    newImg = np.zeros(img.shape[ : 2], dtype = np.uint8)
    for i, label in enumerate(labels):
        newImg[clustering == label] = int(255 / (k - 1)) * i

    # output new segmented picture
    cv2.imwrite(str(k) + "segmentation.png", newImg)

def main():
    image = cv2.imread("trees.png")
    # print image
    for k in K:
        seg(image, k)

if __name__ == "__main__":
    main()
