import tkinter as tk
from tkinter import messagebox

import math

COLOR_FONDO = "#0B1D26"
COLOR_PANEL = "#183A37"
COLOR_PANEL_CLARO = "#244E4A"
COLOR_BOTON = "#D9A441"
COLOR_BOTON_OSCURO = "#B9892F"
COLOR_TEXTO = "#F5F1E3"
COLOR_ENTRADA = "#F7F7F7"
COLOR_OSCURO = "#102522"
COLOR_ERROR = "#A63D40"

ventana = None
menu_lateral = None
contenido = None

#--------------------
#FUNCIONES REQUERIDAS
#---------------------

def listar_paises(mapa):
    paises = []
    for pais in mapa:
        nombre_pais = pais[0]
        paises+=[nombre_pais]

    return paises


def listar_estados(mapa, pais):
    estados = []

    for pais_actual in mapa:
        nombre_pais = pais_actual[0]

        if nombre_pais == pais:
            lista_estados = pais_actual[1]

            for estado in lista_estados:
                nombre_estado = estado[0]
                estados.append(nombre_estado)

            return estados
    return estados

def listar_condados(mapa, pais, estado):
    condados = []

    for pais_actual in mapa:
        if pais_actual[0] == pais:
            for estado_actual in pais_actual[1]:
                if estado_actual[0] == estado:
                    for condado in estado_actual[1]:
                        condados.append(condado[0])
                    return condados
    return condados

def minerales_en_condado(mapa, pais, estado, condado):
    for pais_actual in mapa:
        if pais_actual[0] == pais:
            for estado_actual in pais_actual[1]:
                if estado_actual[0] == estado:
                    for condado_actual in estado_actual[1]:
                        if condado_actual[0] == condado:
                            return condado_actual[2]
    return []

def agregar_mineral_a_condado(mapa, pais, estado, condado, nombre_mineral):
    for pais_actual in mapa:
        if pais_actual[0] == pais:
            for estado_actual in pais_actual[1]:
                if estado_actual[0] == estado:
                    for condado_actual in estado_actual[1]:
                        if condado_actual[0] == condado:
                            if nombre_mineral not in condado_actual[2]:
                                condado_actual[2].append(nombre_mineral)
                                guardar_mapa()
                                return True
                            return False

    return False

def eliminar_mineral_de_condado(mapa, pais, estado, condado, nombre_mineral):
    for pais_actual in mapa:
        if pais_actual[0] == pais:
            for estado_actual in pais_actual[1]:
                if estado_actual[0] == estado:
                    for condado_actual in estado_actual[1]:
                        if condado_actual[0] == condado:
                            if nombre_mineral in condado_actual[2]:
                                condado_actual[2].remove(nombre_mineral)
                                guardar_mapa()
                                return True
                            return False

    return False

def agregar_condado(mapa, pais, estado, nombre_condado, coordenadas, minerales):
    for pais_actual in mapa:
        if pais_actual[0] == pais:
            for estado_actual in pais_actual[1]:
                if estado_actual[0] == estado:
                    for condado_actual in estado_actual[1]:
                        if condado_actual[0] == nombre_condado:
                            return False

                    nuevo_condado = [nombre_condado, coordenadas, minerales]
                    estado_actual[1].append(nuevo_condado)
                    guardar_mapa()
                    return True

    return False

def eliminar_condado(mapa, pais, estado, nombre_condado):
    for pais_actual in mapa:
        if pais_actual[0] == pais:
            for estado_actual in pais_actual[1]:
                if estado_actual[0] == estado:
                    for condado_actual in estado_actual[1]:
                        if condado_actual[0] == nombre_condado:
                            estado_actual[1].remove(condado_actual)
                            guardar_mapa()
                            return True

    return False


def coordenadas_a_decimal(coord):
    grados = coord[0]
    minutos = coord[1]
    segundos = coord[2]

    if grados < 0:
        decimal = grados - minutos / 60 - segundos / 3600
    else:
        decimal = grados + minutos / 60 + segundos / 3600
    return decimal


def buscar_condado_por_coordenadas(mapa, longitud, latitud):
    longitud_decimal = coordenadas_a_decimal(longitud)
    latitud_decimal = coordenadas_a_decimal(latitud)

    for pais_actual in mapa:
        for estado_actual in pais_actual[1]:
            for condado_actual in estado_actual[1]:
                coordenadas = condado_actual[1]

                punto1 = coordenadas[0]
                punto2 = coordenadas[1]

                longitud1 = coordenadas_a_decimal(punto1[0])
                latitud1 = coordenadas_a_decimal(punto1[1])

                longitud2 = coordenadas_a_decimal(punto2[0])
                latitud2 = coordenadas_a_decimal(punto2[1])

                longitud_minima = min(longitud1, longitud2)
                longitud_maxima = max(longitud1, longitud2)

                latitud_minima = min(latitud1, latitud2)
                latitud_maxima = max(latitud1, latitud2)

                if longitud_minima <= longitud_decimal <= longitud_maxima and latitud_minima <= latitud_decimal <= latitud_maxima:
                    return [
                        pais_actual[0],
                        estado_actual[0],
                        condado_actual[0]
                    ]

    return False

def area_de_condado(condado):
    coordenadas = condado[1]

    punto1 = coordenadas[0]
    punto2 = coordenadas[1]

    longitud1 = coordenadas_a_decimal(punto1[0])
    latitud1 = coordenadas_a_decimal(punto1[1])

    longitud2 = coordenadas_a_decimal(punto2[0])
    latitud2 = coordenadas_a_decimal(punto2[1])

    diferencia_longitud = abs(longitud2 - longitud1)
    diferencia_latitud = abs(latitud2 - latitud1)

    latitud_promedio = (latitud1 + latitud2) / 2

    alto = diferencia_latitud * 111
    ancho = diferencia_longitud * 111 * math.cos(math.radians(latitud_promedio))

    area = alto * ancho

    return area


def hay_traslape(condado1, condado2):
    coordenadas1 = condado1[1]
    punto1_1 = coordenadas1[0]
    punto1_2 = coordenadas1[1]

    longitud1_1 = coordenadas_a_decimal(punto1_1[0])
    latitud1_1 = coordenadas_a_decimal(punto1_1[1])
    longitud1_2 = coordenadas_a_decimal(punto1_2[0])
    latitud1_2 = coordenadas_a_decimal(punto1_2[1])

    longitud_minima1 = min(longitud1_1, longitud1_2)
    longitud_maxima1 = max(longitud1_1, longitud1_2)
    latitud_minima1 = min(latitud1_1, latitud1_2)
    latitud_maxima1 = max(latitud1_1, latitud1_2)

    coordenadas2 = condado2[1]
    punto2_1 = coordenadas2[0]
    punto2_2 = coordenadas2[1]

    longitud2_1 = coordenadas_a_decimal(punto2_1[0])
    latitud2_1 = coordenadas_a_decimal(punto2_1[1])
    longitud2_2 = coordenadas_a_decimal(punto2_2[0])
    latitud2_2 = coordenadas_a_decimal(punto2_2[1])

    longitud_minima2 = min(longitud2_1, longitud2_2)
    longitud_maxima2 = max(longitud2_1, longitud2_2)
    latitud_minima2 = min(latitud2_1, latitud2_2)
    latitud_maxima2 = max(latitud2_1, latitud2_2)

    if longitud_maxima1 <= longitud_minima2:
        return False

    if longitud_minima1 >= longitud_maxima2:
        return False

    if latitud_maxima1 <= latitud_minima2:
        return False

    if latitud_minima1 >= latitud_maxima2:
        return False

    return True

def verificar_traslapes():
    condados = []
    traslapes = []

    for pais_actual in mapa:
        for estado_actual in pais_actual[1]:
            for condado_actual in estado_actual[1]:
                condados.append([
                    pais_actual[0],
                    estado_actual[0],
                    condado_actual
                ])

    for i in range(len(condados)):
        for j in range(i + 1, len(condados)):
            condado1 = condados[i][2]
            condado2 = condados[j][2]

            if hay_traslape(condado1, condado2):
                traslapes.append([
                    [condados[i][0], condados[i][1], condado1[0]],
                    [condados[j][0], condados[j][1], condado2[0]]
                ])

    return traslapes


def condado_con_mas_minerales():
    condado_mayor = []
    mayor_cantidad = 0

    for pais_actual in mapa:
        for estado_actual in pais_actual[1]:
            for condado_actual in estado_actual[1]:
                cantidad_minerales = len(condado_actual[2])

                if cantidad_minerales > mayor_cantidad:
                    mayor_cantidad = cantidad_minerales
                    condado_mayor = [
                        pais_actual[0],
                        estado_actual[0],
                        condado_actual[0],
                        mayor_cantidad
                    ]

    return condado_mayor


