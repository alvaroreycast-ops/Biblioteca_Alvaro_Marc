class Prestamo:
    def __init__(self, libro_id, usuario_id, fecha_prestamo=None, id=None):
        self.id = id
        self.libro_id = libro_id
        self.usuario_id = usuario_id
        self.fecha_prestamo = fecha_prestamo

    def __str__(self):
        return f"Prestamo(id={self.id}, libro_id={self.libro_id}, usuario_id={self.usuario_id}, fecha_prestamo={self.fecha_prestamo})"