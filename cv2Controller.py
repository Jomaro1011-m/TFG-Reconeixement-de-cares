'''Aquest script serveix per manipular imatges i el reconeixedor.'''

#Importem las llibrerias necessàries.
import cv2

#Aquesta funció és per definir la cascada detectora de caras.
def cv2Cascade(name):
    #Retorna la cascada.
    return cv2.CascadeClassifier(name)

#Aquesta funció és per definir el reconeixedor.
def cv2FaceRecognitionCreate():
    #Retorna el reconeixedor.
    return cv2.face.FisherFaceRecognizer_create()

#Aquesta funció és per canviar la mida de les imatges.
def cv2ResizeImage(image, how):
    #Retorna la imatge amb la mida.
    return cv2.resize(image, how)

#Aquesta funció és per llegir imatges.
def cv2ReadImage(name):
    #Retorna la imatge llegida.
    return cv2.imread(name)

#Aquesta funció és per canviar el color de les imatges.
def cv2Color(name):
    #Retorna la imatge amb el nou color.
    return cv2.cvtColor(name, cv2.COLOR_BGR2GRAY)

#Aquesta funció és per definir una font de text.
def cv2Font():
    #Retorna la font.
    return cv2.FONT_HERSHEY_SIMPLEX

#Aquesta funció és per posar text a les imatges
def cv2Text(image, name, coordenades, font, color, stroke):
    #Retorna la imatge amb el text.
    cv2.putText(image, name, coordenades, font, 1, color, stroke, cv2.LINE_AA)

#Aquesta funció és per dibuixar rectangles a les imatges.
def cv2Rectangle(image, coordenades, coordenades2, color, stroke):
    #Retorna la imatge amb el rectangle dibuixat.
    cv2.rectangle(image, coordenades, coordenades2, color, stroke)

#Aquesta funció és per guardar imatges.
def cv2Write(name, image):
    #Guarda la imatge.
    cv2.imwrite(name, image)