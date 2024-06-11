#----------------------Proyecto Final--------------------------------


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sqlite3 import *

#------------------------Base de datos y CRUD------------------------

#Creacion de la base

conn = connect('base.db')
cr = conn.cursor()
cr.execute('''CREATE TABLE IF NOT EXISTS Personas(
           id INTEGER,
           nombre TEXT,
           promedio REAL,

           PRIMARY KEY (id AUTOINCREMENT)
           );''')
conn.commit()


def insertarDB(nom, prom):
    cr.execute('''
    INSERT INTO Personas(nombre, promedio)
    VALUES(?, ?)''', (nom, prom))
    conn.commit()

def modificarDB(id, nom, prom):
    cr.execute('''
    UPDATE Personas 
    SET nombre = ?, promedio = ?
    WHERE id = ?''', (nom, prom, id))
    conn.commit()

def eliminarDB(id):
    cr.execute('''DELETE FROM Personas WHERE id = ?''', (id,))
    conn.commit()

#Funcion para la abrir la ventana de insertar
def ventanaInsertar():

    emergente = Toplevel(root)
    emergente.geometry("300x200")
    emergente.title("Insertar nuevo registro")
    emergente.grab_set()

    cajaNombre = Entry(emergente, width=20)
    cajaPromedio = Entry(emergente, width=20)

    label2 = Label(emergente, text="Nombre")
    label3 = Label(emergente, text="Promedio")

    btn5 = Button(emergente, text="Aceptar",
                   command=lambda: (insertarDB(cajaNombre.get(), float(cajaPromedio.get())),
                                    emergente.destroy()
                                    , messagebox.showinfo("Exito", "Agregado exitosamente")))
    
    label2.pack()
    cajaNombre.pack()

    label3.pack()
    cajaPromedio.pack()
    btn5.pack()
    
#Funcion para abrir la ventana de modificar
def ventanaModificar():

    seleccion = []
    seleccion_indices = tabla.selection()
    for indice in seleccion_indices:
        item = tabla.item(indice)
        valores = item['values']
        seleccion.append(valores)

    if seleccion.__len__() == 0:
        messagebox.showerror("Ningun registro", 
                            "No hay un registro seleccionado")
    else:
        sel = seleccion[0]
        print(sel)
        emergente = Toplevel(root)
        emergente.title("Modificar Registros")
        emergente.geometry("300x200")
        emergente.grab_set()

        cajaNombre = Entry(emergente, width=20)
        cajaPromedio = Entry(emergente, width=20)

        cajaNombreV = Entry(emergente, width=20)
        cajaNombreV.insert(0, sel[1])
        cajaNombreV.config(state="disabled")

        cajaPromedioV = Entry(emergente, width=20)
        cajaPromedioV.insert(0, sel[2])
        cajaPromedioV.config(state="disabled")


        label2 = Label(emergente, text="Nuevo Nombre")
        label3 = Label(emergente, text="Nuevo Promedio")
        btn5 = Button(emergente, text="Aceptar", 
                      command=lambda: (modificarDB(int(sel[0]), cajaNombre.get(), float(cajaPromedio.get())), 
                                       emergente.destroy(), 
                                       messagebox.showinfo("Exito", "Modificado exitosamente")))
        
        label2.pack()
        cajaNombreV.pack()
        cajaNombre.pack()

        label3.pack()
        cajaPromedioV.pack()
        cajaPromedio.pack()
        btn5.pack()

