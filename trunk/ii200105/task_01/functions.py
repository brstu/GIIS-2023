import cv2
import random

def show_image(image, window_name): # показать картинку
    cv2.imshow(window_name, image)

def noise(image, level): # шум
    buff = 0.1
    # проходимся по каждому пикселю (x,y) и если рандомом выпадет единица то зарисовываем оттенком серого
    for x, row in enumerate(image):

        progress = x*100/len(image)
        if int(buff) != int(progress):
            print(str(int(progress))+"%")
        buff = progress
        for y, _ in enumerate(row):
            if(random.randrange(0,(102-level)) == 1):
                '''
                если выпала единица (а шанс меняем с помощью level, который берется со слайдера)
                чем больше рейндж, тем меньше шанс единицы
                '''
                random_v = random.randrange(1,5) #чем больше здесь выпало тем ярче пиксель
                image[x][y] = [random_v*50,random_v*50,random_v*50]
    print('100%')
    return image

def denoise(image, threshold, windowx, windowy):
    '''
    шум
    (картинка, порог, размер окна Х, размер окна У)
    идём по каждому пикселю в (х, у)
    '''
    buff = 0.1
    for x, row in enumerate(image):
        progress = x*100/len(image)

        if int(buff) != int(progress):
            print(str(int(progress)) + "%" )
        buff = progress

        for y, _ in enumerate(row):
            # в это время для каждого пикселя смотрим соседей на расстоянии (размер окна \ 2)
            average_pixel, pixels_in_average = check_pixels(image, x, y, windowx, windowy)
            
            # для всех соседей включая сам пиксель находим среднюю яркость
            average_brightness = (average_pixel[0] + average_pixel[1] + average_pixel[2]) / (pixels_in_average*3)
            average_pixel = [average_pixel[0]/(pixels_in_average), average_pixel[1]/(pixels_in_average), average_pixel[2]/(pixels_in_average)]
            pixel_brightness = (int(image[x][y][0]) + int(image[x][y][1]) + int(image[x][y][2])) / 3.0
            # если пиксель ярче средней яркости соседей, то
            if (abs(pixel_brightness-average_brightness)>threshold):
                # то пиксель приравниваем к средней яркости
                image[x][y] = [int(average_pixel[0]),int(average_pixel[1]),int(average_pixel[2])]
    print ('100%')
    return image

def check_pixels(image, x, y, windowx, windowy):
    average_pixel = [0,0,0]
    pixels_in_average = 0
    for x_ in range(int(-1*windowx/2),int(windowx/2) + 1):
        for y_ in range(int(-1*windowy/2),int(windowy/2) + 1):
            if (x+x_>=0) and (y+y_>=0) and (x+x_<len(image)) and (y+y_<len(image[0])):
                pixels_in_average+=1
                average_pixel[0] += image[x+x_][y+y_][0]
                average_pixel[1] += image[x+x_][y+y_][1]
                average_pixel[2] += image[x+x_][y+y_][2]
    return average_pixel, pixels_in_average
