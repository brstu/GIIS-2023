import cv2 # работа с картинками
import functions # файл с функциями

from PyQt5 import uic, QtTest # интерфейс
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import random 
import sys 


global IMAGE_GLOBAL # наше изображение
IMAGE_GLOBAL = cv2.imread("image.jpg") #первоначальная загрузка изображения


class MainWindow(QDialog): # класс окна, тут описан его функционал
    def __init__(self):    # инициализация
        super(MainWindow, self).__init__()
        uic.loadUi("ui/MainWindow.ui", self)
        self.setWindowTitle("Пороговый филтр, лаба 1")
        self.show()
        #----------------- # поиск элементов и присвоение функционала
        self.textNoise = self.findChild(QLabel, "noise_text")
        self.textFilter = self.findChild(QLabel, "threshold_text")

        self.sliderNoise = self.findChild(QSlider, "noise_slider")
        self.sliderFilter = self.findChild(QSlider, "filter_slider")
        self.spinBox1 = self.findChild(QSpinBox, "spinbox1")
        self.spinBox2 = self.findChild(QSpinBox, "spinbox2")

        self.buttonLoad = self.findChild(QPushButton, "load_button")
        self.buttonNoise = self.findChild(QPushButton, "noise_button")
        self.buttonFilter = self.findChild(QPushButton, "filter_button")
        self.buttonImage = self.findChild(QPushButton, "show_button")

        self.progressBar = self.findChild(QProgressBar, "progressBar")
        #-----------------========
        self.buttonLoad.clicked.connect(self.loadImage)
        self.buttonNoise.clicked.connect(self.applyNoise)
        self.buttonFilter.clicked.connect(self.filterImage)
        self.buttonImage.clicked.connect(self.showImage)
        self.sliderNoise.valueChanged.connect(self.sliderNoiseTick)
        self.sliderFilter.valueChanged.connect(self.sliderFilterTick)
        #-----------------========

    def sliderNoiseTick(self): # действие при измененении значений слайдеров
        self.textNoise.setText("шум: "+str(self.sliderNoise.value()) + "%")
    def sliderFilterTick(self):
        self.textFilter.setText("порог: "+str(self.sliderFilter.value()))

    def loadImage(self): # загрузить картинку
        global IMAGE_GLOBAL
        path = QFileDialog.getOpenFileName()
        IMAGE_GLOBAL = cv2.imread(path[0])
        if(True): # если надо выводить по отдельности, то делаем своё окно
            functions.show_image(IMAGE_GLOBAL, "loaded")
        else:   # если нет то рисуем в общее
            functions.show_image(IMAGE_GLOBAL, "main window")


    def applyNoise(self): # применение шума
        global IMAGE_GLOBAL
        IMAGE_GLOBAL = functions.noise(IMAGE_GLOBAL, self.sliderNoise.value(), self.progressBar)
        if(False): 
            functions.show_image(IMAGE_GLOBAL, "noise applied")
        else:
            functions.show_image(IMAGE_GLOBAL, "main window")

    def filterImage(self): # фильтр
        global IMAGE_GLOBAL
        IMAGE_GLOBAL = functions.denoise(IMAGE_GLOBAL, self.sliderFilter.value(), self.spinBox1.value(), self.spinBox2.value(), self.progressBar)
        if(False): 
            functions.show_image(IMAGE_GLOBAL, "filtered")
        else:
            functions.show_image(IMAGE_GLOBAL, "main window")

    def showImage(self): # показать картинку
        if(False): 
            functions.show_image(IMAGE_GLOBAL, "results")
        else:
            functions.show_image(IMAGE_GLOBAL, "main window")

# так надо
app = QApplication(sys.argv)
launcher = MainWindow()
app.exec_()