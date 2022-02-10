import datetime
import time
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import random



root = Tk()
root.geometry("780x500")
root.resizable(0,0)

ahora = datetime.datetime.now()
Fecha = ahora.strftime('%d-%m-%Y')

nom = StringVar()
ap = StringVar()
dni = IntVar()
horario = []
####
def tiempo(): #marca la hora de salida en base de datos

    hora = time.strftime("%H")
    minuto = time.strftime("%M")
    segundo = time.strftime("%S")
    am_pm = time.strftime("%p")
    hs = hora + ":" + minuto + ":" + segundo + " " + am_pm

##########
    selected = tv.focus()
    clave = tv.item(selected, 'text')
    if (clave == ''):
        messagebox.showwarning("Modificar", "Seleccione un elemento")
    else:
        r = messagebox.askquestion("modificar", "Desea modificar el registro seleccionado")
        if (r == messagebox.YES):
            valores = tv.item(selected, 'values')



            try:
                #solo lo modifica en la bd
                codigo = dni.get()

                Conexion = sqlite3.connect("listaPersonal3.db")
                cursor = Conexion.cursor()
                print(hs)

                horario.append(codigo)
                horario.count(codigo)

                print(horario)  # me muestra la lista
                print(horario.count(codigo))  # me dice la cantidad de veces que se repite un nummero


                if (horario.count(codigo) == 1):
                    print("entro: ")
                    HR = (f"UPDATE Personal SET entrada = '{hs}' WHERE documento = '{valores[1]}'")
                elif (horario.count(codigo) == 2):
                    print("salio: ")
                    HR = (f"UPDATE Personal SET salida = '{hs}' WHERE documento = '{valores[1]}'")

                cursor.execute(HR)  # para modificar aqui es
                Conexion.commit()
                print("guardado")
                Conexion.close()
            except:
                print("fallo")
                #messagebox.showerror("Eliminar", "ocurrio un error con la BD")
###




def ConectarBD():
    Conexion = sqlite3.connect("listaPersonal3.db")

    try:
        Cursor = Conexion.cursor()
        Cursor.execute(
            "CREATE TABLE IF NOT EXISTS Personal (id INTEGER PRIMARY KEY AUTOINCREMENT,nombre VARCHAR(50),apellido VARCHAR(50),documento INTEGER,entrada INTEGER,salida INTEGER)")

        print("tabla creada exitosamente")
    except:
        print("error al crear la tabla")
    Conexion.close()
    pass

def AgredarDatos():
    try:
        Nombre = nom.get()
        Apellido = ap.get()
        Doc = int(dni.get())
        #Id = int(id.get())
        ND = "no definido"

        Conexion = sqlite3.connect("listaPersonal3.db")
        cursor = Conexion.cursor()

        sentencia = "INSERT INTO Personal(nombre,apellido,documento,entrada,salida) VALUES (?,?,?,?,?)"
        cursor.execute(sentencia, [Nombre,Apellido,Doc,ND,ND])
        Conexion.commit()
        print("Guardado correctamente")

    except Exception as err:
        print("error al ingresar datos a la tabla",err)



#####

##
tv = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4", "col5", "col6"))

tv.column("#0", width=50)
tv.column("col1", width=90, anchor=CENTER)
tv.column("col2", width=90, anchor=CENTER)
tv.column("col3", width=90, anchor=CENTER)
tv.column("col4", width=90, anchor=CENTER)
tv.column("col5", width=90, anchor=CENTER)
tv.column("col6", width=90, anchor=CENTER)


    # encabezado

tv.heading("#0", text="Id", anchor=CENTER)
tv.heading("col1", text="Fecha", anchor=CENTER)
tv.heading("col2", text="Documento", anchor=CENTER)
tv.heading("col3", text="Nombre", anchor=CENTER)
tv.heading("col4", text="Apellido", anchor=CENTER)
tv.heading("col5", text="Hora Entrada", anchor=CENTER)
tv.heading("col6", text="Hora Salida", anchor=CENTER)

tv.place(x=50, y=100)



###
def mostrarDatos():
    i = 1
    Conexion = sqlite3.connect("listaPersonal3.db")
    cursor = Conexion.cursor()

    registros=tv.get_children()
    for registro in registros:
        tv.delete(registro)

    cursor.execute(f"SELECT `documento`,`nombre`,`apellido`,`entrada`,`salida`   FROM `Personal`")

    for (documento,nombre,apellido,entrada ,salida ) in cursor:

        tv.insert('',i,text=str(i),values=(Fecha,documento,nombre,apellido,entrada ,salida ))
        i = i + 1
####
def verLista():
    i = 1

    Nombre = nom.get()
    Apellido = ap.get()
    Doc = dni.get()
    nd = "No definido"
    nds = "No definido"


    tv.insert("", END,text=str(i), values=(f"{Fecha}", f"{Doc}", f"{Nombre}", f"{Apellido}", f"{nd}", f"{nds}"))
    mostrarDatos()
