import cv2
import random

def show_img(image, window_name): # показать картинку
    cv2.imshow(window_name, image)

def give_noises(image):
    if image:
        return image
    else:
        return 1

def distract_noises(image, t, x_width, y_width):
    tmp = 0.1
    for x, row in enumerate(image):
        prog = x*100/len(image)

        if int(tmp) != int(prog):
            print(str(int(prog)) + "%")
        tmp = prog

        for y, _ in enumerate(row):
            avg_pixel, pixels_in_avg = check(image, x, y, x_width, y_width)
            avg_bright = (avg_pixel[0] + avg_pixel[1] + avg_pixel[2]) / (pixels_in_avg*3)
            avg_pixel = [avg_pixel[0]/(pixels_in_avg), avg_pixel[1]/(pixels_in_avg), avg_pixel[2]/(pixels_in_avg)]
            pixel_bright = (int(image[x][y][0]) + int(image[x][y][1]) + int(image[x][y][2])) / 3.0
            if (abs(pixel_bright-avg_bright)>t):
                image[x][y] = [int(avg_pixel[0]), int(avg_pixel[1]), int(avg_pixel[2])]
    print('100%')
    return image

def check(image, x, y, x_width, y_width):
    avg_pixel = [0,0,0]
    pixels_in_avg = 0
    for x_ in range(int(-1*x_width/2),int(x_width/2) + 1):
        for y_ in range(int(-1*y_width/2),int(y_width/2) + 1):
            if (x+x_>=0) and (y+y_>=0) and (x+x_<len(image)) and (y+y_<len(image[0])):
                pixels_in_avg+=1
                avg_pixel[0] += image[x+x_][y+y_][0]
                avg_pixel[1] += image[x+x_][y+y_][1]
                avg_pixel[2] += image[x+x_][y+y_][2]
    return avg_pixel, pixels_in_avg
