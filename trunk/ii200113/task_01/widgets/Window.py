from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QSlider, QFileDialog, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from widgets.ImagesWidget import ImagesWidget
from helpers.ImageHelper import ImageHelper
from PIL import Image

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.image_helper = ImageHelper()
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("Remove image's noise")
        self.setStyleSheet('''background-color: white;''')
        self.setGeometry(50, 50, 1300, 700)
        self._main_layout = QVBoxLayout()
        self._buttons_widget = QWidget()
        self._buttons_layout = QHBoxLayout()
        self._open_file_btn = self._create_button('Open file', self._open_file_clicked)
        self._buttons_layout.addWidget(self._open_file_btn, 1)
        self._remove_noise_btn = self._create_button('Remove noise', self._remove_noise_clicked)
        self._buttons_layout.addWidget(self._remove_noise_btn, 1)
        self._add_noise_btn = self._create_button('Create noise button', self._add_noise_clicked)
        self._buttons_layout.addWidget(self._add_noise_btn, 1)
        self._buttons_widget.setLayout(self._buttons_layout)
        self._images_widget = ImagesWidget()
        self._radio_widget = QWidget()
        self._radio_layout = QHBoxLayout()
        self._horizontal_radio = self._create_radio('Horizontal axis', 'horizontal')
        self._radio_layout.addWidget(self._horizontal_radio, 1, Qt.AlignCenter)
        self._vertical_radio = self._create_radio('Vertical axis', 'vertical')
        self._radio_layout.addWidget(self._vertical_radio, 1, Qt.AlignCenter)
        self._both_radio = self._create_radio('Both', 'both', True)
        self._radio_layout.addWidget(self._both_radio, 1, Qt.AlignCenter)
        self._radio_widget.setLayout(self._radio_layout)
        self._kernel_slider = QSlider(Qt.Horizontal)
        self._kernel_slider.setRange(1, 20)
        self._kernel_slider.valueChanged.connect(self._on_kernel_change)
        self._kernel_slider.setStyleSheet('''background-color: gray;''')
        self._progress_bar = QProgressBar(self, minimum=0, maximum=100, textVisible=False)
        self._progress_bar.setValue(20)
        self._progress_bar.setStyleSheet('''background-color: black;height: 100px;''')
        self._main_layout.addWidget(self._images_widget, 6)
        self._main_layout.addWidget(self._radio_widget, 1)
        self._kernel_label = QLabel()
        self._kernel_label.setText('Kernel size: 0')
        self._main_layout.addWidget(self._kernel_label, 1)
        self._main_layout.addWidget(self._kernel_slider, 1)
        self._main_layout.addWidget(self._buttons_widget, 1)
        self._main_layout.addWidget(self._progress_bar, 1)
        self.setLayout(self._main_layout)

    def _create_button(self, text, signal):
        button = QPushButton(text)
        button.clicked.connect(signal)
        button.setStyleSheet('''height: 50px;background-color: black;outline: none;font-size: 24px;color: white;border-radius: 12px;''')
        return button
    
    def _create_radio(self, text, axis, checked=False):
        radio = QRadioButton(text)
        radio.axis = axis
        radio.toggled.connect(self._on_radio_toggle)
        radio.setChecked(checked)
        radio.setStyleSheet('color: black;')
        return radio

    def _on_radio_toggle(self):
        self._selected_axis = self.sender().axis

    def _open_file_clicked(self):
        path = QFileDialog.getOpenFileName(self, 'Open file', '', 'Image files (*.png)')[0]
        self._images_widget.set_noised_image(path)
        self._file_path = path

    def _remove_noise_clicked(self):
        image = Image.open(self._file_path)
        kernel_size = self._kernel_slider.value()
        if self._selected_axis == 'both':
            self.image_helper.median_filter(image, kernel_width=kernel_size, kernel_height=kernel_size, progress_handler=self._update_progress)
        elif self._selected_axis == 'vertical':
            self.image_helper.median_filter(image, kernel_height=kernel_size)
        else:
            self.image_helper.median_filter(image, kernel_width=kernel_size)
        self._images_widget.set_unnoised_image()

    def _add_noise_clicked(self):
        self.image_helper.noise_image(self._file_path, 900)
        self._images_widget.set_noised_image(self._file_path)

    def _on_kernel_change(self):
        self._kernel_label.setText(f'Kernel size: {self._kernel_slider.value()}')

    def _update_progress(self, value):
        self._progress_bar.setValue(value)