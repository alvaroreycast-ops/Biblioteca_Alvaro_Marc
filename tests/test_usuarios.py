import unittest
import biblioteca
from bd import conexion
from clases.Usuario import Usuario


class TestUsuarios(unittest.TestCase):

    def test_add_usuario(self):
        usuario = Usuario("Alvaro", "Rey", "alvaro@test.local", True, telefono="600111222", dni="12345678A")
        biblioteca.add_usuario(usuario)

        conn = conexion.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = 'alvaro@test.local'")
            self.assertEqual(cursor.fetchone()[0], 1)

            cursor.execute("DELETE FROM usuarios WHERE email = 'alvaro@test.local'")

            conn.commit()
        finally:
            conn.close()

    def test_remove_usuario(self):
        usuario = Usuario("Marc", "Zahonero", "marc@test.local", True, telefono="600333444", dni="87654321B")
        usuario_id = biblioteca.add_usuario(usuario)

        biblioteca.remove_usuario(usuario_id)

        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE id = ?", (usuario_id,))
        resultado = cursor.fetchone()[0]
        conn.close()

        self.assertEqual(resultado, 0)

    def test_get_usuarioById(self):
        usuario = Usuario("Sebas", "Villa", "sebas@test.local", True, telefono="600555666", dni="11111111C")
        usuario_id = biblioteca.add_usuario(usuario)

        resultado = biblioteca.get_usuarioById(usuario_id)

        conn = conexion.get_connection()
        cursor = conn.cursor()
        self.assertEqual(resultado.nombre, usuario.nombre)
        self.assertEqual(resultado.email, usuario.email)
        self.assertEqual(resultado.telefono, usuario.telefono)
        self.assertEqual(resultado.dni, usuario.dni)

        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))

        conn.commit()
        conn.close()

    def test_get_usuarioByNombre(self):
        usuario = Usuario("Unai", "Nose", "unai@test.local", True, telefono="600777888", dni="22222222D")
        biblioteca.add_usuario(usuario)

        resultado = biblioteca.get_usuarioByNombre("Unai")

        conn = conexion.get_connection()
        cursor = conn.cursor()
        self.assertEqual(resultado[0].nombre, usuario.nombre)

        cursor.execute("DELETE FROM usuarios WHERE email = ?", (usuario.email,))

        conn.commit()
        conn.close()

    def test_get_usuarioByApellidos(self):
        usuario = Usuario("Fernando", "Alonso", "fernando@test.local", True, telefono="600999000", dni="33333333E")
        biblioteca.add_usuario(usuario)

        resultado = biblioteca.get_usuarioByApellidos("Alonso")

        conn = conexion.get_connection()
        cursor = conn.cursor()
        self.assertEqual(resultado[0].apellidos, usuario.apellidos)

        cursor.execute("DELETE FROM usuarios WHERE email = ?", (usuario.email,))

        conn.commit()
        conn.close()

    def test_get_usuarioByEmail(self):
        usuario = Usuario("Iris", "Roca", "iris@test.local", True, telefono="600123123", dni="44444444F")
        biblioteca.add_usuario(usuario)

        resultado = biblioteca.get_usuarioByEmail("iris@test.local")

        conn = conexion.get_connection()
        cursor = conn.cursor()
        self.assertEqual(resultado.email, usuario.email)

        cursor.execute("DELETE FROM usuarios WHERE email = ?", (usuario.email,))

        conn.commit()
        conn.close()

    def test_get_usuario_no_existe(self):
        conn = conexion.get_connection()

        resultado = biblioteca.get_usuarioById(-1)
        self.assertEqual(resultado, None)

        conn.close()

    def test_list_usuarios(self):
        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuario_cantidad = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        lista_usuarios = biblioteca.list_usuarios()

        self.assertEqual(len(lista_usuarios), usuario_cantidad)

    def test_habilita_y_deshabilita_usuario(self):
        usuario = Usuario("Noa", "Soler", "noa@test.local", True, telefono="600456456", dni="55555555G")
        usuario_id = biblioteca.add_usuario(usuario)

        biblioteca.deshabilita_usuario(usuario_id)
        self.assertFalse(biblioteca.get_usuarioById(usuario_id).habilitado)

        biblioteca.habilita_usuario(usuario_id)
        self.assertTrue(biblioteca.get_usuarioById(usuario_id).habilitado)

        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        conn.commit()
        conn.close()


if __name__ == "__main__":
    unittest.main()
