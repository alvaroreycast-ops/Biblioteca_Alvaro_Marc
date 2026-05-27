import unittest
import biblioteca
from bd import  conexion
from clases.Libro import Libro


class TestLibros(unittest.TestCase):

    def test_add(self):
        libro = Libro("Naruto", "Oda", 123, "1")
        biblioteca.add_libro(libro)

        conn = conexion.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM libros WHERE titulo = 'Naruto'")
            self.assertEqual(cursor.fetchone()[0], 1)

            cursor.execute("DELETE FROM libros WHERE titulo = 'Naruto'")

            conn.commit()
        finally:
            conn.close()

    def test_remove_libro(self):
        libro = Libro("Dragon Ball GT", "Akira", 456, "1")
        biblioteca.add_libro(libro)

        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM libros WHERE titulo = ?", ("Dragon Ball GT",))
        libro_id = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        biblioteca.remove_libro(libro_id)

        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM libros WHERE id = ?", (libro_id,))
        resultado = cursor.fetchone()[0]

        cursor.execute("DELETE FROM libros WHERE titulo = 'Dragon Ball GT'")
        conn.close()

        self.assertEqual(resultado, 0)


    def test_get_libroById(self):
        libro = Libro("Jeronimo Stilton", "Sebita Sebas", 214, "1")
        biblioteca.add_libro(libro)

        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM libros WHERE titulo = 'Jeronimo Stilton'")
        libro_id = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        resultado = biblioteca.get_libroById(libro_id)
        conn = conexion.get_connection()
        cursor = conn.cursor()
        self.assertEqual(resultado.titulo, libro.titulo)


        cursor.execute("DELETE FROM libros WHERE id = ?",(libro_id,))

        conn.commit()
        conn.close()

    def test_get_libroByTitulo(self):
        libro = Libro("Jeronimo Stilton 2, la venganza", "Sebita Sebas", 122, "1")
        biblioteca.add_libro(libro)

        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT titulo FROM libros WHERE titulo = 'Jeronimo Stilton 2, la venganza'")
        libro_titulo = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        resultado = biblioteca.get_libroByTitulo(libro_titulo)
        conn = conexion.get_connection()
        cursor = conn.cursor()
        self.assertEqual(resultado.titulo, libro.titulo)


        cursor.execute("DELETE FROM libros WHERE titulo = ?",(libro_titulo,))

        conn.commit()
        conn.close()

    def test_get_libroByAutor(self):
        libro = Libro("La Biblia", "Sebita Sebas Jesus", 122, "1")
        biblioteca.add_libro(libro)

        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT autor FROM libros WHERE autor = 'Sebita Sebas Jesus'")
        libro_autor = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        resultado = biblioteca.get_libroByAutor(libro_autor)
        conn = conexion.get_connection()
        cursor = conn.cursor()
        self.assertEqual(resultado.autor, libro.autor)


        cursor.execute("DELETE FROM libros WHERE autor = ?",(libro_autor,))

        conn.commit()
        conn.close()

    def test_get_libroByDisponible(self):
        libro = Libro("Libro sin stock", "Sebita Sebas", 0, "1")
        biblioteca.add_libro(libro)

        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT disponible FROM libros WHERE disponible = '0'")
        libro_disponible = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        resultado = biblioteca.get_libroByDisponible(libro_disponible)
        conn = conexion.get_connection()
        cursor = conn.cursor()
        self.assertEqual(resultado.disponible, libro.disponible)


        cursor.execute("DELETE FROM libros WHERE disponible = ?",(libro_disponible,))

        conn.commit()
        conn.close()

    def test_get_libro_no_existe(self):
        conn = conexion.get_connection()

        resultado = biblioteca.get_libroById(-1)
        self.assertEqual(resultado, None)

        conn.close()

    def test_list_libros(self):
        conn = conexion.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM libros")
        libro_cantidad = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        lista_libros = biblioteca.list_libros()

        self.assertEqual(len(lista_libros), libro_cantidad)

if __name__ == "__main__":
    unittest.main()