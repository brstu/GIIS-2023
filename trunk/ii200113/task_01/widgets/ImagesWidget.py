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

        self._label_setter = QLabel()
        self._label_setter.setStyleSheet('color: black;')
        self._label_setter.setText("Noised image")
        self._unnoised_label_setter = QLabel()
        self._unnoised_label_setter.setStyleSheet('color: black;')
        self._unnoised_label_setter.setText("Unnoised image")

        self._layout.addWidget(self._label_setter, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._unnoised_label_setter, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._layout)

    def set_noised_image_usable(self, path):
        self._image_usable = QPixmap(path)
        self._label_setter.setPixmap(self._image_usable)

    def set_unnoised_image_usable(self):
        self._unnoised_image_usable = QPixmap('images/unnoised_image_usable.png')
        self._unnoised_label_setter.setPixmap(self._unnoised_image_usable)