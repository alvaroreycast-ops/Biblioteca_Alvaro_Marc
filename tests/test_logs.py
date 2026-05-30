import unittest
import biblioteca
from bd import conexion
from clases.Libro import Libro
from clases.Usuario import Usuario


class TestLogs(unittest.TestCase):

    def setUp(self):
        libro = Libro("Don Quijote", "Cervantes", True, "978-1")
        biblioteca.add_libro(libro)
        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM libros WHERE titulo = 'Don Quijote'")
        self.libro_id = cursor.fetchone()[0]
        conn.close()

        usuario = Usuario("Luis", "Pérez", "luis@test.local", True)
        self.usuario_id = biblioteca.add_usuario(usuario)

    def tearDown(self):
        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM logs WHERE libro_id = ?", (self.libro_id,))
        cursor.execute("DELETE FROM prestamos WHERE libro_id = ?", (self.libro_id,))
        cursor.execute("DELETE FROM libros WHERE id = ?", (self.libro_id,))
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (self.usuario_id,))
        conn.commit()
        conn.close()

    def test_prestar_libro_registra_log(self):
        biblioteca.prestar_libro(self.libro_id, self.usuario_id)
        logs = biblioteca.get_logs()
        mensajes = [log["mensaje"] for log in logs]
        self.assertTrue(any("prestado" in m.lower() for m in mensajes))

    def test_log_contiene_nombre_libro_y_usuario(self):
        biblioteca.prestar_libro(self.libro_id, self.usuario_id)
        logs = biblioteca.get_logs()
        ultimo = logs[-1]["mensaje"]
        self.assertIn("Don Quijote", ultimo)
        self.assertIn("Luis", ultimo)


if __name__ == "__main__":
    unittest.main()