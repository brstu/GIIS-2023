import sqlite3
import tkinter as tk
db_connect_str = 'D:\\second.db'
conn = sqlite3.connect(db_connect_str)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS mytable (name text, date text)")
conn.commit()
conn.close()

window = tk.Tk()
window.geometry("800x600")

label_name = tk.Label(window, text="Name")
entry_name = tk.Entry(window, font=('Arial', 14))

label_date = tk.Label(window, text="Date")
entry_date = tk.Entry(window, font=('Arial', 14))

button_save = tk.Button(window, text="Save")
button_show = tk.Button(window, text="Show")
button_delete = tk.Button(window, text="Delete")
button_update = tk.Button(window, text="Update")
button_sort = tk.Button(window, text="Sort")


def delete():
    name = entry_name.get()
    conn = sqlite3.connect(db_connect_str)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mytable WHERE name=?", (name,))
    conn.commit()
    conn.close()


def update():
    name = entry_name.get()
    new_age = entry_date.get()

    # Создаем подключение к базе данных
    conn = sqlite3.connect(db_connect_str)
    cursor = conn.cursor()

    cursor.execute("UPDATE mytable SET date=? WHERE name=?", (new_age, name))
    conn.commit()
    conn.close()


def show():
    listbox_name.delete(0, tk.END)
    listbox_date.delete(0, tk.END)
    conn = sqlite3.connect(db_connect_str)
    cursor = conn.cursor()

    # выполняем запрос и получаем результаты
    cursor.execute("SELECT * FROM mytable")
    result = cursor.fetchall()

    for name in result:
        listbox_name.insert(tk.END, name[0])
        listbox_date.insert(tk.END, name[1])


def save_data(name, date):

    # Запись данных в БД
    conn = sqlite3.connect(db_connect_str)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mytable(name, date) VALUES (?, ?)", (name, date))
    conn.commit()
    conn.close()


def on_double_click(event):
    selected_item = listbox_name.get(listbox_name.curselection())
    entry_name.delete(0, tk.END)
    entry_name.insert(tk.END, selected_item)


def sort():
    conn = sqlite3.connect(db_connect_str)
    cursor = conn.cursor()


    names = list(listbox_name.get(0, tk.END))

    names.sort()

    listbox_name.delete(0, tk.END)
    listbox_date.delete(0, tk.END)
    for name in names:
        listbox_name.insert(tk.END, name)

    for name in names:
        cursor.execute("SELECT date FROM mytable WHERE name=?", (name, ))
        result = cursor.fetchall()
        listbox_date.insert(tk.END, result[0])


button_save.config(command=lambda: save_data(entry_name.get(), entry_date.get()), padx=10, pady=10)
button_show.config(command=show, padx=10, pady=10)
button_delete.config(command=delete, padx=10, pady=10)
button_update.config(command=update, padx=10, pady=10)
button_sort.config(command=sort, padx=10, pady=10)
listbox_name = tk.Listbox(window, width=30, height=10)
listbox_name.bind("<Double-Button-1>", on_double_click)
listbox_date = tk.Listbox(window, width=30, height=10)

listbox_name.pack(side=tk.LEFT, padx=10, pady=10)
listbox_date.pack(side=tk.RIGHT, padx=10, pady=10)
label_name.pack()
entry_name.pack()
label_date.pack()
entry_date.pack()
button_save.pack()
button_show.pack()
button_update.pack()
button_delete.pack()
button_sort.pack()

window.mainloop()