def total_minerales_distintos():
    minerales_distintos = []

    for pais_actual in mapa:
        for estado_actual in pais_actual[1]:
            for condado_actual in estado_actual[1]:
                for mineral in condado_actual[2]:
                    if mineral not in minerales_distintos:
                        minerales_distintos.append(mineral)

    return len(minerales_distintos)



def minerales_por_pais():
    resultado = []

    for pais_actual in mapa:
        minerales_distintos = []

        for estado_actual in pais_actual[1]:
            for condado_actual in estado_actual[1]:
                for mineral in condado_actual[2]:
                    if mineral not in minerales_distintos:
                        minerales_distintos.append(mineral)

        resultado.append([
            pais_actual[0],
            len(minerales_distintos)
        ])

    return resultado
# ---------------------------------------------------------
# ARCHIVO DEL MAPA
# El mapa ahora se carga desde mapa.txt
# ---------------------------------------------------------

FILE_PATH_MAPA = 'mapa.txt'
mapa = []


# I: path, access_mode: append, override, valor a escribir
def write_file(path, access_mode, string):
    mode = 'a' if access_mode.upper() == 'APPEND' else 'w'
    with open(path, mode,encoding="utf-8") as file:
        file.write(string)


# I: path
def read_file(path):
    with open(path, 'r',encoding="utf-8") as file:
        return file.read()


# Guarda el mapa completo en el archivo
def guardar_mapa():
    write_file(FILE_PATH_MAPA, 'w', str(mapa))


# Lee mapa.txt y carga la lista en memoria
def cargar_mapa():
    try:
        global mapa
        strValue = read_file(FILE_PATH_MAPA)
        mapa = eval(strValue)
    except:
        mapa = []

def recargar_mapa_archivo():
    cargar_mapa()
    messagebox.showinfo("Mapa cargado", "El mapa fue cargado desde mapa.txt")


# ---------------------------------------------------------
# LÓGICA DEL JUEGO - PLAYERS
# ---------------------------------------------------------

import random
from datetime import datetime

FILE_PATH_PLAYERS = "players.txt"
players = []

jugador_actual = ""
intentos_restantes = 0
ubicacion_actual = []
minerales_actuales = []


def guardar_players():
    write_file(FILE_PATH_PLAYERS, "w", str(players))


def cargar_players():
    try:
        global players
        strValue = read_file(FILE_PATH_PLAYERS)

        if strValue.strip() == "":
            players = []
        else:
            players = eval(strValue)
    except:
        players = []


def buscar_player(nombre):
    for player in players:
        if player[0] == nombre:
            return player
    return []


def crear_player(nombre):
    global players

    if nombre.strip() == "":
        return False

    player = buscar_player(nombre)

    if player == []:
        nuevo_player = [nombre, []]
        players.append(nuevo_player)
        guardar_players()

    return True


def obtener_capturas_player(nombre):
    player = buscar_player(nombre)

    if player != []:
        return player[1]

    return []


def obtener_minerales_capturados(nombre):
    capturas = obtener_capturas_player(nombre)
    minerales = []

    for captura in capturas:
        mineral = captura[0]

        if mineral not in minerales:
            minerales.append(mineral)

    return minerales


def mineral_ya_capturado(nombre, mineral):
    minerales = obtener_minerales_capturados(nombre)

    if mineral in minerales:
        return True

    return False


def registrar_captura(nombre, mineral, pais, estado, condado):
    player = buscar_player(nombre)

    if player == []:
        return False

    if mineral_ya_capturado(nombre, mineral):
        return False

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    captura = [mineral, pais, estado, condado, fecha]

    player[1].append(captura)
    guardar_players()

    return True


def iniciar_partida(nombre):
    global jugador_actual
    global intentos_restantes
    global ubicacion_actual
    global minerales_actuales

    if nombre.strip() == "":
        return False

    crear_player(nombre)

    jugador_actual = nombre
    intentos_restantes = random.randint(5, 10)
    ubicacion_actual = []
    minerales_actuales = []

    return True


def intentar_coordenada(longitud, latitud):
    global intentos_restantes
    global ubicacion_actual
    global minerales_actuales

    if intentos_restantes <= 0:
        return "SIN_INTENTOS"

    intentos_restantes = intentos_restantes - 1

    resultado = buscar_condado_por_coordenadas(mapa, longitud, latitud)

    if resultado == False:
        ubicacion_actual = []
        minerales_actuales = []
        return "NO_ENCONTRADO"

    pais = resultado[0]
    estado = resultado[1]
    condado = resultado[2]

    minerales = minerales_en_condado(mapa, pais, estado, condado)
    minerales_no_capturados = []

    for mineral in minerales:
        if mineral_ya_capturado(jugador_actual, mineral) == False:
            minerales_no_capturados.append(mineral)

    ubicacion_actual = [pais, estado, condado]
    minerales_actuales = minerales_no_capturados

    if minerales_no_capturados == []:
        return "SIN_MINERALES_NUEVOS"

    return "ENCONTRADO"


def capturar_mineral(mineral):
    if jugador_actual == "":
        return False

    if ubicacion_actual == []:
        return False

    if mineral not in minerales_actuales:
        return False

    pais = ubicacion_actual[0]
    estado = ubicacion_actual[1]
    condado = ubicacion_actual[2]

    resultado = registrar_captura(jugador_actual, mineral, pais, estado, condado)

    return resultado

# ---------------------------------------------------------
# INTERFAZ VISUAL DEL JUEGO OFICIAL
# Pegar después de la lógica del juego y antes del llamado final
# ---------------------------------------------------------

def limpiar_juego():
    for widget in area_juego.winfo_children():
        widget.destroy()
        


def mostrar_texto_juego(texto):
    texto_juego.config(state="normal")
    texto_juego.delete("1.0", tk.END)
    texto_juego.insert(tk.END, texto)
    texto_juego.config(state="disabled")


def actualizar_info_juego():
    label_jugador_juego.config(text="Jugador: " + jugador_actual)
    label_intentos_juego.config(text="Intentos: " + str(intentos_restantes))


def obtener_limites_mapa_juego():
    longitudes = []
    latitudes = []

    for pais in mapa:
        for estado in pais[1]:
            for condado in estado[1]:
                punto1 = condado[1][0]
                punto2 = condado[1][1]

                longitudes.append(coordenadas_a_decimal(punto1[0]))
                latitudes.append(coordenadas_a_decimal(punto1[1]))

                longitudes.append(coordenadas_a_decimal(punto2[0]))
                latitudes.append(coordenadas_a_decimal(punto2[1]))

    return min(longitudes), max(longitudes), min(latitudes), max(latitudes)


def convertir_pixel_juego(longitud, latitud, lon_min, lon_max, lat_min, lat_max, ancho, alto):
    margen = 30

    x = margen + ((longitud - lon_min) * (ancho - margen * 2) / (lon_max - lon_min))
    y = alto - margen - ((latitud - lat_min) * (alto - margen * 2) / (lat_max - lat_min))

    return x, y


def dibujar_mapa_juego():
    canvas_juego.delete("all")
    canvas_juego.update_idletasks()

    ancho = canvas_juego.winfo_width()
    alto = canvas_juego.winfo_height()

    if ancho <= 1:
        ancho = 820

    if alto <= 1:
        alto = 335

    if mapa == []:
        canvas_juego.create_text(ancho / 2, alto / 2,
                                 text="Mapa vacío",
                                 fill="white",
                                 font=("Arial", 14, "bold"))
        return

    lon_min, lon_max, lat_min, lat_max = obtener_limites_mapa_juego()

    if lon_max == lon_min:
        lon_max = lon_max + 1

    if lat_max == lat_min:
        lat_max = lat_max + 1

    colores = ["#F6C85F", "#8DD17E", "#6F9FD8", "#F08A5D", "#B8D8BA", "#E5989B"]
    contador = 0

    canvas_juego.create_rectangle(0, 0, ancho, alto, fill="white", outline="")

    for pais in mapa:
        for estado in pais[1]:
            for condado in estado[1]:
                punto1 = condado[1][0]
                punto2 = condado[1][1]

                lon1 = coordenadas_a_decimal(punto1[0])
                lat1 = coordenadas_a_decimal(punto1[1])
                lon2 = coordenadas_a_decimal(punto2[0])
                lat2 = coordenadas_a_decimal(punto2[1])

                x1, y1 = convertir_pixel_juego(lon1, lat1, lon_min, lon_max, lat_min, lat_max, ancho, alto)
                x2, y2 = convertir_pixel_juego(lon2, lat2, lon_min, lon_max, lat_min, lat_max, ancho, alto)

                x_menor = min(x1, x2)
                x_mayor = max(x1, x2)
                y_menor = min(y1, y2)
                y_mayor = max(y1, y2)

                color = colores[contador % len(colores)]
                contador = contador + 1

                canvas_juego.create_rectangle(x_menor, y_menor, x_mayor, y_mayor,
                                               fill=color,
                                               outline="white",
                                               width=1)

                centro_x = (x_menor + x_mayor) / 2
                centro_y = (y_menor + y_mayor) / 2

                canvas_juego.create_text(centro_x, centro_y,
                                         text=condado[0],
                                         fill="black",
                                         font=("Arial", 8, "bold"))


