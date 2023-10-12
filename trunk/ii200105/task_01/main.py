import cv2 # работа с картинками
import functions # файл с функциями

from PyQt5 import uic # интерфейс
from PyQt5.QtWidgets import (
    QLabel, QSlider, QSpinBox, QPushButton, QDialog, QFileDialog, QApplication
)
import sys


class MainWindow(QDialog): # класс окна, тут описан его функционал
    def __init__(self):    # инициализация
        super(MainWindow, self).__init__()
        uic.loadUi("ui/MainWindow.ui", self)
        self.setWindowTitle("Пороговый филтр, лаба 1")
        self.show()

        self.image = cv2.imread("image/image.jpg")
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
        path = QFileDialog.getOpenFileName()
        self.image = cv2.imread(path[0])

        self.showImage()


    def applyNoise(self): # применение шума
        self.image = functions.noise(self.image, self.sliderNoise.value())
        self.showImage()

    def filterImage(self): # фильтр
        self.image = functions.denoise(self.image, self.sliderFilter.value(), self.spinBox1.value(), self.spinBox2.value())
        self.showImage()

    def showImage(self, wndout = False): # показать картинку
        if (wndout):
            functions.show_image(self.image, "results")
        else:
            functions.show_image(self.image, "main window")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = MainWindow()
    app.exec_()
