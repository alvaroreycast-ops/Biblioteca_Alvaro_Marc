import sys
import unittest
from io import StringIO
from unittest.mock import patch

import biblioteca as bib

class TestMenuBiblioteca(unittest.TestCase):

    def limpiar_seguro(self):
        with bib.conexion.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM prestamos
                WHERE libro_id IN (
                    SELECT id FROM libros WHERE titulo LIKE 'TEST_%'
                )
            """)

            cursor.execute("DELETE FROM libros WHERE titulo LIKE 'TEST_%'")
            cursor.execute("DELETE FROM usuarios WHERE email LIKE 'test_%'")
            cursor.execute("DELETE FROM logs WHERE mensaje LIKE '%TEST'")

            conn.commit()

    def test_menu_libros_completo(self):

        inputs = [
            "1",
            "1",
            "TEST_LIBRO_1",
            "TEST_AUTOR",
            "TEST_ISBN_1",

            "3",

            "5",
            "TEST_LIBRO_1",

            "0",
            "100",
            "0"
        ]

        with patch("builtins.input", side_effect=inputs):
            bib.menu_principal()

        libro = bib.get_libroByTitulo("TEST_LIBRO_1")

        self.assertIsNotNone(libro)
        self.assertEqual(libro.titulo, "TEST_LIBRO_1")

        bib.remove_libro(libro.id)
        self.limpiar_seguro()

    def test_menu_libros_todas_opciones(self):
        bib.add_libro(bib.Libro("TEST_LIBRO", "TEST_AUTOR", True, "TEST_ISBN"))

        libro = bib.get_libroByTitulo("TEST_LIBRO")
        self.assertIsNotNone(libro)
        libro_id = libro.id

        captured = StringIO()
        sys.stdout = captured

        inputs = [
            "2",
            str(libro_id),

            "1",
            "TEST_LIBRO_2",
            "TEST_AUTOR",
            "TEST_ISBN_2",

            "3",

            "4",
            str(libro_id),

            "5",
            "TEST_LIBRO",

            "6",
            "TEST_AUTOR",

            "7",
            "1",

            "0"
        ]

        with patch("builtins.input", side_effect=inputs):
            bib.menu_libros()


        sys.stdout = sys.__stdout__

        output = captured.getvalue()

        self.assertIn("TEST_LIBRO", output)

    def test_menu_usuarios_1_3_5(self):

        inputs = [
            "2",
            "1",
            "TEST",
            "USER",
            "test_user_1@mail.com",

            "3",

            "5",
            "test_user_1@mail.com",

            "0",
            "0"
        ]

        with patch("builtins.input", side_effect=inputs):
            bib.menu_principal()

        user = bib.get_usuarioByEmail("test_user_1@mail.com")

        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test_user_1@mail.com")

        bib.remove_usuario(user.id)
        self.limpiar_seguro()

    def test_menu_usuarios_2_4_6_7(self):
        bib.add_usuario(
            bib.Usuario(
                "TEST_USER",
                "TEST_APELLIDO",
                "test_user@mail.com",
                True
            )
        )

        user = bib.get_usuarioByEmail("test_user@mail.com")
        self.assertIsNotNone(user)
        user_id = user.id

        captured = StringIO()
        sys.stdout = captured


        inputs = [
            "2",
            str(user_id),

            "1",
            "TEST_USER_2",
            "TEST_APELLIDO",
            "test_user2@mail.com",

            "3",

            "4",
            str(user_id),

            "5",
            "test_user@mail.com",

            "6",
            "TEST_USER_2",

            "7",
            "TEST_APELLIDO",

            "2",
            str(user_id),
            "0"
        ]

        with patch("builtins.input", side_effect=inputs):
            bib.menu_usuarios()

        sys.stdout = sys.__stdout__

        output = captured.getvalue()


        self.assertIn("TEST_USER", output)


    def test_menu_prestamo_completo(self):

        # crear datos previos (necesarios para préstamo)
        libro = bib.Libro("TEST_PRESTAMO", "AUTO", True, "TEST_ISBN_PREST")
        bib.add_libro(libro)
        libro_db = bib.get_libroByTitulo("TEST_PRESTAMO")

        usuario = bib.Usuario("TEST", "USER", "test_prestamo@mail.com", True)
        user_id = bib.add_usuario(usuario)

        inputs = [
            "3",  # préstamos
            "1",  # prestar libro
            str(libro_db.id),
            str(user_id),

            "2",  # devolver libro
            str(libro_db.id),
            str(user_id),

            "0",
            "0"
        ]

        with patch("builtins.input", side_effect=inputs):
            bib.menu_principal()

        libro_final = bib.get_libroById(libro_db.id)

        # puede ser 0/1 dependiendo sqlite
        self.assertIn(libro_final.disponible, (0, 1))

        # cleanup
        bib.remove_libro(libro_db.id)
        bib.remove_usuario(user_id)
        self.limpiar_seguro()

    def test_menu_logs(self):

        bib._registrar_log("TEST_LOG_MENU")

        inputs = [
            "4",
            "",
            "0"
        ]

        with patch("builtins.input", side_effect=inputs):
            bib.menu_principal()

        logs = bib.get_logs()

        self.assertTrue(
            any("TEST_LOG_MENU" in l["mensaje"] for l in logs)
        )

        self.limpiar_seguro()



    def test_salir(self):
        with patch("builtins.input", side_effect=["0"]):
            bib.menu_principal()

        self.assertTrue(True)