def marcar_punto_juego(longitud, latitud):
    canvas_juego.delete("punto")
    canvas_juego.update_idletasks()

    ancho = canvas_juego.winfo_width()
    alto = canvas_juego.winfo_height()

    if ancho <= 1:
        ancho = 820

    if alto <= 1:
        alto = 335

    lon_min, lon_max, lat_min, lat_max = obtener_limites_mapa_juego()

    if lon_max == lon_min:
        lon_max = lon_max + 1

    if lat_max == lat_min:
        lat_max = lat_max + 1

    lon_decimal = coordenadas_a_decimal(longitud)
    lat_decimal = coordenadas_a_decimal(latitud)

    x, y = convertir_pixel_juego(lon_decimal, lat_decimal, lon_min, lon_max, lat_min, lat_max, ancho, alto)

    canvas_juego.create_oval(x - 7, y - 7, x + 7, y + 7,
                             fill=COLOR_ERROR,
                             outline="white",
                             width=2,
                             tags="punto")
    
def mostrar_botones_juego_iniciado():
    boton_partida_juego.pack(pady=7)
    boton_historial_juego.pack(pady=7)

def limpiar_sesion_juego():
    global jugador_actual
    global intentos_restantes
    global ubicacion_actual
    global minerales_actuales

    jugador_actual = ""
    intentos_restantes = 0
    ubicacion_actual = []
    minerales_actuales = []
def comenzar_juego_inicio():
    global entrada_nombre_inicio

    nombre = entrada_nombre_inicio.get().strip()

    if nombre == "":
        messagebox.showerror("Error", "Debe ingresar un nombre.")
        return

    jugador_existente = buscar_player(nombre)

    resultado = iniciar_partida(nombre)

    if resultado:
        mostrar_botones_juego_iniciado()

        if jugador_existente != []:
            messagebox.showinfo("Jugador encontrado", "Bienvenido de nuevo, " + nombre + ".")
        else:
            messagebox.showinfo("Jugador creado", "Bienvenido, " + nombre + ".")

        pantalla_partida()
    else:
        messagebox.showerror("Error", "No se pudo iniciar la partida.")
def pantalla_inicio_juego():
    global entrada_nombre_inicio

    limpiar_juego()

    panel_resultado.pack_forget()

    titulo = tk.Label(area_juego, text="Mineral Hunter",
                      bg=COLOR_FONDO, fg=COLOR_BOTON,
                      font=("Arial", 32, "bold"))
    titulo.pack(pady=(45, 8))

    subtitulo = tk.Label(area_juego,
                         text="Ingresa tu cuenta para comenzar la exploración.",
                         bg=COLOR_FONDO, fg=COLOR_TEXTO,
                         font=("Arial", 13))
    subtitulo.pack(pady=(0, 25))

    panel = tk.Frame(area_juego, bg=COLOR_PANEL_CLARO, width=560, height=240)
    panel.pack(pady=15)
    panel.pack_propagate(False)

    contenido = tk.Frame(panel, bg=COLOR_PANEL_CLARO)
    contenido.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(contenido, text="Acceso del jugador",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
             font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 18))

    tk.Label(contenido, text="Nombre:",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
             font=("Arial", 12, "bold")).grid(row=1, column=0, padx=(0, 12), pady=8, sticky="e")

    entrada_nombre_inicio = tk.Entry(contenido,
                                     bg=COLOR_ENTRADA,
                                     width=24,
                                     font=("Arial", 13),
                                     justify="center")
    entrada_nombre_inicio.grid(row=1, column=1, pady=8, ipady=4)
    entrada_nombre_inicio.focus()

    tk.Label(contenido,
             text="Si la cuenta no existe, se creará una nueva.",
             bg=COLOR_PANEL_CLARO, fg=COLOR_BOTON,
             font=("Arial", 10, "bold")).grid(row=2, column=0, columnspan=2, pady=(14, 18))

    tk.Button(contenido, text="Iniciar partida",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 12, "bold"),
              width=18, height=2,
              command=comenzar_juego_inicio).grid(row=3, column=0, columnspan=2, pady=(0, 5))
def buscar_partida_interfaz():
    lista_minerales_juego.delete(0, tk.END)

    longitud = leer_coordenada(entrada_longitud_juego.get())
    latitud = leer_coordenada(entrada_latitud_juego.get())

    if longitud == False or latitud == False:
        messagebox.showerror("Error", "Use el formato grados,minutos,segundos.")
        return

    resultado = intentar_coordenada(longitud, latitud)
    actualizar_info_juego()
    marcar_punto_juego(longitud, latitud)

    if resultado == "SIN_INTENTOS":
        mostrar_texto_juego("Ya no tienes intentos disponibles.")
        return

    if resultado == "NO_ENCONTRADO":
        mostrar_texto_juego("No se encontró ningún condado en esa coordenada.")
        return

    if resultado == "SIN_MINERALES_NUEVOS":
        texto = "Ubicación encontrada:\n"
        texto = texto + ubicacion_actual[0] + "  |  " + ubicacion_actual[1] + "  |  " + ubicacion_actual[2] + "\n\n"
        texto = texto + "Este condado no tiene minerales nuevos para capturar."
        mostrar_texto_juego(texto)
        return

    if resultado == "ENCONTRADO":
        texto = "Ubicación encontrada:\n"
        texto = texto + ubicacion_actual[0] + "  |  " + ubicacion_actual[1] + "  |  " + ubicacion_actual[2] + "\n\n"
        texto = texto + "Selecciona un mineral de la lista y presiona Capturar."

        mostrar_texto_juego(texto)

        for mineral in minerales_actuales:
            lista_minerales_juego.insert(tk.END, mineral)


def capturar_partida_interfaz():
    seleccion = lista_minerales_juego.curselection()

    if seleccion == ():
        messagebox.showerror("Error", "Seleccione un mineral.")
        return

    mineral = lista_minerales_juego.get(seleccion[0])
    resultado = capturar_mineral(mineral)

    if resultado:
        messagebox.showinfo("Captura realizada", "Capturaste: " + mineral)
        lista_minerales_juego.delete(seleccion[0])

        mostrar_texto_juego("Mineral capturado:\n" +
                            mineral + "\n\nUbicación:\n" +
                            ubicacion_actual[0] + "  |  " +
                            ubicacion_actual[1] + "  |  " +
                            ubicacion_actual[2])
    else:
        messagebox.showerror("Error", "No se pudo capturar el mineral.")

