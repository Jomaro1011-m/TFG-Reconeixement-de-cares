'''Aquest script serveix per definir una classe abstracte per predecir las caras de
diferentes maneras.'''

#Importem las llibrerias necessàries.
import abc

#Definim la classe abstracte per predecir.
class Predictor(abc.ABC):
    #Un mètode per llegir l'arxiu pickle.
    @abc.abstractmethod
    def LeerPickle(self):
        pass
    
    #Un mètode per predecir (aquest és diferent depenent del paràmetre).
    @abc.abstractmethod
    def Predict(self):
        pass
    
    #Un mètode per definir tots els mètodes de la classe.
    @abc.abstractmethod
    def Main(self):
        pass