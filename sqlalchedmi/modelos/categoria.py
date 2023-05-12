from app import db

class Categoria(db.Model):
    __tablename__="categorias"
    idCategoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    catNombre = db.Column(db.String(50),unique=True, nullable=False)
    def __repr__(self):
        return f'{self.catNombre}'