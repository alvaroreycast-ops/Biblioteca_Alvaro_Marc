class Libro:
    def __init__(self, id, titulo, autor, disponible, isbn):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = disponible


    def __str__(self):
        return f"Libro(id={self.id}, titulo={self.titulo}, autor={self.autor}, disponible={self.disponible}, isbn={self.isbn})"