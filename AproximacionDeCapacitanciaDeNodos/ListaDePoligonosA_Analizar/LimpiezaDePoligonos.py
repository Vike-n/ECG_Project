import math
import os

# ============================================================
# ARCHIVOS
# ============================================================

archivo = r"C:\Users\Saile\Desktop\Github\ECG_Project\AproximacionDeCapacitanciaDeNodos\ListaDePoligonosA_Analizar\NodoTierra.txt"

archivo_salida = os.path.splitext(archivo)[0] + "_limpio.txt"


# ============================================================
# PARÁMETROS
# ============================================================

# Distancia^2 mínima para considerar dos puntos iguales
EPS_DIST2 = 1e-12

# Área mínima permitida
EPS_AREA = 1e-10


# Ángulo mínimo permitido
# FasterCap considera problemáticos los triángulos muy delgados.
MIN_ANGLE_DEG = 5

# ============================================================
# FUNCIONES GEOMÉTRICAS
# ============================================================

def distancia2(p1, p2):
    return (
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2 +
        (p1[2] - p2[2]) ** 2
    )


def area_triangulo(p1, p2, p3):

    ax = p2[0] - p1[0]
    ay = p2[1] - p1[1]
    az = p2[2] - p1[2]

    bx = p3[0] - p1[0]
    by = p3[1] - p1[1]
    bz = p3[2] - p1[2]

    cx = ay * bz - az * by
    cy = az * bx - ax * bz
    cz = ax * by - ay * bx

    return 0.5 * math.sqrt(
        cx * cx +
        cy * cy +
        cz * cz
    )

def angulo(p1, p2, p3):
    """
    Ángulo en p1 formado por p2-p1 y p3-p1.
    """

    ax = p2[0] - p1[0]
    ay = p2[1] - p1[1]
    az = p2[2] - p1[2]

    bx = p3[0] - p1[0]
    by = p3[1] - p1[1]
    bz = p3[2] - p1[2]

    na = math.sqrt(ax*ax + ay*ay + az*az)
    nb = math.sqrt(bx*bx + by*by + bz*bz)

    if na == 0 or nb == 0:
        return 0.0

    producto = ax*bx + ay*by + az*bz

    cosang = producto / (na * nb)

    # Evita errores numéricos
    cosang = max(-1.0, min(1.0, cosang))

    return math.degrees(math.acos(cosang))



def angulos_triangulo(p1, p2, p3):

    a1 = angulo(p1, p2, p3)
    a2 = angulo(p2, p1, p3)
    a3 = angulo(p3, p1, p2)

    return a1, a2, a3



def triangulo_valido(p1, p2, p3):

    # --------------------------------------------------------
    # Dos vértices coincidentes
    # --------------------------------------------------------

    if distancia2(p1, p2) < EPS_DIST2:
        return False

    if distancia2(p1, p3) < EPS_DIST2:
        return False

    if distancia2(p2, p3) < EPS_DIST2:
        return False

    # --------------------------------------------------------
    # Área prácticamente nula
    # --------------------------------------------------------

    A = area_triangulo(p1, p2, p3)

    if A < EPS_AREA:
        return False

    a1, a2, a3 = angulos_triangulo(p1, p2, p3)

    angulo_min = min(a1, a2, a3)

    if angulo_min < MIN_ANGLE_DEG:
        return False

    return True


# ============================================================
# PROCESAR ARCHIVO
# ============================================================

triangulos_totales = 0
triangulos_validos = 0
triangulos_eliminados = 0

primeros_degenerados = []

print()
print("Procesando:")
print(archivo)
print()


with open(archivo, "r", encoding="utf-8") as f:
    lineas = f.readlines()


with open(archivo_salida, "w", encoding="utf-8") as salida:

    for numero_linea, linea in enumerate(lineas, start=1):

        partes = linea.split()

        # ----------------------------------------------------
        # Solo procesamos triángulos FasterCap:
        #
        # T nombre x1 y1 z1 x2 y2 z2 x3 y3 z3 ...
        #
        # ----------------------------------------------------

        if len(partes) >= 11 and partes[0] == "T":

            triangulos_totales += 1

            try:

                p1 = (
                    float(partes[2]),
                    float(partes[3]),
                    float(partes[4])
                )

                p2 = (
                    float(partes[5]),
                    float(partes[6]),
                    float(partes[7])
                )

                p3 = (
                    float(partes[8]),
                    float(partes[9]),
                    float(partes[10])
                )

            except (ValueError, IndexError):

                # Si la línea no tiene el formato esperado,
                # NO la eliminamos automáticamente.
                salida.write(linea)
                continue


            # ------------------------------------------------
            # Verificar triángulo
            # ------------------------------------------------

            if triangulo_valido(p1, p2, p3):

                # Triángulo correcto
                triangulos_validos += 1
                salida.write(linea)

            else:

                # Triángulo degenerado
                triangulos_eliminados += 1

                if len(primeros_degenerados) < 20:

                    A = area_triangulo(p1, p2, p3)

                    primeros_degenerados.append(
                        (
                            numero_linea,
                            p1,
                            p2,
                            p3,
                            A
                        )
                    )

                # IMPORTANTE:
                # No escribimos esta línea.
                # Por lo tanto queda eliminada.


        else:

            # ------------------------------------------------
            # Todas las líneas que NO son triángulos
            # se copian exactamente igual.
            # ------------------------------------------------

            salida.write(linea)


# ============================================================
# RESULTADOS
# ============================================================

print("==========================================")
print("RESULTADO")
print("==========================================")

print("Triángulos totales:    ", triangulos_totales)
print("Triángulos válidos:    ", triangulos_validos)
print("Triángulos eliminados: ", triangulos_eliminados)

print()

print("Archivo original:")
print(archivo)

print()

print("Archivo limpio:")
print(archivo_salida)

print()

if primeros_degenerados:

    print("Primeros triángulos eliminados:")
    print()

    for dato in primeros_degenerados:

        linea_num, p1, p2, p3, A = dato

        print(
            f"Línea {linea_num}:"
        )

        print(
            f"  P1 = {p1}"
        )

        print(
            f"  P2 = {p2}"
        )

        print(
            f"  P3 = {p3}"
        )

        print(
            f"  Área = {A}"
        )

        print()

else:

    print("No se encontraron triángulos degenerados.")
