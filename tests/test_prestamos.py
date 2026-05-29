import unittest
import biblioteca
from bd import  conexion
from clases.Libro import Libro
from clases.Usuario import Usuario

class TestPrestamos(unittest.TestCase):

    def test_devolver_libro(self):
        libro = Libro("Libro a devolver", "Sebita Sebas", 123, "11221")
        biblioteca.add_libro(libro)
        usuario = Usuario("Persona que devuelve", "Rey", "alvaro@tesDevolverLibro.local", True, telefono="600111222", dni="12345678A")
        biblioteca.add_usuario(usuario)

        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM libros WHERE titulo = 'Libro a devolver'")
        libro_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM usuarios WHERE nombre = 'Persona que devuelve'")
        usuario_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO prestamos (libro_id, usuario_id) VALUES (?, ?)", (libro_id, usuario_id))
        conn.commit()
        conn.close()

        resultado = biblioteca.devolver_libro(libro_id,usuario_id)

        self.assertEqual(resultado, 1)

        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM libros WHERE id = ?", (libro_id,))
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        conn.commit()
        conn.close()

    def test_devolver_libro_Prestamo_None(self):

        resultado = biblioteca.devolver_libro(-1, 1)

        self.assertEqual(resultado, None)