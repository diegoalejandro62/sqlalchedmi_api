from app import app,db
from modelos.categoria import *
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

@app.route("/vistaCategoria")
def vistaCategoria():
    return render_template("frmCategoria.html")

@app.route("/agregarCategoria",methods=["POST"])
def agregarCategoria():
    try:
        nombre=(request.form["txtNombre"]).upper()
        categoria=Categoria(catNombre=nombre)
        db.session.add(categoria)
        db.session.commit()
        mensaje= "Categoria agregada correctamente"
    except exc.SQLAlchemyError as ex:
        db.session.rollback()
        mensaje=str(ex)
    return render_template("frmCategoria.html",mensaje=mensaje)

@app.route("/obtenerCategoriaJson",methods=["GET"])
def obtenerCategoriaJson():
    listaCategoria=Categoria.query.all()
    listaJson=[]
    for categoria in listaCategoria:
        categoria={
            "idCategoria":categoria.idCategoria,
            "catNombre":categoria.catNombre
        }
        listaJson.append(categoria)
    return listaJson

@app.route("/agregarCategoriaJson",methods=["POST"])
def agregarCategoriaJson():
    try:
        datos=request.get_json()
        categoria=Categoria(catNombre=datos["nombreCategoria"])
        db.session.add(categoria)
        db.session.commit()
        mensaje="categoria Agregada"
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje="problemas al agregar la categoria"
    return {"mensaje":mensaje}