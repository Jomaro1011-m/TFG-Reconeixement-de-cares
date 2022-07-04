'''Aquest script serveix per manipular la col·lecció fs.'''

#Importem las llibrerias necessàries.
import gridfs

#Aquesta funció és per definir la col·lecció fs.
def defineFs(mongo):
    #Retorna la col·lecció fs definida.
    return gridfs.GridFS(mongo.db)

#Aquesta funció és per posar dades a la col·lecció fs.
def putFs(fs, data, filename):
    #Retorna el resultat d'afegir data.
    return fs.put(data, filename = filename)

#Aquesta funció és per consultar la col·lecció fs.
def findFs(fs, query):
    #Retorna el resultat de la consultar.
    return fs.find_one(query)