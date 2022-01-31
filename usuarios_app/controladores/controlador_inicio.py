from flask import render_template, request, redirect, session, flash, url_for
from usuarios_app import app
from usuarios_app.modelos.modelo_inicio import Users
from datetime import datetime
from flask_bcrypt import Bcrypt
import re

PASS_REGEX = re.compile(r'^[a-zA-Z]+[0-9]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

bcrypt = Bcrypt( app )

@app.route( '/', methods=['GET'] )
def paginaInicio():
    return render_template( "index.html")


@app.route( '/dashboard/<idUser>', methods=["GET"] )
def despliegaDashboard(idUser):
    if 'id' in session:
        nuevoUser = {
            "id" : idUser
        }
        user = Users.obtenerUser(nuevoUser)
        return render_template( "dashboard.html", user=user )

    else:
        return redirect( '/' )


@app.route( '/registrar', methods=["POST"] )
def registrarUser_P():
    if not NAME_REGEX.match(request.form["first_name"]): 
        flash("El nombre solo puede contener letras", "register")
        return redirect('/')

    if not NAME_REGEX.match(request.form["last_name"]): 
        flash("El apellido solo puede contener letras", "register")
        return redirect('/')

    data = { 
        "email" : request.form["email"] 
        }
    user_in_db = Users.conseguirEmail(data)
    if user_in_db:
        flash("El e-mail ya está registrado, pruebe otro", "register")
        return redirect("/")

    if not PASS_REGEX.match(request.form["password"]): 
        flash("La contraseña debe contener al menos un número y una letra", "register")
        return redirect('/')

    if request.form["password"] != request.form["confirmarPassword"]:
        flash("Las contraseñas son distintas", "register")
        return redirect( '/' )

    passwordEncriptado = bcrypt.generate_password_hash(request.form["password"])
    nuevoUser = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : passwordEncriptado,
        "gender" : request.form["gender"],
        "created_at" : datetime.today(),
        "update_at" : datetime.today()
    }
    if not Users.validarEmail( nuevoUser ):
        flash("E-mail inválido", "register")
        return redirect('/')

    idUser = Users.agregarUser( nuevoUser )
    if idUser == False:
        flash("Problemas con el database", "register")
        return redirect('/')

    session["id"] = idUser
    session["email"] = request.form["email"]
    return redirect(url_for('despliegaDashboard', idUser=idUser ))


@app.route( '/ingresar', methods=["POST"] )
def ingresarUser_P():
    data = { 
        "email" : request.form["emailUsuario"] 
        }
    user_in_db = Users.conseguirEmail(data)
    if not user_in_db:
        flash("E-mail no registrado", "login")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db["password"], request.form['passwordUsuario']):
        flash("Contraseña inválida", "login")
        return redirect('/')

    session["id"] = user_in_db["id"]
    session["email"] = request.form["emailUsuario"]
    return redirect(url_for('despliegaDashboard', idUser=user_in_db["id"] ))


@app.route( '/destroy', methods=["POST"] )
def borrarSession():
    session.clear()
    return redirect( '/' )


@app.errorhandler(404)
def paginaNoEncontrada(error):
    return "¡Lo siento! No hay respuesta. Inténtalo mas tarde"
