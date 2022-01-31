import re
from flask import flash
from usuarios_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Users:
    def __init__( self, id, first_name, last_name, email, password, gender, created_at, update_at ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.gender = gender
        self.created_at = created_at
        self.update_at = update_at
    
    @staticmethod
    def validarEmail(nuevoEmail):
        is_valid = True
        if not EMAIL_REGEX.match(nuevoEmail["email"]): 
            flash("Dirección de correo inválida!")
            is_valid = False
        return is_valid

    @classmethod
    def agregarUser( cls, nuevoUser ):
        query2 = "ALTER TABLE users AUTO_INCREMENT = 1;"
        connectToMySQL( "inicio_sesion" ).query_db( query2 )
        query = "INSERT INTO users(first_name, last_name, email, password, gender, created_at, update_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(gender)s, %(created_at)s, %(update_at)s);"
        resultado = connectToMySQL( "inicio_sesion" ).query_db( query, nuevoUser )
        return resultado
    
    @classmethod
    def obtenerUser( cls, obtenerUser ):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        resultado = connectToMySQL( "inicio_sesion" ).query_db( query, obtenerUser )
        return resultado[0]
    
    @classmethod
    def conseguirEmail(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        resultado = connectToMySQL( "inicio_sesion" ).query_db( query, data )
        if len(resultado) < 1:
            return False
        return resultado[0]
