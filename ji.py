import pymysql
import random
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk


def conexion():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='ignorancia'
    )
    return conn


def reiniciar_puntos():
    conn = conexion()
    cursor = conn.cursor()
    sql = "UPDATE usuario SET puntos = 0"
    cursor.execute(sql)
    conn.commit()
    conn.close()


def recupera_categoria():
    conn = conexion()
    cursor = conn.cursor()
    sql = "SELECT descripcion FROM categoria"
    cursor.execute(sql)
    datos = cursor.fetchall()
    conn.close()
    return datos


def recupera_preguntas(categoria):
    conn = conexion()
    cursor = conn.cursor()
    sql = """
    SELECT
        p.id_pregunta,
        p.pregunta,
        p.opcion_1,
        p.opcion_2,
        p.opcion_3,
        p.opcion_4,
        p.correcto
    FROM pregunta p
    INNER JOIN categoria c
    ON p.id_categoria = c.id_categoria
    WHERE c.descripcion = %s
    """
    cursor.execute(sql, (categoria,))
    datos = cursor.fetchall()
    conn.close()
    return datos


def recupera_usuarios():
    conn = conexion()
    cursor = conn.cursor()
    sql = "SELECT * FROM usuario"
    cursor.execute(sql)
    datos = cursor.fetchall()
    conn.close()
    return datos


def tabla_puntos():
    usuarios = recupera_usuarios()
    ventana = Toplevel(pantalla)
    ventana.title("🏆 Tabla de Puntos")
    ventana.geometry("500x350")
    ventana.config(bg="#ffb6c1")

    titulo = Label(
        ventana,
        text="TABLA DE PUNTOS :3!",
        font=("Helvetica", 22, "bold"),
        bg="#ffb6c1",
        fg="black"
    )
    titulo.pack(pady=20)

    marco = Frame(
        ventana,
        bg="white",
        bd=3,
        relief="ridge"
    )
    marco.pack(padx=20, pady=10, fill="both", expand=True)

    for usuario in usuarios:
        texto = f"{usuario[1]}    -   {usuario[2]} puntos"
        lbl = Label(
            marco,
            text=texto,
            font=("Helvetica", 16, "bold"),
            bg="white",
            fg="black",
            pady=10
        )
        lbl.pack(fill="x")


def sumar_punto(jugador):
    conn = conexion()
    cursor = conn.cursor()
    sql = "UPDATE usuario SET puntos = puntos + 1 WHERE nombre = %s"
    cursor.execute(sql, (jugador,))
    conn.commit()
    conn.close()


def asignar_puntos():
    posiciones = []
    posiciones.append(("Jugador 1", x1))
    posiciones.append(("Jugador 2", x2))
    posiciones.append(("Jugador 3", x3))
    posiciones.sort(key=lambda x: x[1], reverse=True)

    conn = conexion()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE usuario SET puntos = puntos + 3 WHERE nombre=%s",
        (posiciones[0][0],)
    )
    cursor.execute(
        "UPDATE usuario SET puntos = puntos + 2 WHERE nombre=%s",
        (posiciones[1][0],)
    )
    cursor.execute(
        "UPDATE usuario SET puntos = puntos + 1 WHERE nombre=%s",
        (posiciones[2][0],)
    )

    conn.commit()
    conn.close()


reiniciar_puntos()

# Ventana principal
pantalla = Tk()
pantalla.resizable(1, 1)
pantalla.geometry("1280x788")
pantalla.config(background="Pink")
pantalla.title("Juego de la Ignorancia")

canvas = Canvas(
    pantalla,
    width=1200,
    height=600,
    bg="Pink",
    highlightthickness=0
)
canvas.place(x=40, y=180)

img_pista = Image.open("fondo2.png")
img_pista = img_pista.resize((1200, 600))
fon = ImageTk.PhotoImage(img_pista)
canvas.create_image(0, 0, image=fon, anchor="nw")

# Variables globales
seleccion = ()
str_preg = StringVar()
str_res1 = StringVar()
str_res2 = StringVar()
str_res3 = StringVar()
str_res4 = StringVar()
str_sig = StringVar()
correcto = 0
x1 = 10
x2 = 10
x3 = 10
x4 = 10
turno = 1
nombre_j1 = StringVar()
nombre_j2 = StringVar()
nombre_j3 = StringVar()
juego_iniciado = False


def seleccionar_jugador():
    global juego_iniciado
    if juego_iniciado:
        messagebox.showwarning(
            "Bloqueado",
            "No puedes cambiar jugadores durante la partida"
        )
        return

    nombre_j1.set(entry1.get())
    nombre_j2.set(entry2.get())
    nombre_j3.set(entry3.get())

    if nombre_j1.get() == "":
        nombre_j1.set("Jugador 1")
    if nombre_j2.get() == "":
        nombre_j2.set("Jugador 2")
    if nombre_j3.get() == "":
        nombre_j3.set("Jugador 3")

    str_sig.set(nombre_j1.get())
    juego_iniciado = True

    boton_guardar.config(state=DISABLED)
    entry1.config(state=DISABLED)
    entry2.config(state=DISABLED)
    entry3.config(state=DISABLED)


