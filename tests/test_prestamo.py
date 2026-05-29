import unittest
import biblioteca
from bd import conexion
from clases.Libro import Libro
from clases.Usuario import Usuario

class TestPrestamos(unittest.TestCase):

    def setUp(self):
        """Prepara un libro y un usuario de prueba."""
        libro = Libro("El Quijote", "Cervantes", True, "978-0")
        biblioteca.add_libro(libro)

        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM libros WHERE titulo = 'El Quijote'")
        self.libro_id = cursor.fetchone()[0]
        conn.close()

        usuario = Usuario("Ana", "García", "ana@test.local", True)
        self.usuario_id = biblioteca.add_usuario(usuario)

    def tearDown(self):
        """Limpia los datos de prueba."""
        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prestamos WHERE libro_id = ?", (self.libro_id,))
        cursor.execute("DELETE FROM libros WHERE id = ?", (self.libro_id,))
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (self.usuario_id,))
        conn.commit()
        conn.close()

    def test_prestar_libro_disponible(self):
        resultado = biblioteca.prestar_libro(self.libro_id, self.usuario_id)
        self.assertEqual(resultado, "Libro prestado")

    def test_prestar_libro_no_disponible(self):
        biblioteca.prestar_libro(self.libro_id, self.usuario_id)
        resultado = biblioteca.prestar_libro(self.libro_id, self.usuario_id)
        self.assertEqual(resultado, "Libro no disponible")

    def test_prestar_libro_inexistente(self):
        resultado = biblioteca.prestar_libro(99999, self.usuario_id)
        self.assertEqual(resultado, "Libro no encontrado")

if __name__ == "__main__":
    unittest.main()