def pantalla_partida():
    global label_jugador_juego
    global label_intentos_juego
    global canvas_juego
    global lista_minerales_juego
    global entrada_longitud_juego
    global entrada_latitud_juego

    if jugador_actual == "":
        pantalla_inicio_juego()
        return

    limpiar_juego()

    panel_resultado.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(5, 18))

    encabezado = tk.Frame(area_juego, bg=COLOR_FONDO)
    encabezado.pack(fill="x", padx=25, pady=(15, 5))

    tk.Label(encabezado, text="Partida actual",
             bg=COLOR_FONDO, fg=COLOR_BOTON,
             font=("Arial", 23, "bold")).pack(side=tk.LEFT)

    datos = tk.Frame(encabezado, bg=COLOR_FONDO)
    datos.pack(side=tk.RIGHT)

    label_jugador_juego = tk.Label(datos, text="Jugador: ",
                                   bg=COLOR_FONDO, fg=COLOR_TEXTO,
                                   font=("Arial", 11, "bold"))
    label_jugador_juego.pack(anchor="e")

    label_intentos_juego = tk.Label(datos, text="Intentos: ",
                                    bg=COLOR_FONDO, fg=COLOR_TEXTO,
                                    font=("Arial", 11, "bold"))
    label_intentos_juego.pack(anchor="e")

    actualizar_info_juego()

    panel_mapa = tk.Frame(area_juego, bg=COLOR_PANEL_CLARO)
    panel_mapa.pack(fill="x", padx=25, pady=(10, 8))

    tk.Label(panel_mapa, text="Mapa de exploración",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
             font=("Arial", 15, "bold")).pack(pady=(10, 6))

    canvas_juego = tk.Canvas(panel_mapa,
                             width=820,
                             height=335,
                             bg="white",
                             highlightthickness=0)
    canvas_juego.pack(padx=15, pady=(0, 15))

    dibujar_mapa_juego()

    panel_control = tk.Frame(area_juego, bg=COLOR_PANEL_CLARO)
    panel_control.pack(fill="x", padx=25, pady=(0, 8))

    bloque_busqueda = tk.Frame(panel_control, bg=COLOR_PANEL_CLARO)
    bloque_busqueda.grid(row=0, column=0, padx=15, pady=12, sticky="w")

    tk.Label(bloque_busqueda, text="Buscar coordenada",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
             font=("Arial", 13, "bold")).grid(row=0, column=0, columnspan=4, pady=(0, 8))

    tk.Label(bloque_busqueda, text="Longitud:",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
             font=("Arial", 10)).grid(row=1, column=0, padx=6, pady=5, sticky="e")

    entrada_longitud_juego = tk.Entry(bloque_busqueda,
                                      bg=COLOR_ENTRADA,
                                      width=18,
                                      font=("Arial", 10))
    entrada_longitud_juego.grid(row=1, column=1, padx=6, pady=5)

    tk.Label(bloque_busqueda, text="Latitud:",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
             font=("Arial", 10)).grid(row=1, column=2, padx=6, pady=5, sticky="e")

    entrada_latitud_juego = tk.Entry(bloque_busqueda,
                                     bg=COLOR_ENTRADA,
                                     width=18,
                                     font=("Arial", 10))
    entrada_latitud_juego.grid(row=1, column=3, padx=6, pady=5)

    tk.Label(bloque_busqueda, text="Formato: grados,minutos,segundos",
             bg=COLOR_PANEL_CLARO, fg=COLOR_BOTON,
             font=("Arial", 9, "bold")).grid(row=2, column=0, columnspan=4, pady=(2, 8))

    tk.Button(bloque_busqueda, text="Buscar",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 10, "bold"),
              width=14, height=2,
              command=buscar_partida_interfaz).grid(row=3, column=1, padx=8, pady=(0, 5))

    tk.Button(bloque_busqueda, text="Capturar",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 10, "bold"),
              width=14, height=2,
              command=capturar_partida_interfaz).grid(row=3, column=2, padx=8, pady=(0, 5))

    bloque_minerales = tk.Frame(panel_control, bg=COLOR_PANEL_CLARO)
    bloque_minerales.grid(row=0, column=1, padx=25, pady=12, sticky="e")

    tk.Label(bloque_minerales, text="Minerales disponibles",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
             font=("Arial", 13, "bold")).pack(pady=(0, 8))

    lista_minerales_juego = tk.Listbox(bloque_minerales,
                                       width=30,
                                       height=5,
                                       bg=COLOR_ENTRADA,
                                       fg="black",
                                       font=("Arial", 10))
    lista_minerales_juego.pack()

    panel_control.grid_columnconfigure(0, weight=1)
    panel_control.grid_columnconfigure(1, weight=1)


def pantalla_historial_juego():
    if jugador_actual == "":
        pantalla_inicio_juego()
        return
    limpiar_juego()
    panel_resultado.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(5, 18))

    titulo = tk.Label(area_juego, text="Historial de capturas",
                      bg=COLOR_FONDO, fg=COLOR_BOTON,
                      font=("Arial", 22, "bold"))
    titulo.pack(anchor="w", padx=25, pady=(25, 8))

    panel = tk.Frame(area_juego, bg=COLOR_PANEL_CLARO)
    panel.pack(padx=25, pady=15)

    tk.Label(panel, text="Nombre del jugador:",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
             font=("Arial", 15, "bold")).grid(row=0, column=0, padx=10, pady=12)

    entrada_nombre = tk.Entry(panel, bg=COLOR_ENTRADA, width=24, font=("Arial", 11))
    entrada_nombre.grid(row=0, column=1, padx=10, pady=12)

    if jugador_actual != "":
        entrada_nombre.insert(0, jugador_actual)

    def consultar_historial():
        nombre = entrada_nombre.get().strip()

        if nombre == "":
            messagebox.showerror("Error", "Ingrese un nombre.")
            return

        capturas = obtener_capturas_player(nombre)

        if capturas == []:
            mostrar_texto_juego("Este jugador no tiene capturas registradas.")
            return

        texto = "Capturas de " + nombre + "\n"
        texto = texto + "-" * 70 + "\n\n"

        for captura in capturas:
            texto = texto + captura[0] + "  |  "
            texto = texto + captura[1] + "  |  "
            texto = texto + captura[2] + "  |  "
            texto = texto + captura[3] + "  |  "
            texto = texto + captura[4] + "\n"

        mostrar_texto_juego(texto)

    tk.Button(panel, text="Consultar",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 11, "bold"),
              width=16, height=2,
              command=consultar_historial).grid(row=1, column=0, columnspan=2, pady=(0, 12))


def iniciar_interfaz_juego():
    global ventana_juego
    global area_juego
    global texto_juego
    global boton_partida_juego
    global boton_historial_juego
    global panel_resultado
    limpiar_sesion_juego()

    ventana_juego = tk.Tk()
    ventana_juego.title("Mineral Global Tracker - Juego")
    ventana_juego.geometry("1180x780")
    ventana_juego.config(bg=COLOR_FONDO)

    menu = tk.Frame(ventana_juego, bg=COLOR_PANEL, width=220)
    menu.pack(side=tk.LEFT, fill=tk.Y)

    zona_derecha = tk.Frame(ventana_juego, bg=COLOR_FONDO)
    zona_derecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    tk.Label(menu, text="MINERAL\nHUNTER",
             bg=COLOR_PANEL, fg=COLOR_BOTON,
             font=("Arial", 21, "bold"),
             justify="center").pack(pady=(25, 5))

    tk.Button(menu, text="Inicio",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 11, "bold"),
              width=17, height=2,
              command=pantalla_inicio_juego).pack(pady=7)

    boton_partida_juego = tk.Button(menu, text="Partida",
                                    bg=COLOR_BOTON, fg=COLOR_OSCURO,
                                    activebackground=COLOR_BOTON_OSCURO,
                                    font=("Arial", 11, "bold"),
                                    width=17, height=2,
                                    command=pantalla_partida)

    boton_historial_juego = tk.Button(menu, text="Historial",
                                      bg=COLOR_BOTON, fg=COLOR_OSCURO,
                                      activebackground=COLOR_BOTON_OSCURO,
                                      font=("Arial", 11, "bold"),
                                      width=17, height=2,
                                      command=pantalla_historial_juego)

    tk.Button(menu, text="Salir",
              bg=COLOR_ERROR, fg=COLOR_TEXTO,
              activebackground=COLOR_ERROR,
              font=("Arial", 11, "bold"),
              width=17, height=2,
              command=volver_menu_desde_juego).pack(pady=(30, 10))

    area_juego = tk.Frame(zona_derecha, bg=COLOR_FONDO)
    area_juego.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    panel_resultado = tk.Frame(zona_derecha, bg=COLOR_OSCURO)
    panel_resultado.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(5, 18))

    tk.Label(panel_resultado, text="Información",
             bg=COLOR_OSCURO, fg=COLOR_BOTON,
             font=("Arial", 13, "bold")).pack(anchor="w", padx=12, pady=(8, 0))

    frame_texto = tk.Frame(panel_resultado, bg=COLOR_OSCURO)
    frame_texto.pack(fill=tk.X, padx=12, pady=10)

    scroll = tk.Scrollbar(frame_texto)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    texto_juego = tk.Text(frame_texto,
                          height=9,
                          bg=COLOR_ENTRADA,
                          fg="black",
                          font=("Consolas", 10),
                          relief="flat",
                          yscrollcommand=scroll.set,
                          wrap="none")
    texto_juego.pack(side=tk.LEFT, fill=tk.X, expand=True)

    scroll.config(command=texto_juego.yview)
    texto_juego.config(state="disabled")

    pantalla_inicio_juego()

    ventana_juego.mainloop()


def volver_menu_desde_juego():
    limpiar_sesion_juego()
    ventana_juego.destroy()
    iniciar_menu_principal()


# ---------------------------------------------------------
# MENÚ PRINCIPAL
# ---------------------------------------------------------

def abrir_juego():
        ventana_menu.destroy()
        iniciar_interfaz_juego()

def abrir_mantenimiento():
    ventana_menu.destroy()
    iniciar_interfaz_mantenimiento()

def iniciar_menu_principal():
    global ventana_menu

    ventana_menu = tk.Tk()
    ventana_menu.title("Mineral Global Tracker")
    ventana_menu.geometry("600x430")
    ventana_menu.config(bg=COLOR_FONDO)

    tk.Label(ventana_menu, text="MINERAL GLOBAL TRACKER",
             bg=COLOR_FONDO, fg=COLOR_BOTON,
             font=("Arial", 25, "bold")).pack(pady=(45, 8))
    

    tk.Button(ventana_menu, text="Juego",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 13, "bold"),
              width=20, height=2,
              command=abrir_juego).pack(pady=10)

    tk.Button(ventana_menu, text="Mantenimiento",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 13, "bold"),
              width=20, height=2,
              command=abrir_mantenimiento).pack(pady=10)

    tk.Button(ventana_menu, text="Salir",
              bg=COLOR_ERROR, fg=COLOR_TEXTO,
              activebackground=COLOR_ERROR,
              font=("Arial", 13, "bold"),
              width=20, height=2,
              command=ventana_menu.destroy).pack(pady=10)

    ventana_menu.mainloop()

