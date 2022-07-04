'''Aquest script serveix per manipular arxius pickle.'''

#Importem las llibrerias necessàries.
import pickle

#Aquesta funció és per obrir arxius pickle.
def openPickle(name, how):
    #Retorna l'arxiu obert.
    return open(name, how)

#Aquesta funció és per llegir arxius pickle.
def readPickle(name):
    #Retorna l'arxiu llegit.
    return name.read()

#Aquesta funció és per crear i guardar arxius pickle.
def dumpPickle(name, idsLabels):
    #Escribim l'arxiu nou i el guardem amb un diccionari de base.
    with open(name, 'wb') as f:
        pickle.dump(idsLabels, f)

#Aquesta funció és per carregar arxius pickle.
def loadPickle(download_location):
    #Llegim l'arxiu.
    with open(download_location, 'rb') as f:
        #El carreguem i definim els diccionaris.
        ogIdsLabels = pickle.load(f)
        idsLabels = {v : k for k, v in ogIdsLabels.items()}
        archivos = {v : 1 for v in ogIdsLabels.values()}
    #Retornem els diccionaris.
    return idsLabels, archivos