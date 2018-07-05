import numpy as np
from sklearn.cluster import KMeans
import cv2

K = [3, 4, 5]

def seg(img):
    reshaped = img.reshape(img.shape[0] * img.shape[1], img.shape[2])
    kmeans = KMeans(n_clusters = 5, n_init = 40, max_iter = 500).fit(reshaped)
    clustering = np.reshape(np.array(kmeans.labels_, dtype = np.uint8),
                            (img.shape[0], img.shape[1]))
    sortedLabels = sorted([n for n in range(5)],
                          key = lambda x: -np.sum(clustering == x))
    newImg = np.zeros(img.shape[ : 2], dtype = np.uint8)
    for i, label in enumerate(sortedLabels):
        newImg[clustering == label] = int(255 / 5 - 1) * i
        
    cv2.imwrite("segmentation.png", newImg)

def main():
    image = cv2.imread("trees.png")
    # print image
    seg(image)

if __name__ == "__main__":
    main()
