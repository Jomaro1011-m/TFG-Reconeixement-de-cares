'''Aquest script serveix per fer servir funcions de MongoDB.'''

#Importem las llibrerias necessàries.
from flask_pymongo import PyMongo

#Aquesta funció és per connectar l'app a la base de dades de MongoDB.
def defineMongo(app):
    #Definim l'enllaç de la base de dades.
    app.config['MONGO_URI'] = 'mongodb://localhost/facerecognition'
    mongo = PyMongo(app)
    #Definim la col·lecció.  
    db = mongo.db.users  
    #Retornem la base de dades i la col·lecció.
    return mongo, db

#Aquesta funció és per fer una consulta a la base de dades.
def findMongo(db, query):
    #Retorna el resultat de la consulta.
    return db.find_one(query)

#Aquesta funció és per actualitzar la base de dades.
def updateMongo(db, query, query2):
    #actualitza la base de dades.
    db.update_one(query, query2)

#Aquesta funció és per insertar un document a la col·lecció.
def insertMongo(db, query):
    #Inserta a la col·lecció.
    db.insert_one(query)