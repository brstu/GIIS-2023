import cv2
import random

def pokaz_photo(kartinka, window_name): 
    cv2.imshow(window_name, kartinka)

def shum(kartinka, level): # шум
    buffer = 0.1
    for x, stroka in enumerate(kartinka):

        pokazatel = x*100/len(kartinka)
        if int(buffer) != int(pokazatel):
            print(str(int(pokazatel))+"%")
        buffer = pokazatel
        for y, _ in enumerate(stroka):
            zarandomlennoe_v = random.randrange(1,5) 
            kartinka[x][y] = [zarandomlennoe_v*50,zarandomlennoe_v*50,zarandomlennoe_v*50]
    print('100%')
    return kartinka

def deshum(kartinka, threshold, oknox, oknoy):
    '''
    shum
    (image, porog, window size Х, window size У)
    go throw the every pixel (х, у)
    '''
    buffer = 0.1
    for x, stroka in enumerate(kartinka):
        pokazatel = x*100/len(kartinka)

        if int(buffer) != int(pokazatel):
            print(str(int(pokazatel)) + "%" )
        buffer = pokazatel

        for y, _ in enumerate(stroka):
            sredniy_pixel, pixels_in_average = check_pixels(kartinka, x, y, oknox, oknoy)
            sredniy_yarkost = (sredniy_pixel[0] + sredniy_pixel[1] + sredniy_pixel[2]) / (pixels_in_average*3)
            sredniy_pixel = [sredniy_pixel[0]/(pixels_in_average), sredniy_pixel[1]/(pixels_in_average), sredniy_pixel[2]/(pixels_in_average)]
            pixel_brightness = (int(kartinka[x][y][0]) + int(kartinka[x][y][1]) + int(kartinka[x][y][2])) / 3.0
            if (abs(pixel_brightness-sredniy_yarkost)>threshold):
                kartinka[x][y] = [int(sredniy_pixel[0]),int(sredniy_pixel[1]),int(sredniy_pixel[2])]
    print ('100%')
    return kartinka

def check_pixels(kartinka, x, y, oknox, oknoy):
    sredniy_pixel = [0,0,0]
    pixels_in_average = 0
    for x_ in range(int(-1*oknox/2),int(oknox/2) + 1):
        for y_ in range(int(-1*oknoy/2),int(oknoy/2) + 1):
            if (x+x_>=0) and (y+y_>=0) and (x+x_<len(kartinka)) and (y+y_<len(kartinka[0])):
                pixels_in_average+=1
                sredniy_pixel[0] += kartinka[x+x_][y+y_][0]
                sredniy_pixel[1] += kartinka[x+x_][y+y_][1]
                sredniy_pixel[2] += kartinka[x+x_][y+y_][2]
    return sredniy_pixel, pixels_in_average
