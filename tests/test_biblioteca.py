import unittest
from contextlib import redirect_stdout
from io import StringIO

import biblioteca


class TestBiblioteca(unittest.TestCase):
    def setUp(self):
        biblioteca.libros.clear()
        biblioteca.ultimo_error = ""
        biblioteca.modo = "normal"

    def test_agregar_libro_guarda_titulo_autor_y_estado_disponible(self):
        biblioteca.agregar_libro("El Quijote", "Miguel de Cervantes")

        self.assertEqual(len(biblioteca.libros), 1)
        self.assertEqual(biblioteca.libros[0]["titulo"], "El Quijote")
        self.assertEqual(biblioteca.libros[0]["autor"], "Miguel de Cervantes")
        self.assertTrue(biblioteca.libros[0]["disponible"])

    def test_prestar_libro_cambia_estado_si_existe_y_esta_disponible(self):
        biblioteca.agregar_libro("Nada", "Carmen Laforet")

        resultado = biblioteca.prestar_libro("Nada")

        self.assertEqual(resultado, "Libro prestado")
        self.assertFalse(biblioteca.libros[0]["disponible"])

    def test_devolver_libro_cambia_estado_si_estaba_prestado(self):
        biblioteca.agregar_libro("La colmena", "Camilo Jose Cela")
        biblioteca.prestar_libro("La colmena")

        resultado = biblioteca.devolver_libro("La colmena")

        self.assertEqual(resultado, "Libro devuelto")
        self.assertTrue(biblioteca.libros[0]["disponible"])

    def test_agregar_libro_ultimo_error(self):
        biblioteca.modo = "inalcanzable"
        biblioteca.agregar_libro("Harry Potter","JK")
        self.assertEqual(biblioteca.ultimo_error, "modo desconocido")

    def test_agregar_libro_ultimo_error_vuelve_vacio(self):
        biblioteca.modo = "raro"
        biblioteca.agregar_libro("Harry Potter","JK")
        biblioteca.modo = "normal"
        biblioteca.agregar_libro("It","Stephen King")

        self.assertEqual(biblioteca.ultimo_error, "")

    def test_mostrar_mensaje_biblioteca_saca_texto(self):
        pantalla = StringIO()

        with redirect_stdout(pantalla):
            biblioteca._mostrar_mensaje_biblioteca(123)

        self.assertEqual(pantalla.getvalue(), "123\n")

    def test_actualizar_estado_prestamo_con_accion_rara_da_nada(self):
        libro = {"titulo": "A", "autor": "B", "disponible": True}

        resultado = biblioteca._actualizar_estado_prestamo("x", libro)

        self.assertEqual(resultado, "Nada")
        self.assertTrue(libro["disponible"])

    def test_buscar_libro_no_lo_encuentra(self):
        biblioteca.agregar_libro("Uno","Autor")

        resultado = biblioteca.buscar_libro("Dos")

        self.assertIsNone(resultado)

    def test_buscar_libro_con_diccionario_sin_titulo(self):
        biblioteca.libros.append({"autor": "Anonimo", "disponible": True})
        biblioteca.agregar_libro("Despues","Alguien")

        resultado = biblioteca.buscar_libro("Despues")

        self.assertEqual(resultado["titulo"], "Despues")

    def test_prestar_libro_no_disponible_ultimo_error(self):
        biblioteca.agregar_libro("No disponible","Yo")
        biblioteca.prestar_libro("No disponible")

        resultado = biblioteca.prestar_libro("No disponible")

        self.assertEqual(resultado, "Libro no disponible")
        self.assertEqual(biblioteca.ultimo_error, "Libro no disponible")

    def test_prestar_libro_no_encontrado_ultimo_error(self):
        biblioteca.agregar_libro("Otro","Autor")

        resultado = biblioteca.prestar_libro("Nada aqui")

        self.assertEqual(resultado, "Libro no encontrado")
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    def test_devolver_libro_no_encontrado_ultimo_error(self):
        resultado = biblioteca.devolver_libro("Fantasma")

        self.assertEqual(resultado, "Libro no encontrado")
        self.assertEqual(biblioteca.ultimo_error, "Libro no encontrado")

    def test_devolver_libro_ya_disponible_ultimo_error(self):
        biblioteca.agregar_libro("Libre","Autor")

        resultado = biblioteca.devolver_libro("Libre")

        self.assertEqual(resultado, "Libro ya disponible")
        self.assertEqual(biblioteca.ultimo_error, "Libro ya disponible")

    def test_mostrar_libros_vacio(self):
        pantalla = StringIO()

        with redirect_stdout(pantalla):
            biblioteca.mostrar_libros()

        self.assertEqual(pantalla.getvalue(), "No hay libros\n")

    def test_mostrar_libros_con_disponible_y_prestado(self):
        biblioteca.agregar_libro("Libro 1","Autor 1")
        biblioteca.agregar_libro("Libro 2","Autor 2")
        biblioteca.prestar_libro("Libro 2")
        pantalla = StringIO()

        with redirect_stdout(pantalla):
            biblioteca.mostrar_libros()

        self.assertIn("Libro 1 - Autor 1 - Disponible", pantalla.getvalue())
        self.assertIn("Libro 2 - Autor 2 - Prestado", pantalla.getvalue())

    def test_error_con_raising_exception(self):
        with self.assertRaises(Exception):
            raise Exception("error inventado")

if __name__ == "__main__":
    unittest.main()