#Funcion para abrir la ventana Eliminar
def ventanaEliminar():

    seleccion = []
    seleccion_indices = tabla.selection()
    for indice in seleccion_indices:
        item = tabla.item(indice)
        valores = item['values']
        seleccion.append(valores)

    if seleccion.__len__() == 0:
        messagebox.showerror("Ningun registro", "No hay un registro seleccionado")
    else:
        
        sel = seleccion[0]
        
        emergente = Toplevel(root)
        emergente.title("Eliminar Registros")
        emergente.geometry("300x200")
        emergente.grab_set()

        cajaNombreV = Entry(emergente, width=20)
        cajaNombreV.insert(0, sel[1])
        cajaNombreV.config(state="disabled")

        cajaPromedioV = Entry(emergente, width=20)
        cajaPromedioV.insert(0, sel[2])
        cajaPromedioV.config(state="disabled")

        label2 = Label(emergente, text="¿Está seguro de que quiere eliminar el registro?")
        btn5 = Button(emergente, text="Aceptar", 
                      command=lambda:(eliminarDB(int(sel[0])), 
                                      emergente.destroy(), 
                                        messagebox.showinfo("Exito", "Eliminado exitosamente")))
        btn6 = Button(emergente, text="Cancelar", 
                      command=emergente.destroy)

        cajaNombreV.pack()
        cajaPromedioV.pack()
        label2.pack()
        btn5.pack() 
        btn6.pack() 

#Declaracion de funcion para refrescar tabla
def actualizar_tabla():
    # Guardar los IDs de las filas seleccionadas
    seleccionIds = [tabla.item(indice)['values'][0] for indice in tabla.selection()]

    # Actualizar la tabla (borrar y volver a insertar datos)
    tabla.delete(*tabla.get_children())

    # Alimentar la tabla con la base de datos
    cr.execute('''SELECT * FROM Personas''')
    datos = cr.fetchall()

    # Insertar los nuevos datos y guardar un mapa de IDs a items
    id_a_item = {}
    for row in datos:
        item_id = tabla.insert("", "end", values=(row[0], row[1], row[2]))
        id_a_item[row[0]] = item_id

    # Volver a seleccionar los registros previamente seleccionados
    for id_ in seleccionIds:
        item_id = id_a_item.get(id_)
        if item_id:
            tabla.selection_add(item_id)
    
    # Programar la próxima actualización después de 1000 ms (1 segundo)
    root.after(1000, actualizar_tabla)



#Ventana principal
root = Tk()
root.title("Punto de venta")
root.resizable(width=False, height=False)
root.iconbitmap('logoTeczion.ico')





#------------------------------------Widgets-------------------------
#Botones
btn1 = Button(root, text="Insertar", width=20, command=ventanaInsertar)
btn2 = Button(root, text="Modificar", width=20, command = ventanaModificar)
btn3 = Button(root, text="Eliminar", width=20, command=ventanaEliminar)
btn4 = Button(root, text="Salir", width=20, command=root.destroy)

#Label
label1 = Label(root, text="Registro de estudiantes", 
               font=('Helvetica', 16))

#Treeview
columns = ["#1", "#2", "#3"]
tabla = ttk.Treeview(root, columns=columns, show="headings")

tabla.heading("#1", text="ID")
tabla.heading("#2", text="Nombre")
tabla.heading("#3", text="Promedio")

#Redimensionar la tabla
for col in columns:
    tabla.column(col, width=220, anchor="center")

# Crear un scrollbar vertical y asociarlo al Treeview
scrollTabla= Scrollbar(root, orient="vertical", command=tabla.yview)
scrollTabla.grid(row=2, column=4, sticky='ns')
tabla.configure(yscrollcommand=scrollTabla.set)

#--------------Posicionamiento de widgets-------------
label1.grid(column=0, row=0, columnspan=4)
btn1.grid(column=0, row=1, padx=5, pady=5)
btn2.grid(column=1, row=1, padx=5, pady=5)
btn3.grid(column=2, row=1, padx=5, pady=5)
btn4.grid(column=3, row=1, padx=5, pady=5)
tabla.grid(column=0, row=2, columnspan=4, padx=5, pady=5)


#-----------------Proceso de refrescamiento de la tabla---------------
actualizar_tabla()

#-----------------Declaracion del bucle principal--------------------
root.mainloop()