####
def NuevaVentana(): #ventana donde agregamos los datos del nuevo empleado

    ventana_nueva = Toplevel()
    ventana_nueva.geometry("300x200")
    ventana_nueva.title("Nuevo empleado")

    entryNombre = Label(ventana_nueva, text="Nombre")
    entryNombre.place(x=10,y=30)
    entryNombre = Entry(ventana_nueva, textvariable=nom)
    entryNombre.place(x=80,y=30)


    entryApellido = Label(ventana_nueva, text="Apellido")
    entryApellido.place(x=10,y=60)
    entryApellido = Entry(ventana_nueva, textvariable=ap)
    entryApellido.place(x=80,y=60)

    labelDni = Label(ventana_nueva, text="Dni")
    labelDni.place(x=10,y=90)
    entryDni = Entry(ventana_nueva, textvariable=dni)
    entryDni.place(x=80,y=90)


    entryNombre.focus()
    entryNombre.delete(0, "end")
    entryApellido.delete(0, "end")
    entryDni.delete(0, "end")


    def Salir():

        ventana_nueva.destroy()

    btn1 = Button(ventana_nueva, text="ingresar", command=lambda:[AgredarDatos(),verLista(),Salir()])

    btn1.place(x=50,y=130)


####
def eliminar():
    selected = tv.focus()

    clave = tv.item(selected,'text')

    Conexion = sqlite3.connect("listaPersonal3.db")

    if(clave == ''):
        messagebox.showwarning("eliminar","seleccione elemento")
        print("seleccione elemento")
    else:
        #print(clave)
        valores = tv.item(selected, 'values')
        print(valores[1])


        r = messagebox.askquestion("Eliminar","desea eliminar el registro seleccionado")

        if(r == messagebox.YES):
            try:
                cursor=Conexion.cursor()
                cursor.execute(f"DELETE FROM Personal WHERE documento = '{valores[1]}'")
                Conexion.commit()
                Conexion.close()
                selected_item = tv.selection()[0]
                tv.delete(selected_item)
                messagebox.showinfo("Eliminar", "Eliminado correctamente")
            except:
                messagebox.showerror("Eliminar", "ocurrio un error con la BD")


####

def VentanaEditar(): #ventana donde agregamos los datos del nuevo empleado

    selected = tv.focus()

    clave = tv.item(selected, 'text')

    if (clave == ''):
        messagebox.showwarning("Modificar", "seleccione un elemento")

    else:

        r = messagebox.askquestion("modificar", "desea modificar el registro seleccionado")

        if (r == messagebox.YES):
            valores = tv.item(selected, 'values')
            #print(valores[3])#ape
            #print(valores[2])#nom
            #print(valores[1])#doc

            ventana_nueva = Toplevel()
            ventana_nueva.geometry("300x200")
            ventana_nueva.title("Editar Dato")


            labelNombre = Label(ventana_nueva, text="Nombre")
            labelNombre.place(x=10,y=30)

            entryNombre = Entry(ventana_nueva, textvariable=nom)
            entryNombre.place(x=80,y=30)

            labelApellido = Label(ventana_nueva, text="Apellido")
            labelApellido.place(x=10,y=60)

            entryApellido = Entry(ventana_nueva, textvariable=ap)
            entryApellido.place(x=80,y=60)

            labelDni = Label(ventana_nueva, text="Dni")
            labelDni.place(x=10,y=90)

            entryDni = Entry(ventana_nueva, textvariable=dni)
            entryDni.place(x=80,y=90)

            entryNombre.focus()
            entryNombre.delete(0, "end")
            entryNombre.delete(0, "end")
            entryDni.delete(0, "end")


            selected = tv.focus()

            values = tv.item(selected, 'values')

            entryNombre.insert(0, values[2])
            entryApellido.insert(0, values[3])
            entryDni.insert(0, values[1])




    def Salir():
        entryNombre.delete(0, "end")
        ventana_nueva.destroy()

    def actualizar():
        selected = tv.focus()


        tv.item(selected, values=(f"{Fecha}",entryDni.get(),entryNombre.get(),  entryApellido.get()))


        edit = entryNombre.get()

        #####
        try:
            Conexion = sqlite3.connect("listaPersonal3.db")
            cursor = Conexion.cursor()
            cursor.execute(f"UPDATE Personal SET nombre = '{edit}' WHERE documento = '{valores[1]}'") #para modificar aqui es

            Conexion.commit()
            print("guardado")
            Conexion.close()
        except:
            #print("no se pude guardar")
            messagebox.showerror("Error", "ocurrio un error con la BD")

        ##
        messagebox.showinfo(message="modificado correctamente", title="Exito")

        entryNombre.delete(0, "end")
        entryApellido.delete(0, "end")
        entryDni.delete(0, "end")

    btn1 = Button(ventana_nueva, text="Guardar",command = lambda:[actualizar(),Salir()])
    btn1.place(x=50,y=130)



btnEliminar = Button(root,text="Eliminar",command = eliminar)
btnEliminar.place(x=160,y=60)

btnAgregar = Button(root,text="Agregar Nuevo",command = NuevaVentana)
btnAgregar.place(x=50,y=60)


btnModificar = Button(root,text="Modificar",command = lambda:[VentanaEditar()])
btnModificar.place(x=230,y=60)

btnControlHorario = Button(root,text="Control Horarios",command = lambda:[VentanaEditar(tiempo(),mostrarDatos())])
btnControlHorario.place(x=320,y=60)


ConectarBD()
mostrarDatos()
root.mainloop()