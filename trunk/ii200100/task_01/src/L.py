import sys, random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout, QCheckBox, QInputDialog
from PyQt5.QtGui import QPixmap, QImageReader, QImage, QPainter, QColor, QPen, QIcon
from PyQt5.QtCore import Qt

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowIcon(QIcon("ICO.ico"))

        self.initLabels()
        self.initButtons()

        self.clean_image = None
        self.noisy_image = None
        self.filter_image = None

    def initLabels(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.clean_label = QLabel(self.central_widget)
        self.noisy_label = QLabel(self.central_widget)
        self.filter_label = QLabel(self.central_widget)

        self.layout.addWidget(self.clean_label)
        self.layout.addWidget(self.noisy_label)
        self.layout.addWidget(self.filter_label)

    def initButtons(self):
        open_button = QPushButton("Open Image", self.central_widget)
        noise_button = QPushButton("Add Salt and Pepper Noise", self.central_widget)
        lines_button = QPushButton("Add Lines", self.central_widget)
        reset_button = QPushButton("Reset Noise", self.central_widget)
        filter_button = QPushButton("Filter Noise", self.central_widget)
        refilter_button = QPushButton("ReFilter Noise", self.central_widget)

        open_button.clicked.connect(self.openImage)
        noise_button.clicked.connect(self.addSaltAndPepperNoise)
        lines_button.clicked.connect(self.addLineNoise)
        reset_button.clicked.connect(self.reset)
        filter_button.clicked.connect(self.filter)
        refilter_button.clicked.connect(self.refilter)

        button_layout = QVBoxLayout()
        button_layout.addWidget(open_button)
        button_layout.addWidget(noise_button)
        button_layout.addWidget(lines_button)
        button_layout.addWidget(reset_button)
        button_layout.addWidget(filter_button)
        button_layout.addWidget(refilter_button)

        checkbox_layout = QHBoxLayout()
        self.row = QCheckBox("Rows", self.central_widget)
        self.column = QCheckBox("Columns", self.central_widget)
        checkbox_layout.addWidget(self.row)
        checkbox_layout.addWidget(self.column)

        button_layout.addLayout(checkbox_layout)
        self.layout.addLayout(button_layout)

    def openImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_name:
            image_reader = QImageReader(file_name)
            image_reader.setAutoTransform(True)
            image = image_reader.read()

            # Convert the image to grayscale
            grayscale_image = image.convertToFormat(QImage.Format_Grayscale8)

            clean_pixmap = QPixmap.fromImage(grayscale_image)
            self.clean_image = clean_pixmap.scaled(self.clean_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.clean_label.setPixmap(self.clean_image)

    def addSaltAndPepperNoise(self):
        if self.noisy_image is not None:
            img = self.noisy_image.toImage()
        elif self.clean_image is not None:
            img = self.clean_image.toImage()
        else:
            return
        img = self.addSnPN(img)

        self.noisy_image = QPixmap.fromImage(img)
        self.noisy_label.setPixmap(self.noisy_image)

    def addSnPN(self, img):
        width = img.width()
        height = img.height()

        for _ in range(1000):  # Add noise to 1000 random points
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            img.setPixelColor(x, y, QColor(0, 0, 0) if random.random() < 0.5 else QColor(255, 255, 255))

        return img

    def addLineNoise(self):
        if self.noisy_image is not None:
            img = self.noisy_image.toImage()
        elif self.clean_image is not None:
            img = self.clean_image.toImage()
        else:
            return

        img = self.addLines(img)

        self.noisy_image = QPixmap.fromImage(img)
        self.noisy_label.setPixmap(self.noisy_image)

    def addLines(self, img):
        width = img.width()
        height = img.height()
        for _ in range(10):  # Add noise to 10 random lines
            x1 = random.randint(0, width - 1)
            y1 = random.randint(0, height - 1)
            x2 = random.randint(0, width - 1)
            y2 = random.randint(0, height - 1)
            color = QColor(0, 0, 0) if random.random() < 0.5 else QColor(255, 255, 255)
            pen = QPen(color)
            painter = QPainter(img)
            painter.setPen(pen)
            painter.drawLine(x1, y1, x2, y2)
            painter.end()
        return img

    def reset(self):
        self.noisy_image = None
        self.noisy_label.clear()

    def filter(self):
        qimg = QImage(self.noisy_image)
        img = qimg.convertToFormat(QImage.Format_Grayscale8)
        width = img.width()
        height = img.height()
        new_image = QImage(width, height, QImage.Format_Grayscale8)
        N, _ = QInputDialog.getInt(self, "N?", "Enter:")
        if N < 3:
            return
        if N % 2 == 0:
            N -= 1
        # do filter here
        for x in range(width):
            for y in range(height):
                # get grey scale QColor(img.pixel(x, y)).lightness()
                pixel = QColor(img.pixel(x, y)).lightness()
                if pixel == 0 or pixel == 255:
                    pixels = []
                    if self.row.isChecked():
                        # do h
                        pixels.extend(self.getkernelH(img, N, y, x, width))
                    if self.column.isChecked():
                        # do v
                        pixels.extend(self.getkernelV(img, N, x, y, height))
                    if self.row.isChecked() or self.column.isChecked():
                        median = self.get_median(pixels)
                        pixel = median
                new_image.setPixelColor(x, y, QColor(pixel, pixel, pixel))
        self.filter_image = new_image
        self.filter_label.setPixmap(QPixmap.fromImage(new_image))

    def refilter(self):
        qimg = QImage(self.filter_image)
        img = qimg.convertToFormat(QImage.Format_Grayscale8)
        width = img.width()
        height = img.height()
        new_image = QImage(width, height, QImage.Format_Grayscale8)
        N, _ = QInputDialog.getInt(self, "N?", "Enter:")
        if N < 3:
            return
        if N % 2 == 0:
            N -= 1
        # do filter here
        for x in range(width):
            for y in range(height):
                # get grey scale QColor(img.pixel(x, y)).lightness()
                pixel = QColor(img.pixel(x, y)).lightness()
                if pixel == 0 or pixel == 255:
                    pixels = []
                    if self.row.isChecked():
                        # do h
                        pixels.extend(self.getkernelH(img, N, y, x, width))
                    if self.column.isChecked():
                        # do v
                        pixels.extend(self.getkernelV(img, N, x, y, height))
                    median = self.get_median(pixels)
                    pixel = median
                new_image.setPixelColor(x, y, QColor(pixel, pixel, pixel))
        self.filter_image = new_image
        self.filter_label.setPixmap(QPixmap.fromImage(new_image))

    def getkernelH(self, img, N, y, x, width):
        n = 1
        pixels = []
        N -= 1
        while not N == 0:
            if x + n < width - 1:
                pixels.append(QColor(img.pixel(x + n, y)).lightness())
                N -= 1
            if x - n > -1:
                pixels.append(QColor(img.pixel(x - n, y)).lightness())
                N -= 1
            n += 1
        return pixels

    def getkernelV(self, img, N, x, y, height):
        n = 1
        pixels = []
        N -= 1
        while not N == 0:
            if y + n  < height - 1:
                pixels.append(QColor(img.pixel(x, y + n)).lightness())
                N -= 1
            if y - n  > -1:
                pixels.append(QColor(img.pixel(x, y - n)).lightness())
                N -= 1
            n += 1
        return pixels

    def get_median(self, lst):
        sorted_lst = sorted(lst)
        mid1 = sorted_lst[len(sorted_lst) // 2]
        mid2 = sorted_lst[len(sorted_lst) // 2 - 1]
        median = (mid1 + mid2) / 2
        return int(median)
 

def main():
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
