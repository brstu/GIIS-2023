import cv2
import numpy as np
class Model:
    def __init__(self, path):
        self.original_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        self.noisy_image = None

    def add_noisy(self,sigma, mean=0):
        generator = np.random.default_rng(42)
        noise = generator.standard_normal(mean, sigma, self.original_image.shape)
        self.noisy_image = cv2.add(self.original_image, noise)
    def threshold_filter(self, threshold):
        if self.noisy_image is not None:
            height, width = self.noisy_image.shape
            image = np.zeros((height+2, width+2), dtype=np.uint8)
            image[1:height+1, 1:width+1] = self.noisy_image.copy()
            res_image = image.copy()
            for i in range(1, height+1):
                for j in range(1, width+1):
                    block = image[i-1:i+2, j-1:j+2]
                    pixel = block[1, 1]
                    summa = (block.sum()-pixel)/8

                    if pixel-summa > threshold:
                        res_image[i, j] = summa
                    else:
                        res_image[i, j] = pixel

            return res_image
        else:
            return None