def mostrar_ganador(nombre):
    ventana = Toplevel(pantalla)
    ventana.title("GANADOR")
    ventana.geometry("500x300")
    ventana.config(bg="#edffb7")

    titulo = Label(
        ventana,
        text="¡TENEMOS GANADOR!",
        font=("Helvetica", 24, "bold"),
        bg="#edffb7",
        fg="black"
    )
    titulo.pack(pady=30)

    mensaje = Label(
        ventana,
        text=f"{nombre} ganó la carrera",
        font=("Helvetica", 20, "bold"),
        bg="#edffb7",
        fg="black"
    )
    mensaje.pack(pady=20)

    boton = Button(
        ventana,
        text="Salir",
        font=("Helvetica", 16, "bold"),
        bg="black",
        fg="pink",
        command=pantalla.destroy
    )
    boton.pack(pady=30)


def verificar_ganador():
    global x1, x2, x3, x4
    if x1 >= 1000:
        mostrar_ganador("Jugador 1")
    elif x2 >= 1000:
        mostrar_ganador("Jugador 2")
    elif x3 >= 1000:
        mostrar_ganador("Jugador 3")
    elif x4 >= 1000:
        mostrar_ganador("Ignorancia")


def siguiente_turno():
    global turno
    turno += 1
    if turno > 3:
        turno = 1

    if turno == 1:
        str_sig.set(nombre_j1.get())
    elif turno == 2:
        str_sig.set(nombre_j2.get())
    elif turno == 3:
        str_sig.set(nombre_j3.get())


def actualizar_turno():
    if turno == 1:
        str_sig.set(nombre_j1.get())
    elif turno == 2:
        str_sig.set(nombre_j2.get())
    elif turno == 3:
        str_sig.set(nombre_j3.get())


def avanza_jug():
    global x1, x2, x3
    if turno == 1:
        x1 = x1 + 100
        canvas.coords(j1, x1, 120)
        sumar_punto("Jugador 1")
    elif turno == 2:
        x2 = x2 + 100
        canvas.coords(j2, x2, 250)
        sumar_punto("Jugador 2")
    elif turno == 3:
        x3 = x3 + 100
        canvas.coords(j3, x3, 380)
        sumar_punto("Jugador 3")


def opc1():
    global turno, x4
    r1.config(state=DISABLED)
    r2.config(state=DISABLED)
    r3.config(state=DISABLED)
    r4.config(state=DISABLED)
    if correcto == 1:
        avanza_jug()
    else:
        x4 = x4 + 100
        canvas.coords(j4, x4, 510)
    verificar_ganador()
    siguiente_turno()


def opc2():
    global turno, x4
    r1.config(state=DISABLED)
    r2.config(state=DISABLED)
    r3.config(state=DISABLED)
    r4.config(state=DISABLED)
    if correcto == 2:
        avanza_jug()
    else:
        x4 = x4 + 100
        canvas.coords(j4, x4, 510)
    verificar_ganador()
    siguiente_turno()


def opc3():
    global turno, x4
    r1.config(state=DISABLED)
    r2.config(state=DISABLED)
    r3.config(state=DISABLED)
    r4.config(state=DISABLED)
    if correcto == 3:
        avanza_jug()
    else:
        x4 = x4 + 100
        canvas.coords(j4, x4, 510)
    verificar_ganador()
    siguiente_turno()


def opc4():
    global turno, x4
    r1.config(state=DISABLED)
    r2.config(state=DISABLED)
    r3.config(state=DISABLED)
    r4.config(state=DISABLED)
    if correcto == 4:
        avanza_jug()
    else:
        x4 = x4 + 100
        canvas.coords(j4, x4, 510)
    verificar_ganador()
    siguiente_turno()


def sel_preg():
    global str_preg, correcto
    tam = len(seleccion)
    if tam != 0:
        n = random.randint(0, tam - 1)
        str_preg.set(seleccion[n][1])
        str_res1.set(seleccion[n][2])
        str_res2.set(seleccion[n][3])
        str_res3.set(seleccion[n][4])
        str_res4.set(seleccion[n][5])
        correcto = seleccion[n][6]
        r1.config(state=NORMAL)
        r2.config(state=NORMAL)
        r3.config(state=NORMAL)
        r4.config(state=NORMAL)
    else:
        str_preg.set('Categoria sin preguntas')
        str_res1.set('')
        str_res2.set('')
        str_res3.set('')
        str_res4.set('')
        r1.config(state=DISABLED)
        r2.config(state=DISABLED)
        r3.config(state=DISABLED)
        r4.config(state=DISABLED)


