import sqlite3
import tkinter as tk
db_connection_str = 'C:/Users/oldbuttrue\Desktop\михно1/base.db'
connection = sqlite3.connect(db_connection_str)
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS mytable (name text, date text)")
connection.commit()
connection.close()

mainWindom = tk.Tk()
mainWindom.geometry("800x600")

Label_imya = tk.Label(mainWindom, text="Name:")
Entrylabel_forname = tk.Entry(mainWindom, font=('Arial', 13))

Label_fordata = tk.Label(mainWindom, text="Date:")
Entry_fordate = tk.Entry(mainWindom, font=('Arial', 13))

Save_button = tk.Button(mainWindom, text="Save info")
Show_button = tk.Button(mainWindom, text="Show info")
Delete_button = tk.Button(mainWindom, text="Delete info")
Update_button = tk.Button(mainWindom, text="Update info")
Sortirovka_button = tk.Button(mainWindom, text="Sortirovka")


def deletedata_function():
    somename = Entrylabel_forname.get()
    connection = sqlite3.connect(db_connection_str)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM mytable WHERE name=?", (somename,))
    connection.commit()
    connection.close()


def updatedata_function():
    somename = Entrylabel_forname.get()
    novaya_data = Entry_fordate.get()
    connection = sqlite3.connect(db_connection_str)
    cursor = connection.cursor()
    cursor.execute("UPDATE mytable SET date=? WHERE name=?", (novaya_data, somename))
    connection.commit()
    connection.close()


def showdata_function():
    Listbox_fornames.delete(0, tk.END)
    Listbox_fordates.delete(0, tk.END)
    connection = sqlite3.connect(db_connection_str)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM mytable")
    result = cursor.fetchall()
    for name in result:
        Listbox_fornames.insert(tk.END, name[0])
        Listbox_fordates.insert(tk.END, name[1])
    connection.close()


def datasave_function(somename, somedate):
    connection = sqlite3.connect(db_connection_str)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO mytable(name, date) VALUES (?, ?)", (somename, somedate))
    connection.commit()
    connection.close()


def dvoinoe_najatie(event):
    vibranniu_element = Listbox_fornames.get(Listbox_fornames.curselection())
    Entrylabel_forname.delete(0, tk.END)
    Entrylabel_forname.insert(tk.END, vibranniu_element)


def sortirovka():
    connection = sqlite3.connect(db_connection_str)
    cursor = connection.cursor()
    names = list(Listbox_fornames.get(0, tk.END))
    names.sort()
    Listbox_fornames.delete(0, tk.END)
    Listbox_fordates.delete(0, tk.END)
    for imya in names:
        Listbox_fornames.insert(tk.END, imya)

    for imya in names:
        cursor.execute("SELECT date FROM mytable WHERE name=?", (imya, ))
        result = cursor.fetchall()
        Listbox_fordates.insert(tk.END, result[0])
    connection.close()


Save_button.config(command=lambda: datasave_function(Entrylabel_forname.get(), Entry_fordate.get()), padx=10, pady=10)
Show_button.config(command=showdata_function, padx=10, pady=10)
Delete_button.config(command=deletedata_function, padx=10, pady=10)
Update_button.config(command=updatedata_function, padx=10, pady=10)
Sortirovka_button.config(command=sortirovka, padx=10, pady=10)
Listbox_fornames = tk.Listbox(mainWindom, width=30, height=10)
Listbox_fornames.bind("<Double-Button-1>", dvoinoe_najatie)
Listbox_fordates = tk.Listbox(mainWindom, width=30, height=10)


Label_imya.grid(row=1, column=0)
Entrylabel_forname.grid(row=1, column=1)
Label_fordata.grid(row=2, column=0)
Entry_fordate.grid(row=2, column=1)
Save_button.grid(row=3, column=0)
Show_button.grid(row=3, column=1)
Update_button.grid(row=4, column=0)
Delete_button.grid(row=4, column=1)
Sortirovka_button.grid(row=5, column=0)
Listbox_fornames.grid(row=6, column=0)
Listbox_fordates.grid(row=6, column=1)


mainWindom.mainloop()