from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class ImagesWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(
            '''
                border: 2px solid black;
            '''
        )
        self._layout = QHBoxLayout()

        self._label = QLabel()
        self._label.setStyleSheet('color: black;')
        self._label.setText("Noised image")
        self._unnoised_label = QLabel()
        self._unnoised_label.setStyleSheet('color: black;')
        self._unnoised_label.setText("Unnoised image")

        self._layout.addWidget(self._label, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._unnoised_label, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._layout)

    def set_noised_image(self, path):
        self._image = QPixmap(path)
        self._label.setPixmap(self._image)

    def set_unnoised_image(self):
        self._unnoised_image = QPixmap('images/unnoised_image.png')
        self._unnoised_label.setPixmap(self._unnoised_image)