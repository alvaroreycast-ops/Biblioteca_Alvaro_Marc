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
        print(biblioteca.ultimo_error)

if __name__ == "__main__":
    unittest.main()
