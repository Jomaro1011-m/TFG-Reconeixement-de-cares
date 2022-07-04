'''Aquest script serveix per predecir una persona passant imatges.'''

#Importem las llibrerias i scripts necessaris.
import fsController
import txtController
import cv2Controller
import pickleController
from Predictor import Predictor

#Definim la classe per predecir una persona passant imatges.
class PredictorImagenes(Predictor):
    #Definim els atributs necessaris.
    def __init__(self, fs):
        #Definim la cascada.
        self.faceCascade = cv2Controller.cv2Cascade('HaarCascade-Files-master/haarcascade_frontalface_default.xml')
        #Definim el reconeixedor.
        self.recognizer = cv2Controller.cv2FaceRecognitionCreate()
        #Definim el fs.
        self.fs = fs
        #Busquem l'arxiu yml.
        data = fsController.findFs(self.fs, {'filename' : 'trainer.yml'})
        #Llegim l'arxiu yml.
        outputdata = pickleController.readPickle(data)
        #Definim el directori de l'arxiu.
        download_location = "./Archivos/trainer.yml"
        #Guardem l'arxiu.
        output = pickleController.openPickle(download_location, 'wb')
        #Escribim dins de l'arxiu.
        txtController.writeTxt(outputdata, output)
        #Tanquem l'arxiu.
        txtController.closeTxt(output)
        #Llegim l'arxiu amb el reconeixedor.
        self.recognizer.read(download_location)
        #Definim els labels.
        self.idsLabels = {"person_name" : 1}
        #Definim un diccionari buït.
        self.archivos = {}
        
    #Llegim l'arxiu pickle.
    def LeerPickle(self):
        #Busquem l'arxiu pickle.
        data = fsController.findFs(self.fs, {'filename' : 'labels.pickle'})
        #Llegim l'arxiu.
        outputdata = pickleController.readPickle(data)
        #Definim el directori de l'arxiu.
        download_location = "./Archivos/labels.pickle"
        #Guardem l'arxiu.
        output = pickleController.openPickle(download_location, 'wb')
        #Escribim dins de l'arxiu.
        txtController.writeTxt(outputdata, output)
        #Tanquem l'arxiu.
        txtController.closeTxt(output)
        #Retorna els dos diccionaris amb el contingut del pickle.
        self.idsLabels, self.archivos = pickleController.loadPickle(download_location)
            
    #Predecim amb las imatges.
    def Predict(self, dir = "./Archivos/Imagen.jpg"):
        #Llegim la imatge.
        imagen = cv2Controller.cv2ReadImage(dir)
        #La passem a color gris.
        gray = cv2Controller.cv2Color(imagen)
        #Detectem caras amb la cascada.
        faces = self.faceCascade.detectMultiScale(gray, 1.3, 5)
        #Recorrem las caras
        for (x, y, w, h) in faces:
            #Agafem només la cara.
            roiGray = gray[y : y + h, x : x + w]
            #Canviem la mida de la cara.
            roiGray = cv2Controller.cv2ResizeImage(roiGray, (280, 280))
            #Passem la cara al reconeixedor.
            id_, conf = self.recognizer.predict(roiGray)
            #Definim un string buït.
            name = ""
            #Definim el grossor.
            stroke = 2
            #Agafem només si la confiança és més gran o igual que el 50%.
            if conf >= 50:
                #Definim la font del text.
                font = cv2Controller.cv2Font()
                #Guardem el nom.
                name += self.idsLabels[id_]
                #Definim un color.
                color = (255, 255, 255)
                #Posem el text a la imatge.
                cv2Controller.cv2Text(imagen, name, (x, y), font, color, stroke)
            #Definim un altre color.
            color = (255, 0, 0)
            #Definim les coordenades
            endCordX = x + w
            endCordY = y + h
            #Dibuixem un rectangle a la imatge.
            cv2Controller.cv2Rectangle(imagen, (x, y), (endCordX, endCordY), color, stroke)
            #Sumem al diccionari.
            self.archivos[id_] += 1
            #Guardem la imatge resultant.
            cv2Controller.cv2Write("./Archivos/p.jpg", imagen)
      
    #Executem tots els mètodes.                  
    def Main(self):
        #Cridem per llegir el pickle.
        self.LeerPickle()
        #Fem la predicció.
        self.Predict()