# ---------------------------------------------------------
# FUNCIONES DE APOYO PARA LA INTERFAZ
# ---------------------------------------------------------

def limpiar_area_trabajo():
    for widget in area_trabajo.winfo_children():
        widget.destroy()


def texto_normal(texto):
    return texto.strip()


def formatear_fila(dato):
    if type(dato) == list:
        texto = ""
        for elemento in dato:
            if type(elemento) == list:
                if texto != "":
                    texto = texto + "  |  "
                texto = texto + formatear_fila(elemento)
            else:
                if texto != "":
                    texto = texto + "  |  "
                texto = texto + str(elemento)
        return texto
    else:
        return str(dato)


def mostrar_resultado(titulo, dato):
    caja_resultado.config(state="normal")
    caja_resultado.delete("1.0", tk.END)

    caja_resultado.insert(tk.END, titulo + "\n")
    caja_resultado.insert(tk.END, "-" * 90 + "\n\n")

    if dato == [] or dato == False or dato == None:
        caja_resultado.insert(tk.END, "No se encontraron datos.")
    else:
        if type(dato) == list:
            if len(dato) > 0 and type(dato[0]) == list:
                for fila in dato:
                    caja_resultado.insert(tk.END, formatear_fila(fila) + "\n")
            else:
                if titulo == "Condado encontrado" or titulo == "Condado con más minerales":
                    caja_resultado.insert(tk.END, formatear_fila(dato))
                else:
                    for elemento in dato:
                        caja_resultado.insert(tk.END, str(elemento) + "\n")
        else:
            caja_resultado.insert(tk.END, str(dato))

    caja_resultado.config(state="disabled")


def leer_coordenada(texto):
    partes = texto.split(",")

    if len(partes) != 3:
        return False

    try:
        grados = int(partes[0].strip())
        minutos = int(partes[1].strip())
        segundos = int(partes[2].strip())
        return [grados, minutos, segundos]
    except:
        return False


def leer_minerales(texto):
    minerales = []
    partes = texto.split(",")

    for mineral in partes:
        mineral = mineral.strip()
        if mineral != "":
            minerales.append(mineral)

    return minerales


def buscar_condado_completo(pais, estado, condado):
    for pais_actual in mapa:
        if pais_actual[0] == pais:
            for estado_actual in pais_actual[1]:
                if estado_actual[0] == estado:
                    for condado_actual in estado_actual[1]:
                        if condado_actual[0] == condado:
                            return condado_actual
    return False


def buscar_por_coordenadas_interfaz(longitud, latitud):
    try:
        return buscar_condado_por_coordenadas(mapa, longitud, latitud)
    except:
        return buscar_condado_por_coordenadas(longitud, latitud)


# ---------------------------------------------------------
# PANTALLA: NAVEGACIÓN
# ---------------------------------------------------------

def pantalla_navegacion():
    limpiar_area_trabajo()

    titulo = tk.Label(area_trabajo, text="Navegación y visualización",
                      bg=COLOR_FONDO, fg=COLOR_BOTON,
                      font=("Arial", 22, "bold"))
    titulo.pack(anchor="w", padx=25, pady=(18, 5))

    panel = tk.Frame(area_trabajo, bg=COLOR_PANEL_CLARO)
    panel.pack(fill="x", padx=25, pady=8)

    bloque_paises = tk.LabelFrame(panel, text="Listar países",
                                  bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
                                  font=("Arial", 15, "bold"))
    bloque_paises.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")


    tk.Button(bloque_paises, text="Mostrar Países",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 10, "bold"),
              width=20, height=2,
              command=lambda: mostrar_resultado("Países registrados", listar_paises(mapa))).pack(pady=8)

    bloque_estados = tk.LabelFrame(panel, text="Listar estados",
                                   bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
                                   font=("Arial", 15, "bold"))
    bloque_estados.grid(row=0, column=1, padx=12, pady=12, sticky="nsew")

    tk.Label(bloque_estados, text="País:",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
             font=("Arial", 10)).grid(row=0, column=0, padx=8, pady=8, sticky="w")

    entrada_pais_estados = tk.Entry(bloque_estados, bg=COLOR_ENTRADA, width=22,
                                    font=("Arial", 13))
    entrada_pais_estados.grid(row=0, column=1, padx=8, pady=8)

    tk.Button(bloque_estados, text="Mostrar Estados",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 10, "bold"),
              width=20, height=2,
              command=lambda: mostrar_resultado("Estados encontrados",
                                                listar_estados(mapa, texto_normal(entrada_pais_estados.get())))).grid(row=1, column=1, pady=8)

    bloque_condados = tk.LabelFrame(panel, text="Listar condados",
                                    bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
                                    font=("Arial", 15, "bold"))
    bloque_condados.grid(row=1, column=0, padx=12, pady=12, sticky="nsew")

    tk.Label(bloque_condados, text="País:",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
             font=("Arial", 10)).grid(row=0, column=0, padx=8, pady=6, sticky="w")

    entrada_pais_condados = tk.Entry(bloque_condados, bg=COLOR_ENTRADA, width=22,
                                     font=("Arial", 11))
    entrada_pais_condados.grid(row=0, column=1, padx=8, pady=6)

    tk.Label(bloque_condados, text="Estado:",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
             font=("Arial", 10)).grid(row=1, column=0, padx=8, pady=6, sticky="w")

    entrada_estado_condados = tk.Entry(bloque_condados, bg=COLOR_ENTRADA, width=22,
                                       font=("Arial", 11))
    entrada_estado_condados.grid(row=1, column=1, padx=8, pady=6)

    tk.Button(bloque_condados, text="Mostrar Condados",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 10, "bold"),
              width=20, height=2,
              command=lambda: mostrar_resultado("Condados encontrados",
                                                listar_condados(mapa,
                                                                texto_normal(entrada_pais_condados.get()),
                                                                texto_normal(entrada_estado_condados.get())))).grid(row=2, column=1, pady=8)

    bloque_minerales = tk.LabelFrame(panel, text="Minerales en condado",
                                     bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
                                     font=("Arial", 15, "bold"))
    bloque_minerales.grid(row=1, column=1, padx=12, pady=12, sticky="nsew")

    tk.Label(bloque_minerales, text="País:",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
             font=("Arial", 10)).grid(row=0, column=0, padx=8, pady=5, sticky="w")

    entrada_pais_minerales = tk.Entry(bloque_minerales, bg=COLOR_ENTRADA, width=22,
                                      font=("Arial", 11))
    entrada_pais_minerales.grid(row=0, column=1, padx=8, pady=5)

    tk.Label(bloque_minerales, text="Estado:",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
             font=("Arial", 10)).grid(row=1, column=0, padx=8, pady=5, sticky="w")

    entrada_estado_minerales = tk.Entry(bloque_minerales, bg=COLOR_ENTRADA, width=22,
                                        font=("Arial", 11))
    entrada_estado_minerales.grid(row=1, column=1, padx=8, pady=5)

    tk.Label(bloque_minerales, text="Condado:",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
             font=("Arial", 10)).grid(row=2, column=0, padx=8, pady=5, sticky="w")

    entrada_condado_minerales = tk.Entry(bloque_minerales, bg=COLOR_ENTRADA, width=22,
                                         font=("Arial", 11))
    entrada_condado_minerales.grid(row=2, column=1, padx=8, pady=5)

    tk.Button(bloque_minerales, text="Mostrar Minerales",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 10, "bold"),
              width=20, height=2,
              command=lambda: mostrar_resultado("Minerales encontrados",
                                                minerales_en_condado(mapa,
                                                                     texto_normal(entrada_pais_minerales.get()),
                                                                     texto_normal(entrada_estado_minerales.get()),
                                                                     texto_normal(entrada_condado_minerales.get())))).grid(row=3, column=1, pady=8)

    panel.grid_columnconfigure(0, weight=1)
    panel.grid_columnconfigure(1, weight=1)


# ---------------------------------------------------------
# PANTALLA: MINERALES
# ---------------------------------------------------------
def ejecutar_agregar_mineral(pais, estado, condado, mineral):
    resultado = agregar_mineral_a_condado(mapa, pais, estado, condado, mineral)

    if resultado:
        messagebox.showinfo("Correcto", "Mineral agregado correctamente.")
    else:
        messagebox.showerror("Error", "No se pudo agregar. Revise los datos o si el mineral ya existe.")

    mostrar_resultado("Minerales actuales",
                      minerales_en_condado(mapa, pais, estado, condado))
    
