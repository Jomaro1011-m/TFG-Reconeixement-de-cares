'''Aquest script serveix per manipular directoris i string.'''

#Importem las llibrerias necessàries.
import os

#Aquesta funció és per crear un directori.
def makeDirectory(name):
    #Creem el nou directori en cas de no existir.
    os.makedirs(name, exist_ok = True)

#Aquesta funció és per crear un salt de línia a un string.
def lineSep(name):
    #Retorna l'string amb el salt de línia.
    return name + os.linesep

#Aquesta funció és per crear una llista amb el contingut del directori.
def listDir(name):
    #Retorna la llista amb el contingut del directori.
    return os.listdir(name)

#Aquesta funció és per crear un string amb un directori i el nom d'un arxiu.
def join(directori, filename):
    #Retorna l'string amb el directori i l'arxiu.
    return os.path.join(directori, filename)