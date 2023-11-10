import cv2
import random

def pokaz_photo(kartinka, window_name): # показать картинку
    cv2.imshow(window_name, kartinka)

def shum(kartinka, level): # шум
    buffer = 0.1
    # проходимся по каждому пикселю (x,y) и если рандомом выпадет единица то зарисовываем оттенком серого
    for x, row in enumerate(kartinka):

        pokazatel = x*100/len(kartinka)
        if int(buffer) != int(pokazatel):
            print(str(int(pokazatel))+"%")
        buffer = pokazatel
        for y, _ in enumerate(row):
            # если выпала единица (а шанс меняем с помощью level, который берется со слайдера)
            if (random.randint(0,(102-level)) == 1):
                # чем больше рейндж, тем меньше шанс единицы
                random_v = random.randrange(1,5) #чем больше здесь выпало тем ярче пиксель
                kartinka[x][y] = [random_v*50,random_v*50,random_v*50]
    print('100%')
    return kartinka

def deshum(kartinka, threshold, oknox, oknoy):
    '''
    шум
    (картинка, порог, размер окна Х, размер окна У)
    идём по каждому пикселю в (х, у)
    '''
    buffer = 0.1
    for x, row in enumerate(kartinka):
        pokazatel = x*100/len(kartinka)

        if int(buffer) != int(pokazatel):
            print(str(int(pokazatel)) + "%" )
        buffer = pokazatel

        for y, _ in enumerate(row):
            # в это время для каждого пикселя смотрим соседей на расстоянии (размер окна \ 2)
            sredniy_pixel, pixels_in_average = check_pixels(kartinka, x, y, oknox, oknoy)
            # для всех соседей включая сам пиксель находим среднюю яркость
            sredniy_yarkost = (sredniy_pixel[0] + sredniy_pixel[1] + sredniy_pixel[2]) / (pixels_in_average*3)
            sredniy_pixel = [sredniy_pixel[0]/(pixels_in_average), sredniy_pixel[1]/(pixels_in_average), sredniy_pixel[2]/(pixels_in_average)]
            pixel_brightness = (int(kartinka[x][y][0]) + int(kartinka[x][y][1]) + int(kartinka[x][y][2])) / 3.0
            # если пиксель ярче средней яркости соседей, то
            if (abs(pixel_brightness-sredniy_yarkost)>threshold):
                # то пиксель приравниваем к средней яркости
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