def ejecutar_eliminar_mineral(pais, estado, condado, mineral):
    resultado = eliminar_mineral_de_condado(mapa, pais, estado, condado, mineral)

    if resultado:
        messagebox.showinfo("Correcto", "Mineral eliminado correctamente.")
    else:
        messagebox.showerror("Error", "No se pudo eliminar. Revise los datos.")

    mostrar_resultado("Minerales actuales",
                      minerales_en_condado(mapa, pais, estado, condado))
    
def pantalla_minerales():
    limpiar_area_trabajo()

    titulo = tk.Label(area_trabajo, text="Mantenimiento de minerales",
                      bg=COLOR_FONDO, fg=COLOR_BOTON,
                      font=("Arial", 22, "bold"))
    titulo.pack(anchor="w", padx=25, pady=(18, 5))

    panel = tk.Frame(area_trabajo, bg=COLOR_PANEL_CLARO)
    panel.pack(fill="x", padx=25, pady=8)

    bloque_agregar = tk.LabelFrame(panel, text="Agregar Mineral",
                                   bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
                                   font=("Arial", 15, "bold"))
    bloque_agregar.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

    tk.Label(bloque_agregar, text="País:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=0, column=0, sticky="w", padx=8, pady=6)
    entrada_pais_agregar = tk.Entry(bloque_agregar, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_pais_agregar.grid(row=0, column=1, padx=8, pady=6)

    tk.Label(bloque_agregar, text="Estado:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=1, column=0, sticky="w", padx=8, pady=6)
    entrada_estado_agregar = tk.Entry(bloque_agregar, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_estado_agregar.grid(row=1, column=1, padx=8, pady=6)

    tk.Label(bloque_agregar, text="Condado:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=2, column=0, sticky="w", padx=8, pady=6)
    entrada_condado_agregar = tk.Entry(bloque_agregar, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_condado_agregar.grid(row=2, column=1, padx=8, pady=6)

    tk.Label(bloque_agregar, text="Mineral:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=3, column=0, sticky="w", padx=8, pady=6)
    entrada_mineral_agregar = tk.Entry(bloque_agregar, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_mineral_agregar.grid(row=3, column=1, padx=8, pady=6)


    tk.Button(bloque_agregar, text="Agregar Mineral",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 10, "bold"),
              width=20, height=2,
              command=lambda:ejecutar_agregar_mineral(
              texto_normal(entrada_pais_agregar.get()),
              texto_normal(entrada_estado_agregar.get()),
              texto_normal(entrada_condado_agregar.get()),
              texto_normal(entrada_mineral_agregar.get())
          )).grid(row=4, column=1, pady=12)

    bloque_eliminar = tk.LabelFrame(panel, text="Eliminar Mineral",
                                    bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
                                    font=("Arial", 15, "bold"))
    bloque_eliminar.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

    tk.Label(bloque_eliminar, text="País:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=0, column=0, sticky="w", padx=8, pady=6)
    entrada_pais_eliminar = tk.Entry(bloque_eliminar, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_pais_eliminar.grid(row=0, column=1, padx=8, pady=6)

    tk.Label(bloque_eliminar, text="Estado:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=1, column=0, sticky="w", padx=8, pady=6)
    entrada_estado_eliminar = tk.Entry(bloque_eliminar, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_estado_eliminar.grid(row=1, column=1, padx=8, pady=6)

    tk.Label(bloque_eliminar, text="Condado:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=2, column=0, sticky="w", padx=8, pady=6)
    entrada_condado_eliminar = tk.Entry(bloque_eliminar, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_condado_eliminar.grid(row=2, column=1, padx=8, pady=6)

    tk.Label(bloque_eliminar, text="Mineral:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=3, column=0, sticky="w", padx=8, pady=6)
    entrada_mineral_eliminar = tk.Entry(bloque_eliminar, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_mineral_eliminar.grid(row=3, column=1, padx=8, pady=6)


    tk.Button(bloque_eliminar, text="Eliminar Mineral",
          bg=COLOR_ERROR, fg=COLOR_TEXTO,
          activebackground=COLOR_ERROR,
          font=("Arial", 10, "bold"),
          width=20, height=2,
          command=lambda: ejecutar_eliminar_mineral(
              texto_normal(entrada_pais_eliminar.get()),
              texto_normal(entrada_estado_eliminar.get()),
              texto_normal(entrada_condado_eliminar.get()),
              texto_normal(entrada_mineral_eliminar.get())
          )).grid(row=4, column=1, pady=12)

    panel.grid_columnconfigure(0, weight=1)
    panel.grid_columnconfigure(1, weight=1)


# ---------------------------------------------------------
# PANTALLA: CONDADOS
# ---------------------------------------------------------
def agregar_condado_interfaz(pais, estado, nombre_condado, lon1_texto, lat1_texto, lon2_texto, lat2_texto, minerales_texto):
    lon1 = leer_coordenada(lon1_texto)
    lat1 = leer_coordenada(lat1_texto)
    lon2 = leer_coordenada(lon2_texto)
    lat2 = leer_coordenada(lat2_texto)

    if lon1 == False or lat1 == False or lon2 == False or lat2 == False:
        messagebox.showerror("Error", "Revise las coordenadas. Use: grados,minutos,segundos")
        return

    coordenadas = [[lon1, lat1], [lon2, lat2]]
    minerales = leer_minerales(minerales_texto)

    resultado = agregar_condado(
        mapa,
        texto_normal(pais),
        texto_normal(estado),
        texto_normal(nombre_condado),
        coordenadas,
        minerales
    )

    if resultado:
        messagebox.showinfo("Correcto", "Condado agregado correctamente.")
    else:
        messagebox.showerror("Error", "No se pudo agregar. Revise país, estado o si ya existe.")

    mostrar_resultado(
        "Condados actuales",
        listar_condados(mapa, texto_normal(pais), texto_normal(estado))
    )


def eliminar_condado_interfaz(pais, estado, nombre_condado):
    resultado = eliminar_condado(
        mapa,
        texto_normal(pais),
        texto_normal(estado),
        texto_normal(nombre_condado)
    )

    if resultado:
        messagebox.showinfo("Correcto", "Condado eliminado correctamente.")
    else:
        messagebox.showerror("Error", "No se pudo eliminar. Revise los datos.")

    mostrar_resultado(
        "Condados actuales",
        listar_condados(mapa, texto_normal(pais), texto_normal(estado))
    )

def pantalla_condados():
    limpiar_area_trabajo()

    titulo = tk.Label(area_trabajo, text="Mantenimiento de condados",bg=COLOR_FONDO, fg=COLOR_BOTON,font=("Arial", 22, "bold"))
    titulo.pack(anchor="w", padx=25, pady=(18, 5))

    panel = tk.Frame(area_trabajo, bg=COLOR_PANEL_CLARO)
    panel.pack(fill="x", padx=25, pady=8)

    bloque_agregar = tk.LabelFrame(panel, text="Agregar Condado",bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,font=("Arial", 15, "bold"))
    bloque_agregar.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

    etiquetas = ["País:", "Estado:", "Condado:", "Longitud punto 1:", "Latitud punto 1:","Longitud punto 2:", "Latitud punto 2:", "Minerales:"]

    entradas = []

    for i in range(len(etiquetas)):
        tk.Label(bloque_agregar, text=etiquetas[i],bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,font=("Arial", 10)).grid(row=i, column=0, sticky="w", padx=8, pady=4)

        entrada = tk.Entry(bloque_agregar, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
        entrada.grid(row=i, column=1, padx=8, pady=4)
        entradas.append(entrada)

    entrada_pais_nuevo = entradas[0]
    entrada_estado_nuevo = entradas[1]
    entrada_condado_nuevo = entradas[2]
    entrada_lon1 = entradas[3]
    entrada_lat1 = entradas[4]
    entrada_lon2 = entradas[5]
    entrada_lat2 = entradas[6]
    entrada_minerales_nuevo = entradas[7]


    tk.Button(bloque_agregar, text="Agregar Condado",
          bg=COLOR_BOTON, fg=COLOR_OSCURO,
          activebackground=COLOR_BOTON_OSCURO,
          font=("Arial", 10, "bold"),
          width=15, height=2,
          command=lambda: agregar_condado_interfaz(
              entrada_pais_nuevo.get(),
              entrada_estado_nuevo.get(),
              entrada_condado_nuevo.get(),
              entrada_lon1.get(),
              entrada_lat1.get(),
              entrada_lon2.get(),
              entrada_lat2.get(),
              entrada_minerales_nuevo.get()
          )).grid(row=9, column=1, columnspan=2, pady=10)

    bloque_eliminar = tk.LabelFrame(panel, text="Eliminar condado",
                                    bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
                                    font=("Arial", 11, "bold"))
    bloque_eliminar.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

    tk.Label(bloque_eliminar, text="País:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=0, column=0, sticky="w", padx=8, pady=6)
    entrada_pais_borrar = tk.Entry(bloque_eliminar, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_pais_borrar.grid(row=0, column=1, padx=8, pady=6)

    tk.Label(bloque_eliminar, text="Estado:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=1, column=0, sticky="w", padx=8, pady=6)
    entrada_estado_borrar = tk.Entry(bloque_eliminar, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_estado_borrar.grid(row=1, column=1, padx=8, pady=6)

    tk.Label(bloque_eliminar, text="Condado:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=2, column=0, sticky="w", padx=8, pady=6)
    entrada_condado_borrar = tk.Entry(bloque_eliminar, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_condado_borrar.grid(row=2, column=1, padx=8, pady=6)



    tk.Button(bloque_eliminar, text="Eliminar Condado",
          bg=COLOR_ERROR, fg=COLOR_TEXTO,
          activebackground=COLOR_ERROR,
          font=("Arial", 10, "bold"),
          width=15, height=2,
          command=lambda: eliminar_condado_interfaz(
              entrada_pais_borrar.get(),
              entrada_estado_borrar.get(),
              entrada_condado_borrar.get()
          )).grid(row=4, column=1, columnspan=2, pady=10)

    panel.grid_columnconfigure(0, weight=2)
    panel.grid_columnconfigure(1, weight=1)


# ---------------------------------------------------------
# PANTALLA: COORDENADAS
# ---------------------------------------------------------
def convertir_decimal_interfaz(coordenada_texto):
    coord = leer_coordenada(coordenada_texto)

    if coord == False:
        messagebox.showerror("Error", "Use el formato grados,minutos,segundos.")
        return

    mostrar_resultado("Coordenada en decimal", coordenadas_a_decimal(coord))


def buscar_coordenada_interfaz(longitud_texto, latitud_texto):
    longitud = leer_coordenada(longitud_texto)
    latitud = leer_coordenada(latitud_texto)

    if longitud == False or latitud == False:
        messagebox.showerror("Error", "Use el formato grados,minutos,segundos.")
        return

    resultado = buscar_por_coordenadas_interfaz(longitud, latitud)
    mostrar_resultado("Condado encontrado", resultado)


def calcular_area_interfaz(pais, estado, condado):
    condado_encontrado = buscar_condado_completo(
        texto_normal(pais),
        texto_normal(estado),
        texto_normal(condado)
    )

    if condado_encontrado == False:
        messagebox.showerror("Error", "No se encontró el condado.")
        return

    mostrar_resultado("Área aproximada del condado", area_de_condado(condado_encontrado))


def revisar_traslape_interfaz(pais1, estado1, condado1, pais2, estado2, condado2):
    primer_condado = buscar_condado_completo(
        texto_normal(pais1),
        texto_normal(estado1),
        texto_normal(condado1)
    )

    segundo_condado = buscar_condado_completo(
        texto_normal(pais2),
        texto_normal(estado2),
        texto_normal(condado2)
    )

    if primer_condado == False or segundo_condado == False:
        messagebox.showerror("Error", "No se encontró uno de los condados.")
        return

    mostrar_resultado("Resultado de traslape", hay_traslape(primer_condado, segundo_condado))


def verificar_traslapes_interfaz():
    mostrar_resultado("Traslapes encontrados", verificar_traslapes())

def pantalla_coordenadas():
    limpiar_area_trabajo()

    titulo = tk.Label(area_trabajo, text="Coordenadas y traslapes",
                      bg=COLOR_FONDO, fg=COLOR_BOTON,
                      font=("Arial", 22, "bold"))
    titulo.pack(anchor="w", padx=25, pady=(18, 5))

    panel = tk.Frame(area_trabajo, bg=COLOR_PANEL_CLARO)
    panel.pack(fill="x", padx=25, pady=8)

    bloque_decimal = tk.LabelFrame(panel, text="Convertir a decimal",
                                   bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
                                   font=("Arial", 15, "bold"))
    bloque_decimal.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

    tk.Label(bloque_decimal, text="Coordenada:",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=0, column=0, padx=8, pady=6)

    entrada_coord_decimal = tk.Entry(bloque_decimal, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_coord_decimal.grid(row=0, column=1, padx=8, pady=6)

    tk.Label(bloque_decimal, text="Ejemplo: 10,30,0",
             bg=COLOR_PANEL_CLARO, fg=COLOR_BOTON,
             font=("Arial", 9)).grid(row=1, column=0, columnspan=2)


    tk.Button(bloque_decimal, text="Convertir a decimal",
          bg=COLOR_BOTON, fg=COLOR_OSCURO,
          activebackground=COLOR_BOTON_OSCURO,
          font=("Arial", 10, "bold"),
          width=20, height=2,
          command=lambda: convertir_decimal_interfaz(
              entrada_coord_decimal.get()
          )).grid(row=2, column=1, pady=10)

    bloque_buscar = tk.LabelFrame(panel, text="Buscar condado por coordenadas",
                                  bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
                                  font=("Arial", 15, "bold"))
    bloque_buscar.grid(row=0, column=1, padx=12, pady=12, sticky="nsew")

    tk.Label(bloque_buscar, text="Longitud:",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=0, column=0, padx=8, pady=6)

    entrada_longitud_buscar = tk.Entry(bloque_buscar, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_longitud_buscar.grid(row=0, column=1, padx=8, pady=6)

    tk.Label(bloque_buscar, text="Latitud:",
             bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=1, column=0, padx=8, pady=6)

    entrada_latitud_buscar = tk.Entry(bloque_buscar, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_latitud_buscar.grid(row=1, column=1, padx=8, pady=6)


    tk.Button(bloque_buscar, text="Buscar Condado",
          bg=COLOR_BOTON, fg=COLOR_OSCURO,
          activebackground=COLOR_BOTON_OSCURO,
          font=("Arial", 10, "bold"),
          width=20, height=2,
          command=lambda: buscar_coordenada_interfaz(
              entrada_longitud_buscar.get(),
              entrada_latitud_buscar.get()
          )).grid(row=2, column=1, columnspan=2, pady=10)

    bloque_area = tk.LabelFrame(panel, text="Área de condado",
                                bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
                                font=("Arial", 15, "bold"))
    bloque_area.grid(row=1, column=0, padx=12, pady=12, sticky="nsew")

    tk.Label(bloque_area, text="País:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=0, column=0, padx=8, pady=5, sticky="w")
    entrada_pais_area = tk.Entry(bloque_area, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_pais_area.grid(row=0, column=1, padx=8, pady=5)

    tk.Label(bloque_area, text="Estado:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=1, column=0, padx=8, pady=5, sticky="w")
    entrada_estado_area = tk.Entry(bloque_area, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_estado_area.grid(row=1, column=1, padx=8, pady=5)

    tk.Label(bloque_area, text="Condado:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=2, column=0, padx=8, pady=5, sticky="w")
    entrada_condado_area = tk.Entry(bloque_area, bg=COLOR_ENTRADA, width=22, font=("Arial", 11))
    entrada_condado_area.grid(row=2, column=1, padx=8, pady=5)

    tk.Button(bloque_area, text="Calcular Área",
          bg=COLOR_BOTON, fg=COLOR_OSCURO,
          activebackground=COLOR_BOTON_OSCURO,
          font=("Arial", 10, "bold"),
          width=20, height=2,
          command=lambda: calcular_area_interfaz(
              entrada_pais_area.get(),
              entrada_estado_area.get(),
              entrada_condado_area.get()
          )).grid(row=3, column=1, columnspan=2, pady=10)

    bloque_traslape = tk.LabelFrame(panel, text="Traslapes",
                                    bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
                                    font=("Arial", 15, "bold"))
    bloque_traslape.grid(row=1, column=1, padx=12, pady=12, sticky="nsew")

    tk.Label(bloque_traslape, text="Condado A",
             bg=COLOR_PANEL_CLARO, fg=COLOR_BOTON,
             font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=3)

    tk.Label(bloque_traslape, text="País:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=1, column=0, padx=5, pady=3)
    entrada_pais_t1 = tk.Entry(bloque_traslape, bg=COLOR_ENTRADA, width=16, font=("Arial", 10))
    entrada_pais_t1.grid(row=1, column=1, padx=5, pady=3)

    tk.Label(bloque_traslape, text="Estado:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=2, column=0, padx=5, pady=3)
    entrada_estado_t1 = tk.Entry(bloque_traslape, bg=COLOR_ENTRADA, width=16, font=("Arial", 10))
    entrada_estado_t1.grid(row=2, column=1, padx=5, pady=3)

    tk.Label(bloque_traslape, text="Condado:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=3, column=0, padx=5, pady=3)
    entrada_condado_t1 = tk.Entry(bloque_traslape, bg=COLOR_ENTRADA, width=16, font=("Arial", 10))
    entrada_condado_t1.grid(row=3, column=1, padx=5, pady=3)

    tk.Label(bloque_traslape, text="Condado B",
             bg=COLOR_PANEL_CLARO, fg=COLOR_BOTON,
             font=("Arial", 10, "bold")).grid(row=0, column=2, columnspan=2, pady=3)

    tk.Label(bloque_traslape, text="País:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=1, column=2, padx=5, pady=3)
    entrada_pais_t2 = tk.Entry(bloque_traslape, bg=COLOR_ENTRADA, width=16, font=("Arial", 10))
    entrada_pais_t2.grid(row=1, column=3, padx=5, pady=3)

    tk.Label(bloque_traslape, text="Estado:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=2, column=2, padx=5, pady=3)
    entrada_estado_t2 = tk.Entry(bloque_traslape, bg=COLOR_ENTRADA, width=16, font=("Arial", 10))
    entrada_estado_t2.grid(row=2, column=3, padx=5, pady=3)

    tk.Label(bloque_traslape, text="Condado:", bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO).grid(row=3, column=2, padx=5, pady=3)
    entrada_condado_t2 = tk.Entry(bloque_traslape, bg=COLOR_ENTRADA, width=16, font=("Arial", 10))
    entrada_condado_t2.grid(row=3, column=3, padx=5, pady=3)


    tk.Button(bloque_traslape, text="Revisar",
          bg=COLOR_BOTON, fg=COLOR_OSCURO,
          activebackground=COLOR_BOTON_OSCURO,
          font=("Arial", 10, "bold"),
          width=13, height=2,
          command=lambda: revisar_traslape_interfaz(
              entrada_pais_t1.get(),
              entrada_estado_t1.get(),
              entrada_condado_t1.get(),
              entrada_pais_t2.get(),
              entrada_estado_t2.get(),
              entrada_condado_t2.get()
          )).grid(row=4, column=1, pady=8)

    tk.Button(bloque_traslape, text="Ver todos los traslapes",
          bg=COLOR_BOTON, fg=COLOR_OSCURO,
          activebackground=COLOR_BOTON_OSCURO,
          font=("Arial", 10, "bold"),
          width=20, height=2,
          command=verificar_traslapes_interfaz).grid(row=4, column=3, columnspan=2, pady=8)

    panel.grid_columnconfigure(0, weight=1)
    panel.grid_columnconfigure(1, weight=1)


# ---------------------------------------------------------
# PANTALLA: ANÁLISIS
# ---------------------------------------------------------

def pantalla_analisis():
    limpiar_area_trabajo()

    titulo = tk.Label(area_trabajo, text="Análisis del mapa",
                      bg=COLOR_FONDO, fg=COLOR_BOTON,
                      font=("Arial", 22, "bold"))
    titulo.pack(anchor="w", padx=25, pady=(18, 5))


    panel = tk.Frame(area_trabajo, bg=COLOR_PANEL_CLARO)
    panel.pack(fill="x", padx=25, pady=8)

    bloque1 = tk.LabelFrame(panel, text="Condado con más minerales",
                            bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
                            font=("Arial", 15, "bold"))
    bloque1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

    tk.Button(bloque1, text="Consultar Condado",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 10, "bold"),
              width=20, height=2,
              command=lambda: mostrar_resultado("Condado con más minerales",
                                                condado_con_mas_minerales())).pack(pady=8)

    bloque2 = tk.LabelFrame(panel, text="Total minerales distintos",
                            bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
                            font=("Arial", 15, "bold"))
    bloque2.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")


    tk.Button(bloque2, text="Consultar Minerales",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 10, "bold"),
              width=20, height=2,
              command=lambda: mostrar_resultado("Total de minerales distintos",
                                                total_minerales_distintos())).pack(pady=8)

    bloque3 = tk.LabelFrame(panel, text="Minerales por país",
                            bg=COLOR_PANEL_CLARO, fg=COLOR_TEXTO,
                            font=("Arial", 15, "bold"))
    bloque3.grid(row=0, column=2, padx=15, pady=15, sticky="nsew")

    tk.Button(bloque3, text="Consultar Cantidades",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 10, "bold"),
              width=20, height=2,
              command=lambda: mostrar_resultado("Minerales distintos por país",
                                                minerales_por_pais())).pack(pady=8)

    panel.grid_columnconfigure(0, weight=1)
    panel.grid_columnconfigure(1, weight=1)
    panel.grid_columnconfigure(2, weight=1)


# ---------------------------------------------------------
# VENTANA PRINCIPAL
# ---------------------------------------------------------
def volver_menu_desde_mantenimiento():
    ventana_mantenimiento.destroy()
    iniciar_menu_principal()
    
def iniciar_interfaz_mantenimiento():
    global ventana_mantenimiento
    global area_trabajo
    global caja_resultado

    ventana_mantenimiento = tk.Tk()
    ventana_mantenimiento.title("Mineral Global Tracker - Mantenimiento")
    ventana_mantenimiento.geometry("1180x700")
    ventana_mantenimiento.config(bg=COLOR_FONDO)

    menu = tk.Frame(ventana_mantenimiento, bg=COLOR_PANEL, width=220)
    menu.pack(side=tk.LEFT, fill=tk.Y)

    zona_derecha = tk.Frame(ventana_mantenimiento, bg=COLOR_FONDO)
    zona_derecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    encabezado = tk.Label(menu, text="MINERAL\nTRACKER",
                          bg=COLOR_PANEL, fg=COLOR_BOTON,
                          font=("Arial", 21, "bold"),
                          justify="center")
    encabezado.pack(pady=(25, 5))

    tk.Button(menu, text="Navegación",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 11, "bold"),
              width=17, height=2,
              command=pantalla_navegacion).pack(pady=7)

    tk.Button(menu, text="Minerales",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 11, "bold"),
              width=17, height=2,
              command=pantalla_minerales).pack(pady=7)

    tk.Button(menu, text="Condados",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 11, "bold"),
              width=17, height=2,
              command=pantalla_condados).pack(pady=7)

    tk.Button(menu, text="Coordenadas",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 11, "bold"),
              width=17, height=2,
              command=pantalla_coordenadas).pack(pady=7)

    tk.Button(menu, text="Análisis",
              bg=COLOR_BOTON, fg=COLOR_OSCURO,
              activebackground=COLOR_BOTON_OSCURO,
              font=("Arial", 11, "bold"),
              width=17, height=2,
              command=pantalla_analisis).pack(pady=7)
    tk.Button(menu, text="Recargar mapa",
            bg=COLOR_BOTON, fg=COLOR_OSCURO,
            activebackground=COLOR_BOTON_OSCURO,
            font=("Arial", 11, "bold"),
            width=17, height=2,
            command=recargar_mapa_archivo).pack(pady=7)
    tk.Button(menu, text="Salir",
          bg=COLOR_ERROR, fg=COLOR_TEXTO,
          activebackground=COLOR_ERROR,
          font=("Arial", 11, "bold"),
          width=17, height=2,
          command=volver_menu_desde_mantenimiento).pack(pady=(30, 10))

    area_trabajo = tk.Frame(zona_derecha, bg=COLOR_FONDO)
    area_trabajo.pack(side=tk.TOP, fill=tk.X, anchor="n")

    panel_resultado = tk.Frame(zona_derecha, bg=COLOR_OSCURO)
    panel_resultado.pack(side=tk.TOP, fill=tk.X, padx=20, pady=(8, 18), anchor="n")

    etiqueta_resultado = tk.Label(panel_resultado, text="Resultado",
                                  bg=COLOR_OSCURO, fg=COLOR_BOTON,
                                  font=("Arial", 13, "bold"))
    etiqueta_resultado.pack(anchor="w", padx=12, pady=(8, 0))

    frame_texto = tk.Frame(panel_resultado, bg=COLOR_OSCURO)
    frame_texto.pack(fill=tk.X, padx=12, pady=10)

    scrollbar_resultado = tk.Scrollbar(frame_texto)
    scrollbar_resultado.pack(side=tk.RIGHT, fill=tk.Y)

    caja_resultado = tk.Text(frame_texto,
                             height=10,
                             bg=COLOR_ENTRADA,
                             fg="black",
                             font=("Consolas", 10),
                             relief="flat",
                             yscrollcommand=scrollbar_resultado.set,
                             wrap="none")
    caja_resultado.pack(side=tk.LEFT, fill=tk.X, expand=True)

    scrollbar_resultado.config(command=caja_resultado.yview)

    caja_resultado.config(state="disabled")

    pantalla_navegacion()

    ventana_mantenimiento.mainloop()

cargar_mapa()
cargar_players()
iniciar_menu_principal()