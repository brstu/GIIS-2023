import cv2
import numpy as np
from tkinter import Tk, Label, Scale, Button


def apply_filter(image, threshold):
    noise = np.zeros(image.shape, np.uint8)
    cv2.randn(noise, 0, 10)
    # Добавление шумов к картинке
    noisy_img = cv2.add(image, noise)
    cv2.imshow('noisy image', noisy_img)
    filtered_image = np.copy(noisy_img)
    for i in range(1, image.shape[0]-1):
        for j in range(1, image.shape[1]-1):
            window = image[i-1:i+2, j-1:j+2]
            median = np.median(window)
            if abs(image[i, j] - median) > int(threshold):
                filtered_image[i, j] = median
    return filtered_image


def update_threshold(value):
    threshold = value


def apply_and_show():
    filtered_image = apply_filter(original_image, threshold)
    cv2.imshow('orig image', original_image)
    cv2.imshow('Filtered Image', filtered_image)


# Load the image
original_image = cv2.imread('mama.jpg', 0)

# Create a window with a slider for threshold value
root = Tk()
root.title('Impulse Noise Filter')

label = Label(root, text="Threshold:")
label.pack()

scale = Scale(root, from_=0, to=255, orient='horizontal', length=300, command=update_threshold)
scale.set(20)
scale.pack()

button = Button(root, text="Apply Filter", command=apply_and_show)
button.pack()

# Initialize the threshold value
threshold = 20

root.mainloop()
cv2.waitKey(0)
cv2.destroyAllWindows()