
import math

mapa = [
['CostaRica', [
['Alajuela', [
['Grecia', [[[0, 0, 1], [10, 0, 0]], [[10, 0, 0], [0, 0, 1]]], ['Cuarzo', 'Granito', 'Basalto']],
['SM', [[[12, 52, 53], [-10, 2, 2]], [[19, 21, 34], [-7, 12, 26]]], ['Amatista', 'Pirita', 'Calcita']]
]],
['Cartago', [
['Central', [[[10, 40, 35], [-25, 32, 12]], [[12, 12, 13], [-32, 18, 6]]], ['Amatista', 'Calcita', 'Obsidiana', 'Mica', 'Granito']],
['Guarco', [[[26, 40, 35], [-18, 32, 12]], [[29, 12, 13], [-22, 18, 6]]], ['Topacio', 'Pirita', 'Esmeralda']]
]]
]],
['USA', [
['Florida', [
['Miami', [[[77, 0, 3], [50, 2, 0]], [[72, 1, 1], [89, 8, 44]]], ['Cuarzo', 'Calcita', 'Hematita']],
['Orlando', [[[-18, 4, 39], [86, 33, 32]], [[-22, 12, 3], [82, 16, 22]]], ['Calcita', 'Jade', 'Pirita', 'Granito']]
]],
['Washington', [
['DC', [[[-50, 0, 0], [50, 0, 0]], [[-60, 0, 0], [60, 0, 0]]], ['Esmeralda', 'Rubí', 'Zafiro']]
]]
]],
['Japan', [
['Kanto', [
['Tokyo', [[[35, 41, 22], [139, 41, 30]], [[35, 42, 0], [139, 42, 10]]], ['Obsidiana', 'Granito', 'Mica']],
['Yokohama', [[[35, 27, 50], [139, 38, 18]], [[35, 28, 30], [139, 39, 0]]], ['Granito', 'Topacio', 'Cuarzo', 'Calcita']]
]],
['Kansai', [
['Osaka', [[[34, 41, 38], [135, 30, 14]], [[34, 42, 20], [135, 31, 0]]], ['Topacio', 'Rubí', 'Esmeralda']],
['Kyoto', [[[35, 0, 0], [135, 45, 0]], [[35, 1, 0], [135, 46, 0]]], ['Hematita', 'Jade', 'Obsidiana']]
]]
]]
]


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
print(total_minerales_distintos())


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