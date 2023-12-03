import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QDialog, QVBoxLayout, QLabel, QListWidget, QMessageBox, QLineEdit

class Contact:
    def __init__(self, name, address):
        self.name = name
        self.address = address

class StyledInputDialog(QInputDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setInputMode(QInputDialog.TextInput)
        self.setTextEchoMode(QLineEdit.Normal)
        self.setStyleSheet("QLineEdit { background-color: #97D8C4; border: 1px solid #97D8C4; border-radius: 8px; padding: 5px; }"
                           "QLineEdit:hover { border-color: `#EFF2F1`; }"
                           "QLineEdit:focus { border-color: #EFF2F1; }")
class SearchResultsDialog(QDialog):
    def __init__(self, contacts):
        super().__init__()

        self.setWindowTitle("Результаты поиска")
        self.setGeometry(100, 100, 750, 400)

        layout = QVBoxLayout()

        if contacts:
            label = QLabel(f"Найдено совпадений:{len(contacts)}")
            layout.addWidget(label)
            label.setStyleSheet("font: 75 20pt \"MS Serif\";")

            list_widget = QListWidget()
            for contact in contacts:
                list_widget.addItem(f"NAME: {contact.name}, ADDRESS: {contact.address}")

            # Устанавливаем стили для QListWidget
            list_widget.setStyleSheet("QListWidget {"
                                      "    background-color: #97D8C4; /* Цвет фона */"
                                      "    border: 1px solid #CCCCCC; /* Граница с рамкой */"
                                      "    border-radius: 8px; /* Закругленные углы */"
                                      "    padding: 5px; /* Внутренний отступ */"
                                      "    font-family: MS Serif;\n"
                                      "    font-size: 25px;\n"
                                      "}"
                                      "QListWidget:hover {"
                                      "    border-color: #E0FFFF; /* Изменение цвета рамки при наведении курсора */"
                                      "}"
                                      "QListWidget:focus {"
                                      "    border-color: #3CB371; /* Изменение цвета рамки при фокусировке */"
                                      "}")

            layout.addWidget(list_widget)
        else:
            label = QLabel("Контакты с указанным именем не найдены.")
            layout.addWidget(label)


        self.setLayout(layout)
class AddressBookApp(QtWidgets.QMainWindow):

    qpushbttn = "QPushButton {"
                               "background-color: #EFF2F1; /* Задайте цвет фона кнопки */\n"
                               "color: white; /* Задайте цвет текста кнопки */\n"
                               "border: 2px solid #97D8C4; /* Задайте стиль границы кнопки */\n"
                               "border-radius: 11px; /* Задайте скругление углов кнопки */\n"
                               "font-family: MS Serif;\n"
                               "font-size: 25px;\n"
                               "}\n"
                               "QPushButton:hover {\n"
                               "background-color: #6B9AC4; /* Задайте цвет фона при наведении курсора */\n"
                               "color: black;\n"
                               "}\n"
                               "QPushButton:pressed {\n"
                               "background-color: #EFF2F1    ; /* Задайте цвет фона при нажатии на кнопку */\n"
                               "border: 2px solid black; /* Задайте стиль границы при нажатии */\n"
                               "color: white;\n"
                               "}"

    def __init__(self):
        super().__init__()
        self.initUI()
        self.contacts = []
        self.current_contact_index = 0

    def initUI(self):
        self.setWindowTitle("Адресная книга")
        self.setGeometry(100, 100, 750, 400)

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.NAME = QtWidgets.QLineEdit(self.centralwidget)
        self.NAME.setGeometry(QtCore.QRect(160, 20, 371, 51))
        self.NAME.setObjectName("NAME")
        self.NAME.setStyleSheet("QLineEdit {\n"
                                "    background-color: #E0FFFF; /* Цвет фона */\n"
                                "    border: 1px solid #CCCCCC; /* Граница с рамкой */\n"
                                "    border-radius: 8px; /* Закругленные углы */\n"
                                "    padding: 5px; /* Внутренний отступ */\n"
                                "     \n"
                                "}\n"
                                "\n"
                                "QLineEdit:hover {\n"
                                "    border-color: #E0FFFF; /* Изменение цвета рамки при наведении курсора */\n"
                                "}\n"
                                "\n"
                                "QLineEdit:focus {\n"
                                "    border-color: #3CB371; /* Изменение цвета рамки при фокусировке */\n"
                                "}")
        self.ADDRESS = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.ADDRESS.setGeometry(QtCore.QRect(160, 110, 371, 201))
        self.ADDRESS.setObjectName("ADDRESS")
        self.ADDRESS.setStyleSheet("QPlainTextEdit {\n"
                                   "    font: italic 20pt \"Harlow Solid Italic\";\n"
                                   "    background-color: #E0FFFF; /* Цвет фона */\n"
                                   "    border: 1px solid #CCCCCC; /* Граница с рамкой */\n"
                                   "    border-radius: 10px; /* Закругленные углы */\n"
                                   "    padding: 5px; /* Внутренний отступ */\n"
                                   "     \n"
                                   "}\n"
                                   "\n"
                                   "QPlainTextEdit:hover {\n"
                                   "    border-color: #E0FFFF; /* Изменение цвета рамки при наведении курсора */\n"
                                   "}\n"
                                   "\n"
                                   "QPlainTextEdit:focus {\n"
                                   "    border-color: #3CB371; /* Изменение цвета рамки при фокусировке */\n"
                                   "}")
        self.ADD = QtWidgets.QPushButton(self.centralwidget)
        self.ADD.setGeometry(QtCore.QRect(560, 20, 171, 41))
        self.ADD.setText("ADD")
        self.ADD.clicked.connect(self.add_contact)
        self.ADD.setStyleSheet(qpushbttn)
        self.EDIT = QtWidgets.QPushButton(self.centralwidget)
        self.EDIT.setGeometry(QtCore.QRect(560, 70, 171, 41))
        self.EDIT.setText("EDIT")
        self.EDIT.setStyleSheet(qpushbttn)
        self.EDIT.clicked.connect(self.edit_contact)
        self.REMOVE = QtWidgets.QPushButton(self.centralwidget)
        self.REMOVE.setGeometry(QtCore.QRect(560, 120, 171, 41))
        self.REMOVE.setText("REMOVE")
        self.REMOVE.setStyleSheet(qpushbttn)
        self.REMOVE.clicked.connect(self.remove_contact)
        self.FIND = QtWidgets.QPushButton(self.centralwidget)
        self.FIND.setGeometry(QtCore.QRect(560, 170, 171, 41))
        self.FIND.setText("FIND")
        self.FIND.setStyleSheet(qpushbttn)
        self.FIND.clicked.connect(self.find_contact)
        self.LOAD = QtWidgets.QPushButton(self.centralwidget)
        self.LOAD.setGeometry(QtCore.QRect(560, 220, 171, 41))
        self.LOAD.setText("LOAD")
        self.LOAD.setStyleSheet(qpushbttn)
        self.LOAD.clicked.connect(self.load_contacts)
        self.SAVE = QtWidgets.QPushButton(self.centralwidget)
        self.SAVE.setGeometry(QtCore.QRect(560, 270, 171, 41))
        self.SAVE.setText("SAVE")
        self.SAVE.setStyleSheet(qpushbttn)
        self.SAVE.clicked.connect(self.save_contacts)
        self.EXPORT = QtWidgets.QPushButton(self.centralwidget)
        self.EXPORT.setGeometry(QtCore.QRect(560, 320, 171, 41))
        self.EXPORT.setText("EXPORT")
        self.EXPORT.setStyleSheet(qpushbttn)
        self.EXPORT.clicked.connect(self.export_contacts)
        self.PREVIOUS = QtWidgets.QPushButton(self.centralwidget)
        self.PREVIOUS.setGeometry(QtCore.QRect(160, 330, 181, 41))
        self.PREVIOUS.setText("PREVIOUS")
        self.PREVIOUS.clicked.connect(self.show_previous)
        self.PREVIOUS.setStyleSheet(qpushbttn)
        self.NEXT = QtWidgets.QPushButton(self.centralwidget)
        self.NEXT.setGeometry(QtCore.QRect(350, 330, 181, 41))
        self.NEXT.setText("NEXT")
        self.NEXT.clicked.connect(self.show_next)
        self.NEXT.setStyleSheet(qpushbttn)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 111, 51))
        self.label.setText("NAME")
        self.label.setStyleSheet("\n"
                                 "font: 75 20pt \"MS Serif\";")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 151, 41))
        self.label_2.setText("ADDRESS")
        self.label_2.setStyleSheet("font: 75 20pt \"MS Serif\";")

    def add_contact(self):
        name = self.NAME.text()
        address = self.ADDRESS.toPlainText()
        if name and address:
            contact = Contact(name, address)
            self.contacts.append(contact)
            self.clear()
            self.show_mssg("Контакт добавлен успешно.")
        else:
            self.show_mssg("Заполните все поля перед добавлением контакта.")

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
            self.clear()
            self.show_mssg("Контакт успешно отредактирован.")
        else:
            self.show_mssg("Выберите контакт для редактирования.")

    def remove_contact(self):
        # Получаем текущий индекс контакта
        index = self.current_contact_index

        # Проверяем, что индекс допустим и контакт существует
        if 0 <= index < len(self.contacts):
            # Создаем диалоговое окно для подтверждения
            confirmation = QMessageBox()
            confirmation.setIcon(QMessageBox.Question)
            confirmation.setWindowTitle("Подтверждение удаления")
            confirmation.setText("Вы уверены, что хотите удалить этот контакт?")
            confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirmation.setDefaultButton(QMessageBox.No)

            # Отображаем диалоговое окно и проверяем результат
            result = confirmation.exec_()
            if result == QMessageBox.Yes:
                # Если пользователь подтвердил удаление, удаляем контакт
                del self.contacts[index]

                # Очищаем поля и выводим сообщение
                self.clear()
                self.show_mssg("Контакт успешно удален.")
        else:
            self.show_mssg("Выберите контакт для удаления.")

    def find_contact(self):
        # Отображаем кастомное диалоговое окно для ввода текста поиска
        dialog = StyledInputDialog(self)
        dialog.setWindowTitle("Поиск контакта")
        dialog.setLabelText("Введите имя для поиска:")

        ok_pressed = dialog.exec_()

        if ok_pressed:
            search_text = dialog.textValue()
            if search_text:
                # Ищем контакты, содержащие заданный текст в имени
                matching_contacts = [contact for contact in self.contacts if search_text.lower() in contact.name.lower()]

                if matching_contacts:
                    # Отображаем результаты поиска в отдельном окне
                    self.show_search_results(matching_contacts)
                else:
                    self.show_mssg(f"Контакты с именем '{search_text}' не найдены.")
        else:
            self.show_mssg("Поиск отменен.")
    def show_search_results(self, contacts):
        # Создаем и отображаем диалоговое окно с результатами поиска
        dialog = SearchResultsDialog(contacts)
        dialog.exec_()

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
            self.show_mssg("Контакты успешно загружены из файла.")
        except FileNotFoundError:
            self.show_mssg("Файл с контактами не найден.")

    def save_contacts(self):
        try:
            with open("contacts.txt", "w", encoding="utf-8") as file:
                for contact in self.contacts:
                    file.write(f"{contact.name};{contact.address}\n")
            self.show_mssg("Контакты успешно сохранены в файл.")
        except Exception as e:
            self.show_mssg(f"Ошибка при сохранении: {str(e)}")

    def export_contacts(self):
        try:
            for index, contact in enumerate(self.contacts, start=1):
                vcf_filename = f"{contact.name}.vcf"

                with open(vcf_filename, "w", encoding="utf-8") as vcf_file:
                    vcf_file.write("BEGIN:IDCARD\n")
                    vcf_file.write("VERS:1.0\n")
                    vcf_file.write(f"N:{contact.name}\n")
                    vcf_file.write(f"FN:{contact.name}\n")
                    vcf_file.write(f"ADR:;;{contact.address};;;;\n")
                    vcf_file.write("END:IDCARD\n")

            self.show_mssg("Контакты экспортированы в файлы .vcf.")
        except Exception as e:
            self.show_mssg(f"Ошибка при экспорте: {str(e)}")

    def clear(self):
        self.NAME.clear()
        self.ADDRESS.clear()

    def show_mssg(self, message):
        QtWidgets.QMessageBox.information(self, "Сообщение", message)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = AddressBookApp()
    mainWindow.show()
    sys.exit(app.exec_())
