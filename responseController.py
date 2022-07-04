'''Aquest script serveix per fer response a les imatges.'''

#Importem las llibrerias necessàries.
from flask import make_response

#Aquesta funció és per fer response d'una imatge.
def makeResponse(image):
    #Fem response de la imatge
    response = make_response(image)
    #Definim el tipus de response i retornem.
    response.headers['Content-Type'] = 'image/jpg'
    return response