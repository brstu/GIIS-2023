import tkinter as tk
from tkinter import ttk
import sqlite3

class AddressBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Адресная книга")
        self.conn = sqlite3.connect('address_book.db')
        self.c = self.conn.cursor()
        self.name_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.label_name = tk.Label(root, text="Имя:")
        self.entry_name = tk.Entry(root, textvariable=self.name_var)
        self.label_address = tk.Label(root, text="Адрес:")
        self.entry_address = tk.Entry(root, textvariable=self.address_var)
        self.label_phone = tk.Label(root, text="Телефон:")
        self.entry_phone = tk.Entry(root, textvariable=self.phone_var)
        self.tree = ttk.Treeview(root, columns=('ID', 'Name', 'Address', 'Phone'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Имя')
        self.tree.heading('Address', text='Адрес')
        self.tree.heading('Phone', text='Телефон')
        self.button_add = tk.Button(root, text="Добавить", command=self.add_address)
        self.button_edit = tk.Button(root, text="Редактировать", command=self.edit_address)
        self.button_delete = tk.Button(root, text="Удалить", command=self.delete_address)
        self.button_search = tk.Button(root, text="Поиск", command=self.search_addresses)
        self.button_refresh = tk.Button(root, text="Обновить", command=self.load_addresses)
        self.button_refresh.grid(row=7, column=0, columnspan=2, pady=5)
        self.label_name.grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)
        self.label_address.grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.entry_address.grid(row=1, column=1, padx=10, pady=5)
        self.label_phone.grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.entry_phone.grid(row=2, column=1, padx=10, pady=5)
        self.button_add.grid(row=3, column=0, columnspan=2, pady=10)
        self.button_edit.grid(row=4, column=0, columnspan=2, pady=5)
        self.button_delete.grid(row=5, column=0, columnspan=2, pady=5)
        self.button_search.grid(row=6, column=0, columnspan=2, pady=5)
        self.tree.grid(row=0, column=2, rowspan=7, padx=10, pady=10, sticky='nsew')
        self.tree.bind('<ButtonRelease-1>', self.select_address)
        self.load_addresses()

    def add_address(self):
        name = self.name_var.get()
        address = self.address_var.get()
        phone = self.phone_var.get()
        if name and address and phone:
            self.c.execute("INSERT INTO addresses (name, address, phone) VALUES (?, ?, ?)", (name, address, phone))
            self.conn.commit()
            self.load_addresses()
            self.clear_entries()

    def load_addresses(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.c.execute("SELECT * FROM addresses")
        data = self.c.fetchall()
        for row in data:
            self.tree.insert('', 'end', values=row)

    def edit_address(self):
        selected_item = self.tree.selection()
        if selected_item:
            name = self.name_var.get()
            address = self.address_var.get()
            phone = self.phone_var.get()

            if name and address and phone:
                selected_id = self.tree.item(selected_item, 'values')[0]
                self.c.execute("UPDATE addresses SET name=?, address=?, phone=? WHERE id=?", (name, address, phone, selected_id))
                self.conn.commit()
                self.load_addresses()
                self.clear_entries()

    def delete_address(self):
        print('Udalenie poshlo')
        selected_item = self.tree.selection()
        if selected_item:
            selected_id = self.tree.item(selected_item, 'values')[0]
            self.c.execute("DELETE FROM addresses WHERE id=?", (selected_id,))
            self.conn.commit()
            self.load_addresses()
            self.clear_entries()

    def search_addresses(self):
        print('Poisk')
        search_term = self.name_var.get()
        if search_term:
            for row in self.tree.get_children():
                self.tree.delete(row)
            self.c.execute("SELECT * FROM addresses WHERE name LIKE ?", (f'%{search_term}%',))
            data = self.c.fetchall()
            for row in data:
                self.tree.insert('', 'end', values=row)

    def select_address(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.name_var.set(values[1])
            self.address_var.set(values[2])
            self.phone_var.set(values[3])

    def clear_entries(self):
        print('Ochistka entry')
        self.name_var.set('')
        self.address_var.set('')
        self.phone_var.set('')


if __name__ == "__main__":
    print('Poshel process')
    root = tk.Tk()
    app = AddressBookApp(root)
    root.mainloop()
