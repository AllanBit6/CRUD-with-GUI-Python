from tkinter import *
from tkinter import ttk
from sqlite3 import *

#configuracion de la base de datos
conn = connect("base.db")
cr = conn.cursor()

cr.execute('''
           CREATE TABLE IF NOT EXISTS 
           personas(
            id INTEGER,
           nombre TEXT,
           puntaje REAL,

           PRIMARY KEY(id AUTOINCREMENT)
           );''')
conn.commit()

#Creacion de interfaz
root = Tk()
root.title("Hola")

#Creacion de widgets

#Botones
btn1 = Button(root, text="Boton 1", width=20)
btn2 = Button(root, text="Boton 2", width=10)
btn3 = Button(root, text="Boton 3", width=30)
btn4 = Button(root, text="Boton 4", width=10)

#Labels
label1 = Label(root, text = "Label 1")
label2 = Label(root, text = "Label 2")
label3 = Label(root, text = "Label 3")

#Caja de texto
caja1 = Entry(root, width=20)

#Tabla
columns = ["#1", "#2", "#3"]
tabla = ttk.Treeview(root, columns=columns, show="headings")

tabla.heading("#1", text="Columna 1")
tabla.heading("#2", text="Columna 2")
tabla.heading("#3", text="Columna 3")


cr.execute('''SELECT * FROM Personas''')
for row in cr.fetchall():
    tabla.insert("", "end", values=(row[0], row[1], row[2]))


for col in columns:tabla.column(col, width=100, anchor="center")
tabla.grid(column=0, row=4,columnspan=3)

#Posicionamiento de los widgets
btn1.grid(column=0, row=0, columnspan=2, padx=5, pady=5)
btn2.grid(column=2, row=0, padx=5, pady=5)
btn3.grid(column=0, row=1, columnspan=3, padx=5, pady=5)
btn4.grid(column=2, row=3, padx=5, pady=5)

label1.grid(column=0, row=2, padx=5, pady=5)
label2.grid(column=1, row=2, padx=5, pady=5)
label3.grid(column=2, row=2, padx=5, pady=5)

caja1.grid(column=0, row=3, columnspan=2,padx=5, pady=5)

mainloop()