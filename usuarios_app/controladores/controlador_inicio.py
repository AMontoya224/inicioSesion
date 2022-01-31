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
        print("estededeedeede: ", user[0]["first_name"])
        return render_template( "dashboard.html", user=user )

    else:
        return redirect( '/' )


@app.route( '/registrar', methods=["POST"] )
def registrarUser_P():
    if request.form["password"] != request.form["confirmarPassword"]:
        flash("Las contraseñas son distintas")
        return redirect( '/' )

    if not PASS_REGEX.match(request.form["password"]): 
        flash("La contraseña debe contener al menos un número y una letra")
        return redirect('/')
    
    if not NAME_REGEX.match(request.form["last_name"]): 
        flash("El apellido solo puede contener letras")
        return redirect('/')
    
    if not NAME_REGEX.match(request.form["first_name"]): 
        flash("El nombre solo puede contener letras")
        return redirect('/')

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
        flash("E-mail inválido")
        return redirect('/')

    idUser = Users.agregarUser( nuevoUser )
    if idUser == False:
        flash("Problemas con el database")
        return redirect('/')

    session["id"] = idUser
    session["email"] = request.form["email"]
    #emails = Emails.obtenerListaEmails()
    #for email in emails:
    #    if nuevoEmail["correo"] == email["correo"]:
    #        flash("El correo ya ha sido registrado")
    #       return redirect('/')

    return redirect(url_for('despliegaDashboard', idUser=idUser ))


@app.route( '/ingresar', methods=["POST"] )
def ingresarUser_P():
    data = { 
        "email" : request.form["emailUsuario"] 
        }
    user_in_db = Users.get_by_email(data)
    if not user_in_db:
        print("E-mail no registrado")
        flash("E-mail no registrado")
        return redirect("/")

    print("contraseña", user_in_db["password"])
    if not bcrypt.check_password_hash(user_in_db["password"], request.form['passwordUsuario']):
        flash("Contraseña inválida")
        print("Contraseña inválida")
        return redirect('/')

    print("fefefefe", user_in_db)
    session["id"] = user_in_db["id"]
    session["email"] = request.form["emailUsuario"]
    print("fefefefe", user_in_db["id"])
 
    return redirect(url_for('despliegaDashboard', idUser=user_in_db["id"] ))


@app.route( '/destroy', methods=["POST"] )
def borrarSession():
    session.clear()
    return redirect( '/' )


@app.errorhandler(404)
def paginaNoEncontrada(error):
    return "¡Lo siento! No hay respuesta. Inténtalo mas tarde"