import cv2 # работа с картинками
import functions # файл с функциями

from PyQt5 import uic # интерфейс
from PyQt5.QtWidgets import (
    QLabel, QSlider, QSpinBox, QPushButton, QDialog, QFileDialog, QApplication
)
import sys


class GlavnoeOkno(QDialog): # класс окна, тут описан его функционал
    def __init__(self):    # инициализация
        super(GlavnoeOkno, self).__init__()
        uic.loadUi("ui/GlavnoeOkno.ui", self)
        self.setWindowTitle("Пороговый филтр, лаба 1")
        self.show()

        self.image = cv2.imread("image/kartinka.jpg")
        #----------------- # поиск элементов и присвоение функционала
        self.textshum = self.findChild(QLabel, "shum_text")
        self.textFilter = self.findChild(QLabel, "threshold_text")

        self.slidershum = self.findChild(QSlider, "shum_slider")
        self.sliderChangeFilter = self.findChild(QSlider, "filter_slider")
        self.spinBox1 = self.findChild(QSpinBox, "spinbox1")
        self.spinBox2 = self.findChild(QSpinBox, "spinbox2")

        self.buttonLoad = self.findChild(QPushButton, "load_button")
        self.buttonshum = self.findChild(QPushButton, "shum_button")
        self.buttonFilter = self.findChild(QPushButton, "filter_button")
        self.knopkaKartinki = self.findChild(QPushButton, "show_button")
        #-----------------========
        self.buttonLoad.clicked.connect(self.zagruzkaKartinki)
        self.buttonshum.clicked.connect(self.applyshum)
        self.buttonFilter.clicked.connect(self.otfiltrovatKartinku)
        self.knopkaKartinki.clicked.connect(self.showImage)
        self.slidershum.valueChanged.connect(self.slidershumTick)
        self.sliderChangeFilter.valueChanged.connect(self.sliderChangeFilterTick)
        #-----------------========

    def slidershumTick(self): # действие при измененении значений слайдеров
        self.textshum.setText("шум: "+str(self.slidershum.value()) + "%")

    def sliderChangeFilterTick(self):
        self.textFilter.setText("порог: "+str(self.sliderChangeFilter.value()))

    def zagruzkaKartinki(self): # загрузить картинку
        path = QFileDialog.getOpenFileName()
        self.image = cv2.imread(path[0])

        self.showImage()


    def applyshum(self): # применение шума
        self.image = functions.shum(self.image, self.slidershum.value())
        self.showImage()

    def otfiltrovatKartinku(self): # фильтр
        self.image = functions.deshum(self.image, self.sliderChangeFilter.value(), self.spinBox1.value(), self.spinBox2.value())
        self.showImage()

    def showImage(self, wndout = False): # показать картинку
        if (wndout):
            functions.pokaz_photo(self.image, "results")
        else:
            functions.pokaz_photo(self.image, "main window")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = GlavnoeOkno()
    app.exec_()
