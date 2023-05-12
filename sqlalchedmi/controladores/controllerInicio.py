from app import app,db
from modelos.categoria import *
from modelos.producto import *
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

with app.app_context():
    db.create_all()
    
@app.route("/")
def inicio():
    return render_template("inicio.html")
"Se ha creado las tablas en la base de datos"