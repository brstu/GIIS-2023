import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QTableWidget, QTableWidgetItem, QMenu, QAction,
    QDialog, QLabel, QLineEdit, QPushButton,
    QMessageBox, QFileDialog, QHBoxLayout
)
from PyQt5.QtCore import Qt, QIODevice, QBuffer
from PyQt5.QtGui import QPixmap
import sqlite3


class ImageDialog(QDialog):
    def __init__(self, material):
        super().__init__()

        self.material = material

        self.setWindowTitle(f"Material: {material}")
        self.setGeometry(100, 100, 400, 400)

        add_button = QPushButton("Add Image", self)
        add_button.clicked.connect(self.addImage)

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button, alignment=Qt.AlignHCenter)

        self.db_connection = sqlite3.connect('images.db')

        self.db_connection.cursor().execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY,
                material TEXT,
                image BLOB
            )
        ''')

        self.initUI()
        self.open_db()

    def initUI(self):
        layout = QVBoxLayout()

        self.image_labels = []

        self.setLayout(layout)

    def open_db(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM images WHERE material = ?", (self.material,))

        results = cursor.fetchall()

        layout = self.layout()

        if results:
            if not (isinstance(results[0], list) or isinstance(results[0], tuple)):
                results = [results]
            for result in results:
                image_data = result[2]
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)

                image_label = QLabel(self)
                image_label.setPixmap(pixmap)
                image_label.setAlignment(Qt.AlignCenter)

                self.image_labels.append(image_label)
            for image_label in self.image_labels:
                layout.addWidget(image_label)
        else:
            self.image_labels = []
            image_label = QLabel(self)
            image_label.setText("No image found in the database.")
            layout.addWidget(image_label)

    def addImage(self):
        try:
            image_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")

            if not image_path:
                return

            cursor = self.db_connection.cursor()
            pixmap = QPixmap(image_path)

            pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            buffer = QBuffer()
            buffer.open(QIODevice.WriteOnly)
            pixmap.save(buffer, "PNG")
            image_bytes = buffer.data()

            cursor.execute("INSERT INTO images (material, image) VALUES (?, ?)", (self.material, image_bytes))
            self.db_connection.commit()

            image_label = QLabel(self)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            layout = self.layout()
            layout.addWidget(image_label)

        except Exception as e:
            print(f"Error: {e}")

class AddDialog(QDialog):
    def __init__(self, parent, item_1, item_2=None):
        super(AddDialog, self).__init__(parent)

        self.setWindowTitle("Add Storehouse")
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        self.name_label = QLabel('Name:')
        self.name_edit = QLineEdit()

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)

        self.item_1_label = QLabel(item_1)
        self.item_1_edit = QLineEdit()

        layout.addWidget(self.item_1_label)
        layout.addWidget(self.item_1_edit)

        if item_2:
            self.item_2_label = QLabel(item_2)
            self.item_2_edit = QLineEdit()

            layout.addWidget(self.item_2_label)
            layout.addWidget(self.item_2_edit)

        self.add_button = QPushButton('Add')
        self.add_button.clicked.connect(self.validate_and_close)

        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def validate_and_close(self):
        space_text = self.item_1_edit.text()

        if not space_text.isdigit():
            QMessageBox.warning(self, 'Invalid Input', 'Second line must be a valid integer.')
        else:
            self.accept()

    def get_data(self):
        name = self.name_edit.text()
        if hasattr(self, 'item_2_edit') and self.item_2_edit:
            item_2 = self.item_2_edit.text()
        else:
            item_2 = 0
        item_1 = int(self.item_1_edit.text()) if self.item_1_edit.text().isdigit() else 0

        return name, item_1, item_2

class MainWnd(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("StorehouseApp")
        self.setGeometry(100, 100, 800, 600)

        self.states = {
            'SH': "Storehouses",
            'M': "Materials"
        }

        self.state = 'SH'

        self.store_house = ""

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.table_widget = QTableWidget(self)

        self.make_table()

        self.table_widget.setContextMenuPolicy(3)  # 3 corresponds to Qt.CustomContextMenu
        self.table_widget.customContextMenuRequested.connect(self.show_context_menu)

        layout.addWidget(self.table_widget)

        central_widget.setLayout(layout)

        self.load_data()

    def make_table(self):
        self.db_connection = sqlite3.connect('storehouses.db')
        self.create_table_if_not_exists()

        self.table_widget.clearContents()
        self.table_widget.setColumnCount(4)

        if self.state == 'SH':
            self.table_widget.setHorizontalHeaderLabels(["ID", "Name", "Location", "Space"])
        if self.state == 'M':
            self.table_widget.setHorizontalHeaderLabels(["ID", "Name", "Stored At", "Mass"])

    def create_table_if_not_exists(self):
        cursor = self.db_connection.cursor()
        if self.state == 'SH':
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Storehouses (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    location TEXT NOT NULL,
                    space INTEGER NOT NULL
                )
            ''')
        if self.state == 'M':
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Materials (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    stored_at TEXT NOT NULL,
                    mass INTEGER NOT NULL
                )
            ''')

        self.db_connection.commit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.open_materials_table()
        elif event.key() == Qt.Key_Delete:
            self.delete_storehouses()

    def load_data(self):
        cursor = self.db_connection.cursor()
        query = 'SELECT * FROM %s'
        cursor.execute(query, (self.states[self.state],))
        data = cursor.fetchall()

        self.table_widget.setRowCount(0)
        for row_num, row_data in enumerate(data):
            self.table_widget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                if col_num == 0:
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table_widget.setItem(row_num, col_num, item)

    def show_context_menu(self, pos):
        context_menu = QMenu(self)

        action = QAction("Add", self)
        action.triggered.connect(self.add)
        context_menu.addAction(action)

        action = QAction("Img", self)
        action.triggered.connect(self.img)
        context_menu.addAction(action)

        action = QAction("Delete", self)
        action.triggered.connect(self.delete_storehouses)
        context_menu.addAction(action)

        action = QAction("Open", self)
        action.triggered.connect(self.open_materials_table)
        context_menu.addAction(action)

        action = QAction("Return", self)
        action.triggered.connect(self.return_table)
        context_menu.addAction(action)

        action = QAction("Save", self)
        action.triggered.connect(self.save_table)
        context_menu.addAction(action)

        context_menu.exec_(self.table_widget.mapToGlobal(pos))

    def add(self):
        if self.state == 'SH':
            dialog = AddDialog(self, "Space", "Location")
        else:
            dialog = AddDialog(self, "Mass")
        result = dialog.exec_()

        if result == QDialog.Accepted:
            name, item_1, item_2 = dialog.get_data()

            cursor = self.db_connection.cursor()
            if self.state == 'SH':
                cursor.execute('''
                    INSERT INTO Storehouses (name, location, space) VALUES (?, ?, ?)
                ''',
                (name,
                item_2,
                item_1))
            elif self.state == 'M':
                cursor.execute('''
                    INSERT INTO Materials (name, stored_at, mass) VALUES (?, ?, ?)
                ''',
                (name,
                self.store_house,
                item_1))
            self.db_connection.commit()

            self.load_data()

    def img(self):
        if self.state == 'M':
            row = self.table_widget.selectionModel().currentIndex().row()
            material = self.table_widget.item(row, 1).text()

            img = ImageDialog(material)

            img.exec_()
        else:
            return

    def delete_storehouses(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()

        if selected_rows:
            reply = QMessageBox.question(
                self,
                'Delete Confirmation',
                'Are you sure you want to delete selected storehouses?',
                QMessageBox.Yes | QMessageBox.No
                )

            if reply == QMessageBox.Yes:
                ids_to_delete = [self.table_widget.item(row.row(), 0).text() for row in selected_rows]
                cursor = self.db_connection.cursor()
                
                # Use parameterized query to prevent SQL injection
                query = 'DELETE FROM {} WHERE id IN ({})'
                cursor.execute(query, (self.states[self.state], ','.join(['%s']*len(ids_to_delete)),))
                
                self.db_connection.commit()

    def open_materials_table(self):

        if self.state == 'SH':
            self.save_table()
            self.state = 'M'
        else:
            return

        row = self.table_widget.selectionModel().currentIndex().row()

        self.store_house = self.table_widget.item(row, 1).text()
        
        self.make_table()

        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM Materials WHERE stored_at = {}', (self.store_house, ))
        data = cursor.fetchall()

        self.table_widget.setRowCount(len(data))

        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                if col_num == 0:
                    item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table_widget.setItem(row_num, col_num, item)

    def return_table(self):
        if self.state == 'M':
            self.save_table()
            self.state = 'SH'
        else:
            return
        
        self.make_table()
        self.load_data()

    def save_table(self):
        cursor = self.db_connection.cursor()

        for row in range(self.table_widget.rowCount()):
            id_item = self.table_widget.item(row, 0)
            name_item = self.table_widget.item(row, 1)
            item_1 = self.table_widget.item(row, 2)
            item_2 = self.table_widget.item(row, 3)

            query = 'SELECT * FROM {} WHERE id = {}'
            cursor.execute(query, (self.states[self.state], int(id_item.text()),))
            existing_record = cursor.fetchone()

            if self.state == 'SH':
                if existing_record:
                    cursor.execute('UPDATE {} SET name = {}, location = {}, space = {} WHERE id = {}',
                    (self.states[self.state], name_item.text(), item_1.text(), int(item_2.text()), int(id_item.text())))
                else:
                    cursor.execute('INSERT INTO {} (id, name, location, space) VALUES ({}, {}, {}, {})',
                    (self.states[self.state], int(id_item.text()), name_item.text(), item_1.text(), int(item_2.text())))
            elif self.state == 'M':
                if existing_record:
                    cursor.execute('UPDATE {} SET name = {}, stored_at = {}, mass = {} WHERE id = {}',
                    (self.states[self.state], name_item.text(), item_1.text(), int(item_2.text()), int(id_item.text())))
                else:
                    cursor.execute('INSERT INTO {} (id, name, stored_at, mass) VALUES ({}, {}, {}, {})',
                    (self.states[self.state], int(id_item.text()), name_item.text(), item_1.text(), int(item_2.text())))

        self.db_connection.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    storehouse_app = MainWnd()
    storehouse_app.show()
    sys.exit(app.exec_())
