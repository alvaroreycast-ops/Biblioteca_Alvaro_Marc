class Usuario:
    def __init__(self, nombre, apellidos, email, habilitado=True, id=None, telefono="", dni=""):
        self.id = id
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.habilitado = bool(habilitado)
        self.telefono = telefono
        self.dni = dni

    def __str__(self):
        return (
            f"Usuario(id={self.id}, nombre={self.nombre}, "
            f"apellidos={self.apellidos}, email={self.email}, "
            f"habilitado={self.habilitado}, telefono={self.telefono}, "
            f"dni={self.dni})"
        )
