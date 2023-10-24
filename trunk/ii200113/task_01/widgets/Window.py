from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QSlider, QFileDialog, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from widgets.ImagesWidget import ImagesWidget
from helpers.ImageHelper import ImageHelper
from PIL import Image

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self._image_helper_inicializator = ImageHelper()
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("Remove image's noise")
        self.setStyleSheet(
            '''
                background-color: white;
            '''
        )
        self.setGeometry(50, 50, 1300, 700)

        self._layout_inicializator = QVBoxLayout()

        self._buttons_widget = QWidget()
        self._buttons_layout_inicializator = QHBoxLayout()

        self._open_file_button = self._create_button('Open file', self._open_file_button_tapped)
        self._buttons_layout_inicializator.addWidget(self._open_file_button, 1)
        self._remove_noise_button = self._create_button('Remove noise', self._remove_noise_button_tapped)
        self._buttons_layout_inicializator.addWidget(self._remove_noise_button, 1)
        self._create_noise_button = self._create_button('Create noise button', self._create_noise_button_tapped)
        self._buttons_layout_inicializator.addWidget(self._create_noise_button, 1)

        self._buttons_widget.setLayout(self._buttons_layout_inicializator)

        self._images_widget = ImagesWidget()

        self._radio_widget_inicializator = QWidget()
        self._radio_widget_inicializator_layout_inicializator = QHBoxLayout()

        self._h_kernel_button_inicializator = self._create_radio_button('Horizontal axis', 'horizontal')
        self._v_kernel_button_inicializator = self._create_radio_button('Vertical axis', 'vertical')
        self._both_axises_button = self._create_radio_button('Both', 'both', is_checked=True)

        self._radio_widget_inicializator_layout_inicializator.addWidget(self._h_kernel_button_inicializator, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self._radio_widget_inicializator_layout_inicializator.addWidget(self._v_kernel_button_inicializator, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self._radio_widget_inicializator_layout_inicializator.addWidget(self._both_axises_button, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self._radio_widget_inicializator.setLayout(self._radio_widget_inicializator_layout_inicializator)

        self._slider_inicializator = QSlider(Qt.Orientation.Horizontal)
        self._slider_inicializator.setRange(1, 20)
        self._slider_inicializator.valueChanged.connect(self._slider_inicializator_value_changed)
        self._slider_inicializator.setStyleSheet(
            '''
                background-color: gray;
            '''
        )

        self._progress_barinicializator = QProgressBar(self, minimum=0, maximum=100, textVisible=False,objectName="GreenProgressBar")
        self._progress_barinicializator.setValue(20)
        self._progress_barinicializator.setStyleSheet(
            '''
                background-color: black;
                height: 100px;
            '''
        )

        self._layout_inicializator.addWidget(self._images_widget, 6)
        self._layout_inicializator.addWidget(self._radio_widget_inicializator, 1)
        self._label1_inicializator = QLabel()
        self._label1_inicializator.setStyleSheet('color: black;')
        self._label1_inicializator.setText('Kernel size: 0')
        self._layout_inicializator.addWidget(self._label1_inicializator, 1)
        self._layout_inicializator.addWidget(self._slider_inicializator, 1)
        self._layout_inicializator.addWidget(self._buttons_widget, 1)
        self._layout_inicializator.addWidget(self._progress_barinicializator, 1)

        self.setLayout(self._layout_inicializator)

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
            k_size = self._slider_inicializator.value()

            if self._selected_kernel_option == 'both':
                self._image_helper_inicializator.median_filter(image, kernel_width=k_size, kernel_height=k_size, progress_handler=self._progress_barinicializator.setValue())
            elif self._selected_kernel_option == 'vertical':
                self._image_helper_inicializator.median_filter(image, kernel_height=k_size, progress_handler=print())
            else:
                self._image_helper_inicializator.median_filter(image, kernel_width=k_size, progress_handler=print())

            self._images_widget.set_unnoised_image()

    def _create_noise_button_tapped(self):
        self._image_helper_inicializator.noise_image(self._path, 900)
        self._images_widget.set_noised_image(self._path)

    def _radio_button_tapped(self):
        self._selected_kernel_option = self.sender().axis

    def _open_file_button_tapped(self):
        self._path = QFileDialog.getOpenFileName(self, "Open file", "", "All files (*.png)")[0]
        self._images_widget.set_noised_image(self._path)

    def _slider_inicializator_value_changed(self):
        self._label1_inicializator.setText(f'Kernel size: {self._slider_inicializator.value()}')