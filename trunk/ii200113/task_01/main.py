import cv2 
import functions 
from PyQt5 import uic 
from PyQt5.QtWidgets import (
    QLabel, QSlider, QSpinBox, QPushButton, QDialog, QFileDialog, QApplication
)
import sys

class GlavnoeOkno(QDialog): 
    def __init__(self):    
        super(GlavnoeOkno, self).__init__()
        uic.loadUi("ui/GlavnoeOkno.ui", self)
        self.setWindowTitle("Пороговый филтр, лаба 1")
        self.show()

<<<<<<< HEAD
        self.image = cv2.imread("image/kartinka.png")
=======
        self.image = cv2.imread("image/kartinka.jpg")
>>>>>>> 324f7f90673bbd9be7a30b094ad258e8126aeb9f
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
        self.buttonLoad.clicked.connect(self.zagruzkaKartinki)
        self.buttonshum.clicked.connect(self.applyshum)
        self.buttonFilter.clicked.connect(self.otfiltrovatKartinku)
        self.knopkaKartinki.clicked.connect(self.showImage)
        self.slidershum.valueChanged.connect(self.slidershumTick)
        self.sliderChangeFilter.valueChanged.connect(self.sliderChangeFilterTick)

    def slidershumTick(self): 
        self.textshum.setText("shum: "+str(self.slidershum.value()) + "%")

    def sliderChangeFilterTick(self):
        self.textFilter.setText("porog: "+str(self.sliderChangeFilter.value()))

    def zagruzkaKartinki(self): 
        path = QFileDialog.getOpenFileName()
        self.image = cv2.imread(path[0])

        self.showImage()


    def applyshum(self): 
        self.image = functions.shum(self.image)
        self.showImage()

    def otfiltrovatKartinku(self):
        self.image = functions.deshum(self.image, self.sliderChangeFilter.value(), self.spinBox1.value(), self.spinBox2.value())
        self.showImage()

    def showImage(self, wndout = False): 
        if (wndout):
            functions.pokaz_photo(self.image, "результаты")
        else:
            functions.pokaz_photo(self.image, "главное окно")


if __name__ == '__main__':
    application = QApplication(sys.argv)
    zapusk = GlavnoeOkno()
    application.exec_()
