from app import db

class Producto(db.Model):
    __tablename__='productos'
    idProducto=db.Column(db.Integer, primary_key=True, autoincrement=True)
    proCodigo= db.Column(db.Integer, unique=True, nullable=False)
    proNombre= db.Column(db.String(50),nullable=False)
    proPrecio= db.Column(db.Integer, nullable=False)
    
    proCategoria=db.Column(db.Integer,db.ForeignKey('categorias.idCategoria'),nullable=False)
    categoria=db.relationship("Categoria",backref=db.backref('categorias',lazy=True))
    
    def __repr__(self):
        return f'''({self.proCodigo},{self.proNombre},{self.proPrecio},{self.categoria.catNombre})'''