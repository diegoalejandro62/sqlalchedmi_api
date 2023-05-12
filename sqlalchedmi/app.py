from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
import sqlite3

app=Flask(__name__)

cadenaConexion = "mysql+pymysql://root@localhost/sql_api"
#cadenaConexion = "sqlite:///basedatos.db"
app.config["SQLALCHEMY_DATABASE_URI"]=cadenaConexion

db=SQLAlchemy(app)

app.config['UPLOAD_FOLDER']='./static/imagenes'

from controladores.controllerInicio import *
from controladores.controllerCategoria import *
from controladores.controllerProducto import *

if __name__=="__main__":
    app.run(port=3000,debug=True)