import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Contact:
    def __init__(self, name, address):
        self.name = name
        self.address = address

class AddressBookApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.contacts = []
        self.current_contact_index = 0

    def initUI(self):
        self.setWindowTitle("ADRESSNAYA KNIGA")
        self.setGeometry(100, 100, 750, 400)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.NAME = QtWidgets.QLineEdit(self.centralwidget)
        self.NAME.setGeometry(QtCore.QRect(160, 20, 371, 51))
        self.NAME.setObjectName("NAME")                    
        self.ADDRESS = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.ADDRESS.setGeometry(QtCore.QRect(160, 110, 371, 201))
        self.ADDRESS.setObjectName("ADDRESS ")
        self.ADD = QtWidgets.QPushButton(self.centralwidget)
        self.ADD.setGeometry(QtCore.QRect(560, 20, 171, 41))
        self.ADD.setText("ADD")
        self.ADD.clicked.connect(self.add_contact)
        self.EDIT = QtWidgets.QPushButton(self.centralwidget)
        self.EDIT.setGeometry(QtCore.QRect(560, 70, 171, 41))
        self.EDIT.setText("EDIT")
        self.EDIT.clicked.connect(self.edit_contact)
        self.REMOVE = QtWidgets.QPushButton(self.centralwidget)
        self.REMOVE.setGeometry(QtCore.QRect(560, 120, 171, 41))
        self.REMOVE.setText("REMOVE")
        self.REMOVE.clicked.connect(self.remove_contact)
        self.FIND = QtWidgets.QPushButton(self.centralwidget)
        self.FIND.setGeometry(QtCore.QRect(560, 170, 171, 41))
        self.FIND.setText("FIND")
        self.FIND.clicked.connect(self.find_contact)
        self.LOAD = QtWidgets.QPushButton(self.centralwidget)
        self.LOAD.setGeometry(QtCore.QRect(560, 220, 171, 41))
        self.LOAD.setText("LOAD")
        self.LOAD.clicked.connect(self.load_contacts)
        self.SAVE = QtWidgets.QPushButton(self.centralwidget)
        self.SAVE.setGeometry(QtCore.QRect(560, 270, 171, 41))
        self.SAVE.setText("SAVE")
        self.SAVE.clicked.connect(self.save_contacts)
        self.EXPORT = QtWidgets.QPushButton(self.centralwidget)
        self.EXPORT.setGeometry(QtCore.QRect(560, 320, 171, 41))
        self.EXPORT.setText("EXPORT")
        self.EXPORT.clicked.connect(self.export_contacts)
        self.PREVIOUS = QtWidgets.QPushButton(self.centralwidget)
        self.PREVIOUS.setGeometry(QtCore.QRect(160, 320, 181, 41))
        self.PREVIOUS.setText("PREVIOUS")
        self.PREVIOUS.clicked.connect(self.show_previous)
        self.NEXT = QtWidgets.QPushButton(self.centralwidget)
        self.NEXT.setGeometry(QtCore.QRect(350, 320, 181, 41))
        self.NEXT.setText("NEXT")
        self.NEXT.clicked.connect(self.show_next)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 111, 51))
        self.label.setText("NAME:")
        self.label.setStyleSheet("\n"
                                 "font: 75 20pt \"Times New Roman\";")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 151, 41))
        self.label_2.setText("ADDRESS:")
        self.label_2.setStyleSheet("font: 75 20pt \"Times New Roman\";")
    def add_contact(self):
        name = self.NAME.text()
        address = self.ADDRESS.toPlainText()
        if name and address:
            contact = Contact(name, address)
            self.contacts.append(contact)
            self.clear_fields()
            self.show_message("Контакт добавлен успешно.")
        else:
            self.show_message("Заполните все поля перед добавлением контакта.")
    def show_previous(self):
        if self.current_contact_index > 0:
            self.current_contact_index -= 1
            self.display_contact()
    def show_next(self):
        if self.current_contact_index < len(self.contacts) - 1:
            self.current_contact_index += 1
            self.display_contact()
    def display_contact(self):
        if 0 <= self.current_contact_index < len(self.contacts):
            # Отобразить контакт с индексом self.current_contact_index
            contact = self.contacts[self.current_contact_index]
            self.NAME.setText(contact.name)
            self.ADDRESS.setPlainText(contact.address)
        else:
            # Если нет контактов или неверный индекс, очистить поля
            self.NAME.clear()
            self.ADDRESS.clear()
    def edit_contact(self):
        # Получаем текущий индекс контакта
        index = self.current_contact_index
        # Проверяем, что индекс допустим и контакт существует
        if 0 <= index < len(self.contacts):
            # Получаем новое имя и адрес
            name = self.NAME.text()
            address = self.ADDRESS.toPlainText()
            # Обновляем информацию о контакте
            self.contacts[index].name = name
            self.contacts[index].address = address
            # Очищаем поля и выводим сообщение
            self.clear_fields()
            self.show_message("Контакт успешно отредактирован.")
        else:
            self.show_message("Выберите контакт для редактирования.")
    def remove_contact(self):
        # Получаем текущий индекс контакта
        index = self.current_contact_index
        # Проверяем, что индекс допустим и контакт существует
        if 0 <= index < len(self.contacts):
            # Удаляем контакт из списка
            del self.contacts[index]
            # Очищаем поля и выводим сообщение
            self.clear_fields()
            self.show_message("Контакт успешно удален.")
        else:
            self.show_message("Выберите контакт для удаления.")
    def find_contact(self):
        # Получаем текст для поиска
        search_text = self.NAME.text()
        self.save_contacts()
        # Ищем контакты, содержащие заданный текст в имени
        matching_contacts = [contact for contact in self.contacts if search_text.lower() in contact.name.lower()]
        # Если есть совпадения, выбираем первый и отображаем
        if matching_contacts:
            self.contacts = matching_contacts
            self.current_contact_index = 0
            self.display_contact()
            self.show_message(f"Найдено {len(matching_contacts)} совпадений.")
        else:
            self.show_message("Контакты с указанным именем не найдены.")
    def load_contacts(self):
        self.contacts.clear()
        try:
            with open("contacts.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split(";")
                    if len(parts) == 2:
                        name, address = parts
                        contact = Contact(name, address)
                        self.contacts.append(contact)
            self.show_message("Контакты успешно загружены из файла.")
        except FileNotFoundError:
            self.show_message("Файл с контактами не найден.")
    def save_contacts(self):
        try:
            with open("contacts.txt", "w", encoding="utf-8") as file:
                for contact in self.contacts:
                    file.write(f"{contact.name};{contact.address}\n")
            self.show_message("Контакты успешно сохранены в файл.")
        except Exception as e:
            self.show_message(f"Произошла ошибка при сохранении контактов: {str(e)}")
    def export_contacts(self):
        try:
            for index, contact in enumerate(self.contacts, start=1):
                vcf_filename = f"{contact.name}.vcf"
                with open(vcf_filename, "w", encoding="utf-8") as vcf_file:
                    vcf_file.write(f"BEGIN:VCARD\n")
                    vcf_file.write(f"VERSION:3.0\n")
                    vcf_file.write(f"N:{contact.name}\n")
                    vcf_file.write(f"FN:{contact.name}\n")
                    vcf_file.write(f"ADR:;;{contact.address};;;;\n")
                    vcf_file.write(f"END:VCARD\n")
            self.show_message("Контакты успешно экспортированы в файлы .vcf.")
        except Exception as e:
            self.show_message(f"Произошла ошибка при экспорте контактов: {str(e)}")

    def clear_fields(self):
        self.NAME.clear()
        self.ADDRESS.clear()

    def show_message(self, message):
        QtWidgets.QMessageBox.information(self, "Сообщение", message)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = AddressBookApp()
    mainWindow.show()
    sys.exit(app.exec_())
