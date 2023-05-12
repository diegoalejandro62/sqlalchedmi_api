from werkzeug.utils import secure_filename
from app import app,db
from modelos.producto import *
from modelos.categoria import *
from flask import Flask,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import os

@app.route("/vistaProducto")
def vistaProducto():
    producto=None
    listaCategorias = Categoria.query.all()
    return render_template("frmProducto.html",producto=producto,listaCategorias=listaCategorias)

@app.route("/listarProductos",methods=["GET"])
def listarProductos():
    listaProductos=Producto.query.all()
    return render_template('listarProductos.html',listaProductos=listaProductos)


@app.route("/agregarProducto",methods=["POST"])
def agregarProducto():
    try:
        estado=False
        codigo=int(request.form["txtCodigo"])
        nombre=request.form["txtNombreP"]
        precio=(request.form["txtPrecio"])
        categoria=int(request.form["cbCategoria"])
        producto=Producto(proCodigo=codigo,proNombre=nombre,
                          proPrecio=precio,proCategoria=categoria)
        db.session.add(producto)
        db.session.commit()
        estado=True
        archivo=request.files["fileFoto"]
        if(archivo.filename!=""):
            nombre=secure_filename(archivo.filename)
            nombreArchivo=str(producto.idProducto)+".jpg"
            archivo.save(os.path.join(app.config["UPLOAD_FOLDER"],nombreArchivo))
        mensaje="producto agregado correctamente"
        return redirect("/listarProductos")
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje=str(error)
    listaCategorias = Categoria.query.all()
    return render_template("frmProducto",producto=producto,listaCategorias=listaCategorias,mensaje=mensaje,estado=estado)

@app.route("/consultarProducto/<int:idProducto>",methods=["GET"])
def consultarProducto(idProducto):
    try:
        producto=Producto.query.get(idProducto)
    except exc.SQLAlchemyError as error:
        mensaje= "problemas al obtener producto"
    listaCategorias = Categoria.query.all()
    return render_template("frmEditarproducto.html",producto=producto,listaCategorias=listaCategorias)

@app.route("/actualizarProducto",methods=["POST"])
def actualizarProducto():
    try:
        idProducto=int(request.form["idProducto"])
        producto=Producto.query.get(idProducto)
        producto.proCodigo=int(request.form["txtCodigo"])
        producto.proNombre=request.form["txtNombreP"]
        producto.proPrecio=(request.form["txtPrecio"])
        producto.proCategoria=int(request.form["cbCategoria"])
        db.session.commit()
        archivo=request.files["fileFoto"]
        if(archivo.filename!=""):
            nombre=secure_filename(archivo.filename)
            nombreArchivo=str(producto.idProducto)+".jpg"
            archivo.save(os.path.join(app.config["UPLOAD_FOLDER"],nombreArchivo))
        return redirect("/listarProductos")
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje= "Problemas al actualizar el producto"
    listaCategorias=Categoria.query.all()
    return render_template("frmEditarProducto.html",listaCategorias=listaCategorias,mensaje=mensaje,producto=producto)

@app.route("/eliminar/<int:idProducto>",methods=["GET"])
def eliminarProducto(idProducto):
    try:
        producto=Producto.query.get(idProducto)
        db.session.delete(producto)
        db.session.commit()
        nombreArchivo=str(idProducto)+"jpg"
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"]+"/",nombreArchivo))
        mensaje="producto eliminado"
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje= "Eliminado"
    listaProductos=Producto.query.all()
    return render_template('listarProductos.html',listaProductos=listaProductos,mensaje=mensaje)

@app.route("/listarProductosJson",methods=["GET"])
def listarProductosjson():
    try:
        listaProductos=Producto.query.all()
        listaJson=[]
        for producto in listaProductos:
            producto={
                "idProducto":producto.idProducto,
                "proNombre":producto.proNombre,
                "proPrecio":producto.proPrecio,
                "categoria":{
                    "idCategoria":producto.categoria.idCategoria,
                    "catNombre":producto.categoria.catNombre
                }
            }
            listaJson.append(producto)
        mensaje="Lista de productos"
    except exc.SQLAlchemyError as error:
        mensaje= "Problemas al obtener los productos"
    return {"mensaje":mensaje,"listaProductos":listaJson}

@app.route("/consultarProductoJson",methods=["GET"])
def consultarProductosJson():
    try:
        datos=request.get_json(force=True)
        idProducto=int(datos["idProducto"])
        producto=Producto.query.get(idProducto)
        productoJson={
            "idProducto":producto.idProducto,
            "proNombre":producto.proNombre,
            "proPrecio":producto.proPrecio,
            "categoria":{
                "idCategoria":producto.categoria.idCategoria,
                "catNombre":producto.categoria.catNombre
            }
        }
        mensaje="Datos del Producto"
    except exc.SQLAlchemyError as error:
        mensaje="Problemas al consultar"
    return {"mensaje":mensaje,"producto":productoJson}

@app.route("/agregarProductoJson",methods=["POST"])
def agregarProductoJson():
    estado=False
    try:
        datos=request.get_json(force=True)
        codigo=int(datos["codigo"])
        nombre=datos["nombre"]
        precio=(datos["precio"])
        categoria=int(datos["categoria"])
        producto=Producto(proCodigo=codigo,proNombre=nombre,
                          proPrecio=precio,proCategoria=categoria)
        db.session.add(producto)
        db.session.commit()
        mensaje="Producto Agregado correctamente"
        estado=True
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje="Problemas al registrar"
    return {"mensaje":mensaje,"estado":estado}

@app.route("/eliminarProductoJson",methods=["POST"])
def eliminarProductoJson():
    try:
        estado=False
        datos=request.get_json(force=True)
        idProducto=int(datos["idProducto"])
        producto=Producto.query.get(idProducto)
        db.session.delete(producto)
        db.session.commit()
        estado=True
        mensaje="Producto Eliminado"
        nombreArchivo=str(idProducto)+"jpg"
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"]+"/"+nombreArchivo))
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje="Problemas al eliminar el producto"
    return {"mensaje":mensaje,"estado":estado}

@app.route("/actualizarProductoJson",methods=["POST"])
def actualizarProductoJson():
    try:
        estado=False
        datos=request.get_json(force=True)
        idProducto=int(datos["idProducto"])
        producto=Producto.query.get(idProducto)
        producto.proCodigo=int(datos["codigo"])
        producto.proNombre=datos["nombre"]
        producto.proPrecio=(datos["precio"])
        producto.proCategoria=int(datos["categoria"])
        db.session.commit()
        estado=True
        mensaje="producto eliminado"
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje= "Problemas al actualizar el producto"
    return {"mensaje":mensaje,"estado":estado}