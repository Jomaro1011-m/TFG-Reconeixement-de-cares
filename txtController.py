'''Aquest script serveix per manipular arxius txt.'''

#Aquesta funció és per llegir arxius txt.
def readTxt(name):
    #Guardem les línies de text en una llista i la retorna.
    with open(name, "r") as archivo:
        usuarioActual = [i for i in archivo]
    return usuarioActual

#Aquesta funció és per obrir arxius txt.
def openTxt(name):
    #Retorna l'arxiu obert.
    return open(name, "w")

#Aquesta funció és per escriure arxius txt.
def writeTxt(name, file):
    #Fa servir el mètode write per escriure en l'arxiu.
    file.write(name)

#Aquesta funció és per tancar arxius txt.
def closeTxt(file):
    #Fa servir el mètode close per tancar l'arxiu.
    file.close()