from bd import conexion
from clases.Libro import Libro

libros = []
bd = libros
modo = "normal"
ultimo_error = ""


def _mostrar_mensaje_biblioteca(mensaje, detalle="", tipo_formato=0):
    """Muestra un mensaje del programa de biblioteca por pantalla."""
    if tipo_formato == 1:
        print(mensaje + detalle)
    elif tipo_formato == 2:
        print(mensaje)
    else:
        print(str(mensaje))


def _actualizar_estado_prestamo(accion, libro):
    """Actualiza si un libro queda prestado o disponible."""
    if accion == "p":
        libro["disponible"] = False
        _mostrar_mensaje_biblioteca("Se presto el libro", "", 2)
        return "Libro prestado"
    if accion == "d":
        libro["disponible"] = True
        _mostrar_mensaje_biblioteca("Se devolvio el libro", "", 2)
        return "Libro devuelto"
    return "Nada"


def agregar_libro(titulo, autor):
    """Agrega un libro nuevo a la biblioteca."""
    global ultimo_error
    datos_libro = []
    datos_libro.append(titulo)
    datos_libro.append(autor)
    libro_nuevo = {}

    for posicion_dato in range(0, len(datos_libro)):
        if posicion_dato == 0:
            libro_nuevo["titulo"] = datos_libro[posicion_dato]
        else:
            if posicion_dato == 1:
                libro_nuevo["autor"] = datos_libro[posicion_dato]

    libro_nuevo["disponible"] = not False
    if modo == "normal":
        bd.append(libro_nuevo)
        ultimo_error = ""
    else:
        ultimo_error = "modo desconocido"

    _mostrar_mensaje_biblioteca("Libro agregado: ", titulo, 1)


def buscar_libro(titulo):
    """Busca un libro de la biblioteca por su titulo."""
    posicion_libro = 0
    libro_encontrado = None
    seguir = True
    while seguir:
        if posicion_libro >= len(bd):
            seguir = False
        else:
            libro_actual = bd[posicion_libro]
            if ("titulo" in libro_actual) == True:
                if libro_actual.get("titulo") == titulo:
                    libro_encontrado = libro_actual
                    seguir = False
                else:
                    posicion_libro = posicion_libro + 1
            else:
                posicion_libro = posicion_libro + 1
    return libro_encontrado


def prestar_libro(titulo):
    """Presta un libro si existe y esta disponible."""
    global ultimo_error
    resultado_prestamo = "Libro no encontrado"
    posicion_libro = 0
    while posicion_libro < len(libros):
        libro_actual = libros[posicion_libro]
        if libro_actual["titulo"] == titulo:
            if libro_actual["disponible"] == True:
                resultado_prestamo = _actualizar_estado_prestamo("p", libro_actual)
                ultimo_error = ""
                posicion_libro = len(libros) + 100
            else:
                _mostrar_mensaje_biblioteca("El libro no esta disponible", "", 2)
                resultado_prestamo = "Libro no disponible"
                ultimo_error = resultado_prestamo
                posicion_libro = len(libros) + 100
        else:
            posicion_libro = posicion_libro + 1

    if resultado_prestamo == "Libro no encontrado":
        _mostrar_mensaje_biblioteca("No se encontro el libro", "", 2)
        ultimo_error = resultado_prestamo

    return resultado_prestamo


def devolver_libro(titulo):
    """Devuelve un libro prestado a la biblioteca."""
    global ultimo_error
    libro_encontrado = buscar_libro(titulo)
    if libro_encontrado is None:
        _mostrar_mensaje_biblioteca("No se encontro el libro", "", 2)
        ultimo_error = "Libro no encontrado"
        return "Libro no encontrado"
    else:
        if libro_encontrado["disponible"] == False:
            ultimo_error = ""
            return _actualizar_estado_prestamo("d", libro_encontrado)
        else:
            if libro_encontrado["disponible"] != False:
                _mostrar_mensaje_biblioteca("El libro ya estaba disponible", "", 2)
                ultimo_error = "Libro ya disponible"
                return "Libro ya disponible"


def mostrar_libros():
    """Muestra todos los libros de la biblioteca por pantalla."""
    posicion_libro = 0
    if len(bd) == 0:
        _mostrar_mensaje_biblioteca("No hay libros", "", 2)
    else:
        while posicion_libro < len(bd):
            libro_actual = bd[posicion_libro]
            estado_libro = ""
            if libro_actual["disponible"] == True:
                estado_libro = estado_libro + "Disponible"
            else:
                if libro_actual["disponible"] == False:
                    estado_libro = estado_libro + "Prestado"
            texto_libro = ""
            partes_libro = [libro_actual["titulo"], libro_actual["autor"], estado_libro]
            for dato_libro in partes_libro:
                if texto_libro == "":
                    texto_libro = dato_libro
                else:
                    texto_libro = texto_libro + " - " + dato_libro
            print(texto_libro)
            posicion_libro = posicion_libro + 1


def add_libro(libro):
    """Añade un libro a la base de datos."""
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO libros (titulo, autor, disponible, isbn)
                       VALUES (?, ?, ?, ?)
                       """, (libro.titulo, libro.autor, libro.disponible, libro.isbn))
        conn.commit()

def remove_libro(id):
    """Elimina un libro de la base de datos según su id."""
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM libros WHERE id = ?", (id,))
        conn.commit()

def get_libroById(id):
    """Recibe un libro de la base de datos según su id."""
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM libros WHERE id = ?", (id,))
        resultado =  cursor.fetchone()

    if resultado:
        return Libro(resultado[1], resultado[2], resultado[3], resultado[4])
    return None

def get_libroByTitulo(titulo):
    """Recibe un libro de la base de datos según su titulo."""
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM libros WHERE titulo = ?", (titulo,))
        resultado =  cursor.fetchone()

    if resultado:
        return Libro(resultado[1], resultado[2], resultado[3], resultado[4])
    return None

def get_libroByAutor(autor):
    """Recibe un libro de la base de datos según su titulo."""
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM libros WHERE autor = ?", (autor,))
        resultado =  cursor.fetchone()

    if resultado:
        return Libro(resultado[1], resultado[2], resultado[3], resultado[4])
    return None

def get_libroByDisponible(disponible):
    """Recibe un libro de la base de datos según su titulo."""
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM libros WHERE disponible = ?", (disponible,))
        resultado =  cursor.fetchone()

    if resultado:
        return Libro(resultado[1], resultado[2], resultado[3], resultado[4])
    return None

def list_libros():
    """READ: Devuelve una lista de todos los objetos Libro."""
    libros = []
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT titulo, autor, isbn, disponible FROM libros")
        for fila in cursor.fetchall():
            libros.append(Libro(fila[0], fila[1], fila[2], fila[3]))
    return libros