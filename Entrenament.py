'''Aquest script serveix per entrenar el reconeixedor de caras.'''

#Importem las llibrerias i scripts necessaris.
import numpy as np
import fsController
import cv2Controller
import imageController
import pickleController

#Aquesta funció és per entrenar el reconeixedor.
def Entrenament(imagesNames, fs):
    #Definim variables per definir les persones
    idActual = 0
    idsLabels = {}
    #Definim les imatges d'entrenament i els labels.
    x_train = []
    y_labels = []
    #Definim la cascada per trobar la cara.
    faceCascade = cv2Controller.cv2Cascade('HaarCascade-Files-master/haarcascade_frontalface_default.xml')
    #Definim el reconeixedor a entrenar.
    recognizer = cv2Controller.cv2FaceRecognitionCreate()

    #Recorrem el directori d'entrenament i entrenem el reconeixedor.
    for i in imagesNames:
        #Busquem la imatge.
        file = fsController.findFs(fs, {"filename" : i})
        #Llegim la imatge.
        bytedata = pickleController.readPickle(file)
        #Descodifiquem la imatge.
        ima_IO = imageController.decodeImage(bytedata)
        #Transformem la imatge.
        img_PIL = imageController.convertImage(imageController.openImage(ima_IO), "L")
        #Passem la imatge a numpy.
        imageArray = imageController.numpyImage(img_PIL, "uint8")
        #Recorrem el nom de la imatge per agafar el nom sense el número.
        for j in range(len(i)):
            if i[j].isdigit():
                label = i[:j - len(i)]
                break
        #Afegim un valor al diccionari.
        if not label in idsLabels:
            idsLabels[label] = idActual
            idActual += 1
        #Agafem el seu valor.
        id_ = idsLabels[label]
        #Detectem caras amb la cascada.
        faces = faceCascade.detectMultiScale(imageArray, 1.3, 5)
        #Recorrem las caras.
        for (x, y, w, h) in faces:
            #Agafem només la cara.
            roi = imageArray[y : y + h, x : x + w]
            #Canviem la mida de la cara.
            roi = cv2Controller.cv2ResizeImage(roi, (280, 280))
            #Afegim els valors al x_train i y_labels.
            x_train.append(roi)
            y_labels.append(id_)
                    
    #Creem un pickle on guardar el diccionari de les persones.     
    pickleController.dumpPickle("./Archivos/labels.pickle", idsLabels)
        
    #Creem un yml que serà el resultat de l'entrenament.
    recognizer.train(x_train, np.array(y_labels))
    recognizer.save("./Archivos/trainer.yml")