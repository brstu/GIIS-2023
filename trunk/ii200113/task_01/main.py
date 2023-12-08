from PyQt6.QtWidgets import QApplication, QWidget, QProgressBar, QLabel, QPushButton, QFileDialog, QHBoxLayout, QSlider, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
import sys
import cv2
from model import Model
import threading

class ImageProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.load_button = QPushButton('Загрузить изображение', self)
        self.start_button = QPushButton('Старт', self)
        self.start_button.clicked.connect(self.start)
        self.load_button.clicked.connect(self.showDialog)
        self.selectedFilePath = None
        self.progressBar = QProgressBar()
        self.progressBar.setHidden(True)
        self.noise_layout = QGridLayout()
        self.noise_label = QLabel('Уровень шума', self)
        self.noise_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.noise_slider.setMinimum(0)
        self.noise_slider.setMaximum(10)
        self.noise_slider.setSingleStep(1)
        self.noise_value = QLabel('0', self)
        self.noise_slider.valueChanged.connect(self.noise_slider_value_changed)
        self.noise_layout.addWidget(self.noise_label, 0, 0)
        self.noise_layout.addWidget(self.noise_slider, 0, 1)
        self.noise_layout.addWidget(self.noise_value, 0, 2)
        self.threshold_layout = QHBoxLayout()
        self.threshold_label = QLabel('Порог', self)
        self.threshold_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(255)
        self.threshold_slider.setSingleStep(1)
        self.threshold_value = QLabel('0', self)
        self.threshold_slider.valueChanged.connect(self.threshold_slider_value_changed)
        self.threshold_layout.addWidget(self.threshold_label)
        self.threshold_layout.addWidget(self.threshold_slider)
        self.threshold_layout.addWidget(self.threshold_value)
        self.threshold_layout.addWidget(self.start_button)
        self.label_original = QLabel(self)
        self.label_noisy = QLabel(self)
        self.label_result = QLabel(self)
        self.image_original_layout = QGridLayout()
        self.image_original_layout.addWidget(self.load_button, 0, 0)
        self.image_original_layout.addWidget(self.label_original, 1, 0)
        self.image_noisy_layout = QGridLayout()
        self.image_noisy_layout.addLayout(self.noise_layout, 0, 0)
        self.image_noisy_layout.addWidget(self.label_noisy, 1, 0)
        self.image_result_layout = QGridLayout()
        self.image_result_layout.addLayout(self.threshold_layout, 0, 0)
        self.image_result_layout.addWidget(self.label_result, 1, 0)
        layout = QGridLayout()
        layout.addLayout(self.image_original_layout, 0, 0)
        layout.addLayout(self.image_noisy_layout, 0, 1)
        layout.addLayout(self.image_result_layout, 0, 2)
        layout.addWidget(self.progressBar, 1, 2)
        self.setLayout(layout)
        self.setWindowTitle('Фильтрация изображения')
        self.show()

    def showDialog(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Выбрать файл", "", "All Files (*);;Python Files (*.py)")
        if file_paths:
            self.noise_slider.setValue(0)
            self.threshold_slider.setValue(0)
            self.model =  Model(file_paths[0])
            image = self.model.original_image
            self.original_image = cv2.imread(self.selectedFilePath, cv2.IMREAD_GRAYSCALE)
            original_pixmap = QPixmap.fromImage(QImage(image, image.shape[1], image.shape[0], image.shape[1], QImage.Format.Format_Grayscale8))
            original_pixmap = original_pixmap.scaled(300, 200)
            self.label_original.setPixmap(original_pixmap)
            noisy_pixmap = QPixmap.fromImage(QImage(image, image.shape[1],image.shape[0], image.shape[1], QImage.Format.Format_Grayscale8))
            noisy_pixmap = noisy_pixmap.scaled(300, 200)
            self.label_noisy.setPixmap(noisy_pixmap)
            result_pixmap = QPixmap.fromImage(QImage(image, image.shape[1], image.shape[0], image.shape[1], QImage.Format.Format_Grayscale8))
            result_pixmap = result_pixmap.scaled(300, 200)
            self.label_result.setPixmap(result_pixmap)
            self.label_original.setScaledContents(True)
            self.label_noisy.setScaledContents(True)
            self.label_result.setScaledContents(True)
            self.original_image = cv2.imread(self.selectedFilePath, cv2.IMREAD_GRAYSCALE)

    def noise_slider_value_changed(self):
        value = self.noise_slider.value()
        self.noise_value.setText(str(value*10)+"%")
        value = value/5
        self.model.add_noisy(value)
        if self.model.noisy_image is not None:
            noisy_pixmap = QPixmap.fromImage(QImage(self.model.noisy_image,
            self.model.noisy_image.shape[1], self.model.noisy_image.shape[0],
            self.model.noisy_image.shape[1], QImage.Format.Format_Grayscale8))
            noisy_pixmap = noisy_pixmap.scaled(300, 200)
            self.label_noisy.setPixmap(noisy_pixmap)

    def start(self):
        value = self.threshold_slider.value()

        def run_operation():
            res = self.model.threshold_filter(value)
            if res is not None:
                result_pixmap = QPixmap.fromImage(QImage(res, res.shape[1], res.shape[0],res.shape[1], QImage.Format.Format_Grayscale8))
                result_pixmap = result_pixmap.scaled(300, 200)
                self.label_result.setPixmap(result_pixmap)
                self.progressBar.setHidden(True)
        operation_thread = threading.Thread(target=run_operation)
        operation_thread.start()
        self.progressBar.show()
        self.progressBar.setRange(0, 0)

    def threshold_slider_value_changed(self):
        value = self.threshold_slider.value()
        self.threshold_value.setText(str(value))


def main():
    app = QApplication(sys.argv)
    ex = ImageProcessor()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()