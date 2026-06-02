import unittest
import biblioteca
from bd import conexion


class TestLogs(unittest.TestCase):

    def tearDown(self):
        conn = conexion.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM logs WHERE mensaje = ?", (self.mensaje,))

        conn.commit()
        conn.close()

    def test_registrar_log_y_get_logs(self):
        self.mensaje = "TEST_LOG_UNICO_123"

        biblioteca._registrar_log(self.mensaje)
        logs = biblioteca.get_logs()

        self.assertTrue(any(log["mensaje"] == self.mensaje for log in logs))