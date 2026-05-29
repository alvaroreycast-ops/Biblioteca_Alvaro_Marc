from bd import conexion
from clases.Libro import Libro
from clases.Usuario import Usuario

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


def _crear_tabla_prestamos():
    """Crea la tabla de préstamos si no existe."""
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                libro_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                fecha_prestamo TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (libro_id) REFERENCES libros(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)
        conn.commit()

def prestar_libro(libro_id, usuario_id):
    """Presta un libro si existe y está disponible."""
    _crear_tabla_prestamos()
    libro = get_libroById(libro_id)

    if libro is None:
        return "Libro no encontrado"

    if not libro.disponible:
        return "Libro no disponible"

    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE libros SET disponible = 0 WHERE id = ?",
            (libro_id,)
        )
        cursor.execute(
            "INSERT INTO prestamos (libro_id, usuario_id) VALUES (?, ?)",
            (libro_id, usuario_id)
        )
        conn.commit()

    return "Libro prestado"


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
    """Anade un libro a la base de datos."""
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO libros (titulo, autor, disponible, isbn)
                       VALUES (?, ?, ?, ?)
                       """, (libro.titulo, libro.autor, libro.disponible, libro.isbn))
        conn.commit()


def remove_libro(id):
    """Elimina un libro de la base de datos segun su id."""
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM libros WHERE id = ?", (id,))
        conn.commit()


def get_libroById(id):
    """Recibe un libro de la base de datos segun su id."""
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM libros WHERE id = ?", (id,))
        resultado = cursor.fetchone()

    if resultado:
        return Libro(resultado[1], resultado[2], resultado[3], resultado[4])
    return None


def get_libroByTitulo(titulo):
    """Recibe un libro de la base de datos segun su titulo."""
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM libros WHERE titulo = ?", (titulo,))
        resultado = cursor.fetchone()

    if resultado:
        return Libro(resultado[1], resultado[2], resultado[3], resultado[4])
    return None


def get_libroByAutor(autor):
    """Recibe un libro de la base de datos segun su autor."""
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM libros WHERE autor = ?", (autor,))
        resultado = cursor.fetchone()

    if resultado:
        return Libro(resultado[1], resultado[2], resultado[3], resultado[4])
    return None


def get_libroByDisponible(disponible):
    """Recibe un libro de la base de datos segun su disponibilidad."""
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM libros WHERE disponible = ?", (disponible,))
        resultado = cursor.fetchone()

    if resultado:
        return Libro(resultado[1], resultado[2], resultado[3], resultado[4])
    return None


def list_libros():
    """READ: Devuelve una lista de todos los objetos Libro."""
    lista_libros = []
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT titulo, autor, isbn, disponible FROM libros")
        for fila in cursor.fetchall():
            lista_libros.append(Libro(fila[0], fila[1], fila[2], fila[3]))
    return lista_libros


def _crear_tabla_usuarios():
    """Crea la tabla de usuarios si todavia no existe."""
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS usuarios (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nombre TEXT,
                       apellidos TEXT,
                       email TEXT,
                       habilitado INTEGER,
                       telefono TEXT,
                       dni TEXT
                       )
                       """)
        columnas = cursor.execute("PRAGMA table_info(usuarios)").fetchall()
        nombres_columnas = [columna[1] for columna in columnas]
        if "telefono" not in nombres_columnas:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN telefono TEXT")
        if "dni" not in nombres_columnas:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN dni TEXT")
        conn.commit()


def _usuario_desde_fila(fila):
    """Convierte una fila de base de datos en un objeto Usuario."""
    if fila is None:
        return None
    return Usuario(fila[1], fila[2], fila[3], bool(fila[4]), fila[0], fila[5], fila[6])


def add_usuario(usuario):
    """Anade un usuario a la base de datos."""
    _crear_tabla_usuarios()
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO usuarios
                       (nombre, apellidos, email, habilitado, telefono, dni)
                       VALUES (?, ?, ?, ?, ?, ?)
                       """, (
                           usuario.nombre,
                           usuario.apellidos,
                           usuario.email,
                           int(usuario.habilitado),
                           usuario.telefono,
                           usuario.dni,
                       ))
        conn.commit()
        return cursor.lastrowid


def remove_usuario(id):
    """Elimina un usuario de la base de datos segun su id."""
    _crear_tabla_usuarios()
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
        conn.commit()


def get_usuarioById(id):
    """Recibe un usuario de la base de datos segun su id."""
    _crear_tabla_usuarios()
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        resultado = cursor.fetchone()
    return _usuario_desde_fila(resultado)


def get_usuario(id):
    """Recibe un usuario de la base de datos segun su id."""
    return get_usuarioById(id)


def update_usuario(id, usuario):
    """Actualiza los datos de un usuario existente."""
    _crear_tabla_usuarios()
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE usuarios
                       SET nombre = ?, apellidos = ?, email = ?, habilitado = ?,
                       telefono = ?, dni = ?
                       WHERE id = ?
                       """, (
                           usuario.nombre,
                           usuario.apellidos,
                           usuario.email,
                           int(usuario.habilitado),
                           usuario.telefono,
                           usuario.dni,
                           id,
                       ))
        conn.commit()


def list_usuarios():
    """Devuelve una lista de todos los usuarios."""
    _crear_tabla_usuarios()
    usuarios = []
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        for fila in cursor.fetchall():
            usuarios.append(_usuario_desde_fila(fila))
    return usuarios


def habilita_usuario(id):
    """Marca un usuario como habilitado."""
    _crear_tabla_usuarios()
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET habilitado = 1 WHERE id = ?", (id,))
        conn.commit()


def deshabilita_usuario(id):
    """Marca un usuario como deshabilitado."""
    _crear_tabla_usuarios()
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET habilitado = 0 WHERE id = ?", (id,))
        conn.commit()


def get_usuarioByNombre(nombre):
    """Recibe usuarios de la base de datos segun su nombre."""
    _crear_tabla_usuarios()
    usuarios = []
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre = ?", (nombre,))
        for fila in cursor.fetchall():
            usuarios.append(_usuario_desde_fila(fila))
    return usuarios


def get_usuarioByEmail(email):
    """Recibe un usuario de la base de datos segun su email."""
    _crear_tabla_usuarios()
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()
    return _usuario_desde_fila(resultado)


def get_usuarioByApellidos(apellidos):
    """Recibe usuarios de la base de datos segun sus apellidos."""
    _crear_tabla_usuarios()
    usuarios = []
    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE apellidos = ?", (apellidos,))
        for fila in cursor.fetchall():
            usuarios.append(_usuario_desde_fila(fila))
    return usuarios

def devolver_libro(libro_id,usuario_id):
    """Si el usuario tiene ese libro, se borra de la base de datos y aumenta disponible en uno."""

    with conexion.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM prestamos WHERE libro_id = ? AND usuario_id = ?", (libro_id,usuario_id))
        resultado = cursor.fetchone()

        if not resultado:
            print("No hay ningun prestamo de ese libro a ese usuario")
            return None

        prestamo_id = resultado[0]

        cursor.execute("DELETE FROM prestamos WHERE id = ?", (prestamo_id,))
        cursor.execute("UPDATE libros SET disponible = disponible + 1 WHERE id = ?", (libro_id,))

        conn.commit()
        return 1