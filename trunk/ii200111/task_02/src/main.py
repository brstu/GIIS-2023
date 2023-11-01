import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, \
    QLabel, QTextEdit, QListWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QFileDialog


class PhoneBookApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initui()

    def initui(self):
        self.setWindowTitle("Phone Book")
        self.setGeometry(100, 100, 600, 400)

        self.phone_book = {}  # Dictionary для хранения данных
        self.page_size = 5  # Страницы
        self.current_page = 0  # Текущая страница

        # Центральный виджет и окно
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()

        # Кнопки
        left_layout = QVBoxLayout()

        # Вывод данных в поля
        self.name_entry = QLineEdit()
        self.address_entry = QTextEdit()
        left_layout.addWidget(QLabel("Name:"))
        left_layout.addWidget(self.name_entry)
        left_layout.addWidget(QLabel("Address:"))
        left_layout.addWidget(self.address_entry)

        # Вывод
        main_layout.addLayout(left_layout)

        # Вывод
        right_layout = QVBoxLayout()

        # Кнопки
        add_button = QPushButton("Add Entry")
        find_button = QPushButton("Find Entry")
        edit_button = QPushButton("Edit Entry")
        delete_button = QPushButton("Delete Entry")
        hint_button = QPushButton("Hint")
        next_page_button = QPushButton("Next Page")
        prev_page_button = QPushButton("Previous Page")
        save_button = QPushButton("Save")
        load_button = QPushButton("Load")

        add_button.clicked.connect(self.add_entry)
        find_button.clicked.connect(self.find_entry_dialog)
        edit_button.clicked.connect(self.edit_entry)
        delete_button.clicked.connect(self.delete_entry)
        hint_button.clicked.connect(self.show_hints)
        next_page_button.clicked.connect(self.next_page)
        prev_page_button.clicked.connect(self.prev_page)
        save_button.clicked.connect(self.save_phone_book)
        load_button.clicked.connect(self.load_phone_book)

        # Добавление кнопок
        right_layout.addWidget(add_button)
        right_layout.addWidget(find_button)
        right_layout.addWidget(edit_button)
        right_layout.addWidget(delete_button)
        right_layout.addWidget(hint_button)
        right_layout.addWidget(next_page_button)
        right_layout.addWidget(prev_page_button)
        right_layout.addWidget(save_button)
        right_layout.addWidget(load_button)

        main_layout.addLayout(right_layout)

        # Вывод списка виджетов
        self.entry_list = QListWidget()
        self.entry_list.itemClicked.connect(self.select_entry)
        main_layout.addWidget(self.entry_list)

        central_widget.setLayout(main_layout)

    def add_entry(self):
        name = self.name_entry.text()
        address = self.address_entry.toPlainText()

        if name and address:
            self.phone_book[name] = address
            self.name_entry.clear()
            self.address_entry.clear()
            self.refresh_entry_list()  # перезагрузка листа(лист-бокса)
        else:
            self.display_entry_data("Name and Address cannot be empty!")

    def find_entry_dialog(self):
        f_name = self.name_entry.text()
        if f_name in self.phone_book:
            QMessageBox.information(self, "Success", f"Entry '{f_name}' found.")
            self.name_entry.setText(f_name)
            self.address_entry.setPlainText(self.phone_book[f_name])
            self.refresh_entry_list()
        else:
            QMessageBox.warning(self, "Not Found", f"Entry '{f_name}' not found.")

    def edit_entry(self):
        if self.selected_entry:
            old_name = self.selected_entry.text()
            new_name = self.name_entry.text()
            new_address = self.address_entry.toPlainText()

            if old_name in self.phone_book:
                # обновить
                self.phone_book[new_name] = new_address
                if old_name != new_name:
                    del self.phone_book[old_name]  # удалить старую запись, если уже есть
                self.refresh_entry_list()
                QMessageBox.information(self, "Success", f"Entry '{new_name}' updated.")
            else:
                self.display_entry_data("Entry not found.")
                QMessageBox.warning(self, "Not Found", f"No matching entry found for '{old_name}'.")

    def delete_entry(self):
        name = self.name_entry.text()
        if name in self.phone_book:
            del self.phone_book[name]
            self.name_entry.clear()
            self.address_entry.clear()
            self.refresh_entry_list()  # Обновить
            QMessageBox.information(self, "Success", f"Entry '{name}' deleted.")
        else:
            self.display_entry_data(f"Entry not found for {name}.")

    def show_hints(self):
        QMessageBox.information(self, "Hint", "The program is a notebook. Use the specified buttons.")

    def select_entry(self, item):
        if item is not None:
            self.selected_entry = item
            name = item.text()
            if name in self.phone_book:
                self.name_entry.setText(name)
                self.address_entry.setPlainText(self.phone_book[name])

    def refresh_entry_list(self):
        self.entry_list.clear()
        entries = list(self.phone_book.keys())
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        for entry in entries[start_idx:end_idx]:
            self.entry_list.addItem(entry)

    def next_page(self):
        total_entries = len(self.phone_book)
        max_pages = (total_entries + self.page_size - 1) // self.page_size
        if self.current_page < max_pages - 1:
            self.current_page += 1
            self.refresh_entry_list()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.refresh_entry_list()

    def save_phone_book(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter("JSON Files (*.json)")
        if file_dialog.exec_():
            file_name = file_dialog.selectedFiles()[0]
            with open(file_name, 'w') as file:
                json.dump(self.phone_book, file)
            QMessageBox.information(self, "Success", "Phone book saved successfully.")

    def load_phone_book(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("JSON Files (*.json)")
        if file_dialog.exec_():
            file_name = file_dialog.selectedFiles()[0]
            try:
                with open(file_name, 'r') as file:
                    self.phone_book = json.load(file)
                self.refresh_entry_list()
                QMessageBox.information(self, "Success", "Phone book loaded successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load phone book: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = PhoneBookApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
