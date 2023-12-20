import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QGroupBox, QDialog
from PyQt5.QtGui import QPalette, QColor


class AddressBookApp(QWidget):
    def __init__(self):
        super().__init__()

        self.contacts = []

        self.init_ui()

    def init_ui(self):
        # Создание виджетов
        self.label_name = QLabel('Имя:')
        self.label_phone = QLabel('Телефон:')
        self.edit_name = QLineEdit()
        self.edit_phone = QLineEdit()
        self.btn_add_contact = QPushButton('Добавить контакт')
        self.list_contacts = QListWidget()
        self.btn_edit_contact = QPushButton('Редактировать')
        self.btn_delete_contact = QPushButton('Удалить')

        # Создание группы виджетов
        input_group = QGroupBox('Добавить контакт')
        input_layout = QVBoxLayout(input_group)
        input_layout.addWidget(self.label_name)
        input_layout.addWidget(self.edit_name)
        input_layout.addWidget(self.label_phone)
        input_layout.addWidget(self.edit_phone)
        input_layout.addWidget(self.btn_add_contact)

        contact_group = QGroupBox('Список контактов')
        contact_layout = QVBoxLayout(contact_group)
        contact_layout.addWidget(self.list_contacts)
        contact_layout.addWidget(self.btn_edit_contact)
        contact_layout.addWidget(self.btn_delete_contact)

        main_layout = QHBoxLayout()
        main_layout.addWidget(input_group)
        main_layout.addWidget(contact_group)

        self.setLayout(main_layout)

        # Назначение обработчиков событий
        self.btn_add_contact.clicked.connect(self.add_contact)
        self.btn_edit_contact.clicked.connect(self.edit_contact)
        self.btn_delete_contact.clicked.connect(self.delete_contact)
        self.list_contacts.itemClicked.connect(self.load_contact_info)

        # Стилизация виджетов
        self.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                margin-top: 10px;
            }
            QLabel {
                font-size: 16px;
            }
            QLineEdit, QListWidget {
                font-size: 16px;
                padding: 8px;
            }
            QPushButton {
                font-size: 16px;
                padding: 8px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #357835;
            }
        """)

        # Настройка окна
        self.setWindowTitle('Адресная книга')
        self.setGeometry(100, 100, 600, 300)

    def add_contact(self):
        name = self.edit_name.text()
        phone = self.edit_phone.text()

        if name and phone:
            contact_str = f'{name}: {phone}'
            self.contacts.append(contact_str)
            self.list_contacts.addItem(contact_str)

            # Очищаем поля ввода
            self.edit_name.clear()
            self.edit_phone.clear()

    def edit_contact(self):
        current_row = self.list_contacts.currentRow()
        if current_row != -1:
            edited_contact, ok = EditContactDialog.get_contact_info(self.contacts[current_row])
            if ok:
                self.contacts[current_row] = edited_contact
                self.list_contacts.clear()
                self.list_contacts.addItems(self.contacts)

    def delete_contact(self):
        current_row = self.list_contacts.currentRow()
        if current_row != -1:
            del self.contacts[current_row]
            self.list_contacts.clear()
            self.list_contacts.addItems(self.contacts)

    def load_contact_info(self, item):
        contact_info = item.text().split(': ')
        self.edit_name.setText(contact_info[0])
        self.edit_phone.setText(contact_info[1])


class EditContactDialog(QDialog):
    @staticmethod
    def get_contact_info(contact):
        dialog = EditContactDialog(contact)
        result = dialog.exec_()
        return dialog.edited_contact, result == dialog.Accepted

    def __init__(self, contact):
        super().__init__()

        self.edited_contact = contact

        self.init_ui()

    def init_ui(self):
        # Создание виджетов
        self.label_name = QLabel('Имя:')
        self.label_phone = QLabel('Телефон:')
        self.edit_name = QLineEdit(self.edited_contact.split(': ')[0])
        self.edit_phone = QLineEdit(self.edited_contact.split(': ')[1])
        self.btn_save = QPushButton('Сохранить')
        self.btn_cancel = QPushButton('Отмена')

        # Размещение виджетов в компоновщике QVBoxLayout
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.label_name)
        input_layout.addWidget(self.edit_name)
        input_layout.addWidget(self.label_phone)
        input_layout.addWidget(self.edit_phone)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_cancel)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Назначение обработчиков событий
        self.btn_save.clicked.connect(self.save_contact)
        self.btn_cancel.clicked.connect(self.reject)

        # Стилизация виджетов
        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
            }
            QLineEdit {
                font-size: 16px;
                padding: 8px;
            }
            QPushButton {
                font-size: 16px;
                padding: 8px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #357835;
            }
        """)

        # Настройка окна
        self.setWindowTitle('Редактирование контакта')
        self.setGeometry(200, 200, 300, 150)

    def save_contact(self):
        name = self.edit_name.text()
        phone = self.edit_phone.text()

        if name and phone:
            self.edited_contact = f'{name}: {phone}'
            self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    address_book = AddressBookApp()
    address_book.show()
    sys.exit(app.exec_())
