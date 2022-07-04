'''Aquest script serveix per manipular imatges.'''

#Importem las llibrerias necessàries.
import base64
import numpy as np
from PIL import Image
from io import BytesIO

#Aquesta funció és per obrir imatges.
def openImage(image):
    #Retorna la imatge oberta.
    return Image.open(image)

#Aquesta funció és per codificar imatges.
def encodeImage(image):
    #Retorna la imatge codificada.
    return base64.b64encode(image)

#Aquesta funció és per descodificar imatges.
def decodeImage(image):
    #Retorna la imatge descodificada.
    return BytesIO(base64.b64decode(image))

#Aquesta funció és per transformar imatges.
def convertImage(image, how):
    #Retorna la imatge transformada.
    return image.convert(how)

#Aquesta funció és per guardar imatges.
def saveImage(image, where):
    #Guarda la imatge.
    image.save(where)

#Aquesta funció és per passar imatges com a numpy.
def numpyImage(image, how):
    #Retorna la imatge com numpy.
    return np.array(image, how)