from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QRadioButton,
    QSlider,
    QFileDialog,
    QLabel,
    QProgressBar
)
from PyQt5.QtCore import Qt, QVariantAnimation
from PyQt5.QtGui import QPixmap, QTransform
from widgets.ImagesWidget import ImagesWidget
from helpers.ImageHelper import ImageHelper
from PIL import Image

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self._image_helper = ImageHelper()
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("Remove image's noise")
        self.setStyleSheet(
            '''
                background-color: white;
            '''
        )
        self.setGeometry(50, 50, 1300, 700)

        self._layout = QVBoxLayout()

        self._buttons_widget = QWidget()
        self._buttons_layout = QHBoxLayout()

        self._open_file_button = self._create_button('Open file', self._open_file_button_tapped)
        self._buttons_layout.addWidget(self._open_file_button, 1)
        self._remove_noise_button = self._create_button('Remove noise', self._remove_noise_button_tapped)
        self._buttons_layout.addWidget(self._remove_noise_button, 1)
        self._create_noise_button = self._create_button('Create noise button', self._create_noise_button_tapped)
        self._buttons_layout.addWidget(self._create_noise_button, 1)

        self._buttons_widget.setLayout(self._buttons_layout)

        self._images_widget = ImagesWidget()

        self._radio_widget = QWidget()
        self._radio_widget_layout = QHBoxLayout()

        self._h_kernel_button = self._create_radio_button('Horizontal axis', 'horizontal')
        self._v_kernel_button = self._create_radio_button('Vertical axis', 'vertical')
        self._both_axises_button = self._create_radio_button('Both', 'both', is_checked=True)

        self._radio_widget_layout.addWidget(self._h_kernel_button, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self._radio_widget_layout.addWidget(self._v_kernel_button, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self._radio_widget_layout.addWidget(self._both_axises_button, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self._radio_widget.setLayout(self._radio_widget_layout)

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setRange(1, 20)
        self._slider.valueChanged.connect(self._slider_value_changed)
        self._slider.setStyleSheet(
            '''
                background-color: gray;
            '''
        )

        self._progress_bar = QProgressBar(self, minimum=0, maximum=100, textVisible=False,objectName="GreenProgressBar")
        self._progress_bar.setValue(20)
        self._progress_bar.setStyleSheet(
            '''
                background-color: black;
                height: 100px;
            '''
        )

        self._layout.addWidget(self._images_widget, 6)
        self._layout.addWidget(self._radio_widget, 1)
        self._label1 = QLabel()
        self._label1.setStyleSheet('color: black;')
        self._label1.setText(f'Kernel size: 0')
        self._layout.addWidget(self._label1, 1)
        self._layout.addWidget(self._slider, 1)
        self._layout.addWidget(self._buttons_widget, 1)
        self._layout.addWidget(self._progress_bar, 1)

        self.setLayout(self._layout)

    def _create_button(self, title, signal):
        button = QPushButton(title)
        button.clicked.connect(signal)
        button.setStyleSheet(
            '''
                height: 50px;
                background-color: black;
                outline: none;
                font-size: 24px;
                color: white;
                border-radius: 12px;
            '''
        )

        return button

    def _create_radio_button(self, title, axis, is_checked=False):
        radio_button = QRadioButton(title)
        radio_button.axis = axis
        radio_button.toggled.connect(self._radio_button_tapped)
        radio_button.setChecked(is_checked)
        radio_button.setStyleSheet('color: black;')

        return radio_button

    def _remove_noise_button_tapped(self):
        with Image.open(self._path) as image:
            kernel_size = self._slider.value()

            if self._selected_kernel_option == 'both':
                self._image_helper.median_filter(image, kernel_width=kernel_size, kernel_height=kernel_size, progress_handler=lambda x: self._progress_bar.setValue(x))
            elif self._selected_kernel_option == 'vertical':
                self._image_helper.median_filter(image, kernel_height=kernel_size, progress_handler=lambda x: print(x))
            else:
                self._image_helper.median_filter(image, kernel_width=kernel_size, progress_handler=lambda x: print(x))

            self._images_widget.set_unnoised_image()

    def _create_noise_button_tapped(self):
        self._image_helper.noise_image(self._path, 900)
        self._images_widget.set_noised_image(self._path)

    def _radio_button_tapped(self):
        self._selected_kernel_option = self.sender().axis

    def _open_file_button_tapped(self):
        self._path = QFileDialog.getOpenFileName(self, "Open file", "", "All files (*.png)")[0]
        self._images_widget.set_noised_image(self._path)

    def _slider_value_changed(self):
        self._label1.setText(f'Kernel size: {self._slider.value()}')