def preguntas(event):
    global seleccion
    cat = event.widget.get()
    cat = str(cat).replace("_", " ")
    seleccion = recupera_preguntas(cat)
    sel_preg()


def pregunta_sig():
    global seleccion
    cat = categorias.get()
    cat = str(cat).replace("_", " ")
    seleccion = recupera_preguntas(cat)
    sel_preg()


# Cargar categorías
l_cats = recupera_categoria()
cats = []
for cat in l_cats:
    cats.append(cat[0])

# Elementos de la interfaz
eti = Label(pantalla, bg="Pink", text="Categoria", font='Helvetica 18 bold')
eti.place(x=10, y=10)

categorias = ttk.Combobox(pantalla, font='Helvetica 18 bold')
pantalla.option_add("TComboboxListbox.font", ("Helvetica", 18))
categorias['values'] = cats
categorias.place(x=150, y=10)
categorias.bind("<<ComboboxSelected>>", preguntas)

Label(pantalla, text="Jugador 1", bg="Pink", font='Helvetica 12 bold').place(x=930, y=10)
entry1 = Entry(pantalla, font='Helvetica 12 bold')
entry1.place(x=930, y=40)

Label(pantalla, text="Jugador 2", bg="Pink", font='Helvetica 12 bold').place(x=930, y=70)
entry2 = Entry(pantalla, font='Helvetica 12 bold')
entry2.place(x=930, y=100)

Label(pantalla, text="Jugador 3", bg="Pink", font='Helvetica 12 bold').place(x=930, y=130)
entry3 = Entry(pantalla, font='Helvetica 12 bold')
entry3.place(x=930, y=160)

boton_guardar = Button(
    pantalla,
    text="Guardar jugadores",
    command=seleccionar_jugador,
    bg="Black",
    fg="Pink",
    font='Helvetica 12 bold'
)
boton_guardar.place(x=930, y=200)

btn_puntos = Button(
    pantalla,
    text="Tabla de puntos",
    command=tabla_puntos,
    font='Helvetica 14 bold',
    bg="Black",
    fg="Pink"
)
btn_puntos.place(x=1140, y=10)

sig = Button(
    pantalla,
    text="Siguiente",
    command=pregunta_sig,
    font='Helvetica 14 bold',
    bg="Pink"
)
sig.place(x=750, y=10)

str_sig.set('Jugador 1')
sig_jug = Label(pantalla, bg="Pink", textvariable=str_sig, font='Helvetica 18 bold')
sig_jug.place(x=500, y=10)

eti = Label(pantalla, bg="Pink", text="Pregunta", font='Helvetica 16 bold')
eti.place(x=5, y=60)

str_preg.set("")
pre = Entry(
    pantalla,
    textvariable=str_preg,
    font='Helvetica 14 bold',
    bg="Lavender",
    width=50,
    state=DISABLED
)
pre.place(x=110, y=60)

str_res1.set("")
r1 = Button(
    pantalla,
    textvariable=str_res1,
    command=opc1,
    font='Helvetica 14 bold',
    bg="Black",
    fg="Pink",
    width=20
)
r1.place(x=40, y=150)

str_res2.set("")
r2 = Button(
    pantalla,
    textvariable=str_res2,
    command=opc2,
    font='Helvetica 14 bold',
    bg="Black",
    fg="Pink",
    width=20
)
r2.place(x=260, y=150)

str_res3.set("")
r3 = Button(
    pantalla,
    textvariable=str_res3,
    command=opc3,
    font='Helvetica 14 bold',
    bg="Black",
    fg="Pink",
    width=20
)
r3.place(x=480, y=150)

str_res4.set("")
r4 = Button(
    pantalla,
    textvariable=str_res4,
    command=opc4,
    font='Helvetica 14 bold',
    bg="Black",
    fg="Pink",
    width=20
)
r4.place(x=670, y=150)

# Imágenes de los carros/personajes
img1 = Image.open("Carro1.png")
img1 = img1.resize((80, 80))
ju1 = ImageTk.PhotoImage(img1)

img2 = Image.open("Carro2.png")
img2 = img2.resize((80, 80))
ju2 = ImageTk.PhotoImage(img2)

img3 = Image.open("Carro3.png")
img3 = img3.resize((80, 80))
ju3 = ImageTk.PhotoImage(img3)

img4 = Image.open("Gatobuho.png")
img4 = img4.resize((80, 80))
ju4 = ImageTk.PhotoImage(img4)

j1 = canvas.create_image(60, 120, image=ju1)
j2 = canvas.create_image(60, 250, image=ju2)
j3 = canvas.create_image(60, 380, image=ju3)
j4 = canvas.create_image(60, 510, image=ju4)

pantalla.mainloop()