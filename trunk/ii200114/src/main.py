from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import sys
from functions import Functions  # Assuming you have a 'functions.py' file with a 'Functions' class

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("ui/MainWindow.ui", self)
        self.setWindowTitle("Пороговый филтр, лаба 1")
        self.show()

        self.functions = Functions()  # Create an instance of the Functions class

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

        self.buttonLoad.clicked.connect(self.loadImage)
        self.buttonNoise.clicked.connect(self.applyNoise)
        self.buttonFilter.clicked.connect(self.filterImage)
        self.buttonImage.clicked.connect(self.showImage)
        self.sliderNoise.valueChanged.connect(self.sliderNoiseTick)
        self.sliderFilter.valueChanged.connect(self.sliderFilterTick)

    def sliderNoiseTick(self):
        self.textNoise.setText("шум: " + str(self.sliderNoise.value()) + "%")

    def sliderFilterTick(self):
        self.textFilter.setText("порог: " + str(self.sliderFilter.value()))

    def loadImage(self):
        path, _ = QFileDialog.getOpenFileName()
        if path:
            self.image = cv2.imread(path)
            self.functions.show_image(self.image, "loaded")

    def applyNoise(self):
        if hasattr(self, 'image'):
            self.image = self.functions.noise(self.image, self.sliderNoise.value(), self.progressBar)
            self.functions.show_image(self.image, "noise applied")

    def filterImage(self):
        if hasattr(self, 'image'):
            self.image = self.functions.denoise(self.image, self.sliderFilter.value(), self.spinBox1.value(),
                                                self.spinBox2.value(), self.progressBar)
            self.functions.show_image(self.image, "filtered")

    def showImage(self):
        if hasattr(self, 'image'):
            self.functions.show_image(self.image, "results")

app = QApplication(sys.argv)
launcher = MainWindow()
sys.exit(app.exec_())
