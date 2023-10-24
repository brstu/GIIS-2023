import cv2
import functions

from PyQt5 import uic
from PyQt5.QtWidgets import (
    QLabel, QSlider, QSpinBox, QPushButton, QDialog, QFileDialog, QApplication
)
import sys


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("ui/MainWindow.ui", self)
        self.setWindowTitle("Пороговый филтр, лаба 1")
        self.show()

        self.image = cv2.imread("image/image.jpg")
        self.txtNoise = self.findChild(QLabel, "noise_text")
        self.txtFilter = self.findChild(QLabel, "threshold_text")

        self.slNoise = self.findChild(QSlider, "noise_slider")
        self.slFilter = self.findChild(QSlider, "filter_slider")
        self.spinBox1 = self.findChild(QSpinBox, "spinbox1")
        self.spinBox2 = self.findChild(QSpinBox, "spinbox2")

        self.btnLoad = self.findChild(QPushButton, "load_button")
        self.btnNoise = self.findChild(QPushButton, "noise_button")
        self.btnFilter = self.findChild(QPushButton, "filter_button")
        self.btnImage = self.findChild(QPushButton, "show_button")
        #-----------------========
        self.btnLoad.clicked.connect(self.loadImg)
        self.btnNoise.clicked.connect(self.approveNoise)
        self.btnFilter.clicked.connect(self.filterImg)
        self.btnImage.clicked.connect(self.showImg)
        self.slNoise.valueChanged.connect(self.noisesTick)
        self.slFilter.valueChanged.connect(self.filterTick)
        #-----------------========

    def noisesTick(self):
        self.txtNoise.setText("шум: "+str(self.slNoise.value()) + "%")

    def filterTick(self):
        self.txtFilter.setText("порог: "+str(self.slFilter.value()))

    def loadImg(self):
        path = QFileDialog.getOpenFileName()
        self.image = cv2.imread(path[0])

        self.showImg()


    def approveNoise(self):
        self.image = functions.give_noises(self.image)
        self.showImg()

    def filterImg(self):
        self.image = functions.distract_noises(self.image, self.slFilter.value(), self.spinBox1.value(), self.spinBox2.value())
        self.showImg()

    def showImg(self, wndout = False): # показать картинку
        if (wndout):
            functions.show_img(self.image, "results")
        else:
            functions.show_img(self.image, "main window")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = MainWindow()
    app.exec_()
