import sys, pickle
from enum import Enum
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QGridLayout, QHBoxLayout, QMessageBox, QDialog, QFileDialog
)
from PyQt5.QtCore import Qt


#Окно для обработки поиска
class FindDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        findLabel = QLabel("Enter the name of a contact:")
        self.lineEdit = QLineEdit()

        self.findButton = QPushButton("&Find")
        self.findText = ""

        layout = QHBoxLayout()
        layout.addWidget(findLabel)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.findButton)

        self.setLayout(layout)
        self.setWindowTitle("Find a Contact")
        self.findButton.clicked.connect(self.findClicked)
        self.findButton.clicked.connect(self.accept)

    def findClicked(self):
        text = self.lineEdit.text()

        if text == "":
            QMessageBox.information(self, "Empty Field",
                "Please enter a name.")
            return
        else:
            self.findText = text
            self.lineEdit.clear()
            self.hide()

    def getFindText(self):
        return self.findText


#Главное окно
class AddressBook(QWidget):
    #Enum для обозначения состояния главного окна
    class Mode(Enum):
        NavigationMode, AddingMode, EditingMode = range(3)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    #Создаём кучу кнопок и другое
    def initUI(self):
        nameLabel = QLabel("Name:")
        self.nameLine = QLineEdit()
        self.nameLine.setReadOnly(True)

        addressLabel = QLabel("Address:")
        self.addressText = QTextEdit()
        self.addressText.setReadOnly(True)

        self.addButton = QPushButton("&Add")
        self.addButton.clicked.connect(self.addContact)
        self.addButton.show()

        self.submitButton = QPushButton("&Submit")
        self.submitButton.clicked.connect(self.submitContact)
        self.submitButton.hide()

        self.cancelButton = QPushButton("&Cancel")
        self.cancelButton.clicked.connect(self.cancel)
        self.cancelButton.hide()

        self.nextButton = QPushButton("&Next")
        self.nextButton.clicked.connect(self.next)
        self.nextButton.setEnabled(False)

        self.previousButton = QPushButton("&Previous")
        self.previousButton.clicked.connect(self.previous)
        self.previousButton.setEnabled(False)

        self.editButton = QPushButton("&Edit")
        self.editButton.clicked.connect(self.editContact)
        self.editButton.setEnabled(False)

        self.removeButton = QPushButton("&Remove")
        self.removeButton.clicked.connect(self.removeContact)
        self.removeButton.setEnabled(False)

        self.findButton = QPushButton("&Find")
        self.findButton.clicked.connect(self.findContact)
        self.findButton.setEnabled(False)

        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(self.addButton, alignment=Qt.AlignTop)
        buttonLayout1.addWidget(self.submitButton)
        buttonLayout1.addWidget(self.cancelButton)
        buttonLayout1.addWidget(self.editButton)
        buttonLayout1.addWidget(self.removeButton)
        buttonLayout1.addWidget(self.findButton)
        buttonLayout1.addStretch()

        buttonLayout2 = QHBoxLayout()
        buttonLayout2.addWidget(self.previousButton)
        buttonLayout2.addWidget(self.nextButton)

        self.loadButton = QPushButton("&Load")
        self.loadButton.setToolTip("Load contacts from a file")
        self.loadButton.clicked.connect(self.loadFromFile)

        self.saveButton = QPushButton("&Save")
        self.saveButton.setToolTip("Save contacts to a file")
        self.saveButton.clicked.connect(self.saveToFile)

        self.exportButton = QPushButton("&Export")
        self.exportButton.setToolTip("Export contact as a vCard")
        self.exportButton.clicked.connect(self.exportAsVCard)

        buttonLayout3 = QVBoxLayout()
        buttonLayout3.addWidget(self.loadButton)
        buttonLayout3.addWidget(self.saveButton)
        buttonLayout3.addWidget(self.exportButton)
        buttonLayout3.addStretch()

        mainLayout = QGridLayout()
        mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addWidget(self.nameLine, 0, 1)
        mainLayout.addWidget(addressLabel, 1, 0, alignment=Qt.AlignTop)
        mainLayout.addWidget(self.addressText, 1, 1)
        mainLayout.addLayout(buttonLayout1, 1, 2)
        mainLayout.addLayout(buttonLayout2, 2, 1)
        mainLayout.addLayout(buttonLayout3, 2, 2)

        self.setLayout(mainLayout)
        self.setWindowTitle("Simple Address Book")

        self.contacts = {}
        self.oldName = ""
        self.oldAddress = ""
        self.currentMode = self.Mode.NavigationMode

        self.dialog = FindDialog()

    def addContact(self):
        self.oldName = self.nameLine.text()
        self.oldAddress = self.addressText.toPlainText()

        self.nameLine.clear()
        self.addressText.clear()

        self.nameLine.setReadOnly(False)
        self.nameLine.setFocus(Qt.OtherFocusReason)
        self.addressText.setReadOnly(False)

        self.addButton.setEnabled(False)
        self.editButton.setEnabled(False)
        self.removeButton.setEnabled(False)
        self.nextButton.setEnabled(False)
        self.previousButton.setEnabled(False)
        self.findButton.setEnabled(False)
        self.submitButton.show()
        self.cancelButton.show()
        self.currentMode = self.Mode.AddingMode

    #Проверка на корректность внесённых данных
    def submitContact(self):
        name = self.nameLine.text()
        address = self.addressText.toPlainText()

        if name == "" or address == "":
            QMessageBox.information(self, "Empty Field",
                "Please enter a name and address.")
            return

        if self.currentMode == self.Mode.AddingMode:
            if name not in self.contacts:
                self.contacts[name] = address
                QMessageBox.information(self, "Add Successful",
                    f'"{name}" has been added to your address book.')
            else:
                QMessageBox.information(self, "Add Unsuccessful",
                    f'Sorry, "{name}" is already in your address book.')
        elif self.currentMode == self.Mode.EditingMode:
            if self.oldName != name:
                if name not in self.contacts:
                    self.contacts[name] = address
                    QMessageBox.information(self, "Edit Successful",
                        f'"{self.oldName}" has been edited in your address book.')
                    del self.contacts[self.oldName]
                else:
                    QMessageBox.information(self, "Edit Unsuccessful",
                        f'Sorry, "{name}" is already in your address book.')
            elif self.oldAddress != address:
                QMessageBox.information(self, "Edit Successful",
                    f'"{name}" has been edited in your address book.')
                self.contacts[name] = address

        self.updateInterface(self.Mode.NavigationMode)

    #Отмена внесения изменений
    def cancel(self):
        self.nameLine.setText(self.oldName)
        self.addressText.setText(self.oldAddress)

        self.nameLine.setReadOnly(True)
        self.addressText.setReadOnly(True)

        self.addButton.setEnabled(True)
        self.editButton.setEnabled(len(self.contacts) >= 1)
        self.removeButton.setEnabled(len(self.contacts) >= 1)
        self.nextButton.setEnabled(len(self.contacts) > 1)
        self.previousButton.setEnabled(len(self.contacts) > 1)
        self.findButton.setEnabled(True)
        self.submitButton.hide()
        self.cancelButton.hide()

        self.currentMode = self.Mode.NavigationMode

    def next(self):
        name = self.nameLine.text()
        names = list(self.contacts.keys())
        if name in names:
            index = names.index(name)
            index = (index + 1) % len(names)
            self.nameLine.setText(names[index])
            self.addressText.setText(self.contacts[names[index]])

    def previous(self):
        name = self.nameLine.text()
        names = list(self.contacts.keys())
        if name in names:
            index = names.index(name)
            index = (index - 1) % len(names)
            self.nameLine.setText(names[index])
            self.addressText.setText(self.contacts[names[index]])

    def editContact(self):
        self.oldName = self.nameLine.text()
        self.oldAddress = self.addressText.toPlainText()
        self.updateInterface(self.Mode.EditingMode)

    def removeContact(self):
        name = self.nameLine.text()
        if name in self.contacts:
            button = QMessageBox.question(self, "Confirm Remove",
                f'Are you sure you want to remove "{name}"?',
                QMessageBox.Yes | QMessageBox.No)
            if button == QMessageBox.Yes:
                self.next()
                del self.contacts[name]
                self.updateInterface(self.Mode.NavigationMode)
                QMessageBox.information(self, "Remove Successful",
                    f'"{name}" has been removed from your address book.')

    #Обновление окна в зависимости от состояния (вкл/выкл кнопки)
    def updateInterface(self, mode):
        self.currentMode = mode

        if self.currentMode == self.Mode.AddingMode or self.currentMode == self.Mode.EditingMode:
            self.nameLine.setReadOnly(False)
            self.nameLine.setFocus(Qt.OtherFocusReason)
            self.addressText.setReadOnly(False)

            self.addButton.setEnabled(False)
            self.editButton.setEnabled(False)
            self.removeButton.setEnabled(False)
            self.nextButton.setEnabled(False)
            self.previousButton.setEnabled(False)
            self.findButton.setEnabled(False)
            self.submitButton.show()
            self.cancelButton.show()
        elif self.currentMode == self.Mode.NavigationMode:
            if not self.contacts:
                self.nameLine.clear()
                self.addressText.clear()

            self.nameLine.setReadOnly(True)
            self.addressText.setReadOnly(True)
            self.addButton.setEnabled(True)
            self.editButton.setEnabled(len(self.contacts) >= 1)
            self.removeButton.setEnabled(len(self.contacts) >= 1)
            self.nextButton.setEnabled(len(self.contacts) > 1)
            self.previousButton.setEnabled(len(self.contacts) > 1)
            self.findButton.setEnabled(True)
            self.submitButton.hide()
            self.cancelButton.hide()

    def findContact(self):
        self.dialog.show()

        if self.dialog.exec_() == QDialog.Accepted:
            contactName = self.dialog.getFindText()

            if contactName in self.contacts:
                self.nameLine.setText(contactName)
                self.addressText.setText(self.contacts[contactName])
            else:
                QMessageBox.information(self, "Contact Not Found",
                    f'Sorry, "{contactName}" is not in your address book.')

        self.updateInterface(self.Mode.NavigationMode)

    def saveToFile(self):
        fileName, _ = QFileDialog.getSaveFileName(self,
            "Save Address Book", "", "Address Book (*.abk);;All Files (*)")

        if fileName == "":
            return
        else:
            with open(fileName, 'wb') as file:
                pickle.dump(self.contacts, file)

    def loadFromFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
            "Open Address Book", "", "Address Book (*.abk);;All Files (*)")

        if fileName == "":
            return
        else:
            try:
                with open(fileName, 'rb') as file:
                    self.contacts = pickle.load(file)

                if not self.contacts:
                    QMessageBox.information(self, "No contacts in file",
                        "The file you are attempting to open contains no contacts.")
                else:
                    name, address = next(iter(self.contacts.items()))
                    self.nameLine.setText(name)
                    self.addressText.setText(address)
            except (pickle.UnpicklingError, FileNotFoundError) as e:
                QMessageBox.information(self, "Unable to open file", str(e))

        self.updateInterface(self.Mode.NavigationMode)

    def exportAsVCard(self):
        name = self.nameLine.text()
        address = self.addressText.toPlainText()
        firstName, lastName = "", ""
        nameList = []

        index = name.find(" ")

        if index != -1:
            nameList = name.split()
            firstName = nameList[0]
            lastName = nameList[-1]
        else:
            firstName = name

        fileName, _ = QFileDialog.getSaveFileName(self,
            "Export Contact", "", "vCard Files (*.vcf);;All Files (*)")

        if fileName == "":
            return

        try:
            with open(fileName, 'w') as file:
                file.write("BEGIN:VCARD\n")
                file.write("VERSION:2.1\n")
                file.write(f"N:{lastName};{firstName}\n")

                if nameList:
                    file.write(f"FN:{' '.join(nameList)}\n")
                else:
                    file.write(f"FN:{firstName}\n")

                address = address.replace(";", "\\;", -1)
                address = address.replace("\n", ";", -1)
                address = address.replace(",", " ", -1)

                file.write(f"ADR;HOME:;{address}\n")
                file.write("END:VCARD\n")

            QMessageBox.information(self, "Export Successful",
                f'"{name}" has been exported as a vCard.')
        except Exception as e:
            QMessageBox.information(self, "Export Failed", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    address_book = AddressBook()
    address_book.show()
    sys.exit(app.exec_())
