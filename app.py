'''Aquest script serveix per executar l'app de manera local.'''

#Importem las llibrerias i scripts necessaris.
import re
import string
import zipfile
import osController
import fsController
import txtController
import mongoController
import imageController
import pickleController
from mail import sendmail
from shutil import rmtree
import responseController
from random import choice
from Entrenament import Entrenament
from werkzeug.utils import secure_filename
from PredictorImatges import PredictorImagenes
from flask import Flask, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash

#Definim l'app i configurem la base de dades de MongoDB amb las sevas col·leccions.
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/facerecognition'
mongo, db = mongoController.defineMongo(app)
fs = fsController.defineFs(mongo)

#Definim una clau per verificar l'usuari.
chars = string.digits
codigoVerificacion = ''.join(choice(chars) for _ in range(4))

#Definim un directori temporal per guardar i fer servir arxius temporals.
app.config['UPLOAD_FOLDER'] = "./Archivos"

#Creem el directori temporal.
osController.makeDirectory(app.config['UPLOAD_FOLDER'])

#Definim la ruta principal que et portarà a l'inici de sessió.
@app.route('/')
def home():
    #Retorna la plantilla d'iniciar sessió.
    return render_template('inicio.html')
 
#Definim la ruta del menú principal.  
@app.route('/Menu principal', methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        #Busquem l'usuari.
        user = mongoController.findMongo(db, {'name' : request.form['name'], 'email' : request.form['email']})
        #Comprovem que l'usuari existeix.
        try:
            #Comprovem que les dades siguin correctes.
            if len(user.keys()) != 0 and check_password_hash(user['password'], request.form['password']):
                #Definim l'usuari actual.
                file = txtController.openTxt(app.config['UPLOAD_FOLDER'] + "/usuarioActual.txt")
                txtController.writeTxt(osController.lineSep(request.form['name']), file)
                txtController.writeTxt(request.form['email'], file)
                txtController.closeTxt(file)
                #Si no està verificat va a la plantilla de verificar i se li envia un mail.
                if user['valid'] == False:
                    sendmail(request.form['email'], codigoVerificacion)
                    return render_template('validacion.html')
                #Sinó va a la plantilla del menú.
                return render_template('menu.html')
        #Sinó torna a la plantilla d'iniciar sessió.
        except AttributeError:
            return render_template('inicio.html')
    #Entra a la plantilla del menú.
    return render_template('menu.html')
    
#Definim la ruta per registrar sessió.
@app.route('/Registro')
def registro():
    #Entra a la plantilla del registre d'usuari.
    return render_template('registro.html')

#Definim la ruta on s'envia un mail de verificació.
@app.route('/Registro/Verificacion', methods = ['POST', 'GET'])
def verifyUser():
    if request.method == "POST":
        #Comprovem que el mail sigui correcte.
        EMAIL_REGEX = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
        if EMAIL_REGEX.match(request.form['email']):
            #Busquem l'usuari que ha posat.
            user = mongoController.findMongo(db, {'email' : request.form['email']})
            #Si ja està registrat torna a la plantilla de registre d'usuari.
            try:
                if len(user.keys()) != 0:
                    return render_template('registro.html')
            #Sinó envia un mail.
            except AttributeError:
                sendmail(request.form['email'], codigoVerificacion)
                #Insertem l'usuari en la col·lecció.
                mongoController.insertMongo(db, {'name' : request.form['name'],
                'email' : request.form['email'],
                'password' : generate_password_hash(request.form['password']),
                'role' : 'noAdmin',
                'images' : [],
                'imagesId' : [],
                'valid' : False
                })
                #Definim l'usuari actual.
                file = txtController.openTxt(app.config['UPLOAD_FOLDER'] + "/usuarioActual.txt")
                txtController.writeTxt(osController.lineSep(request.form['name']), file)
                txtController.writeTxt(request.form['email'], file)
                txtController.closeTxt(file)
                #Entra a la plantilla de verificació.
                return render_template('verificacion.html')
        #Si el mail no és correcte torna a la plantilla de registre d'usuari.
        return render_template('registro.html')
    #Entra a la plantilla de verificació.
    return render_template('verificacion.html')

#Definim la ruta per validar l'usuari.
@app.route('/Validación', methods = ['POST'])
@app.route('/Verificación', methods = ['POST'])
def validate():
    #Comprovem que el codi sigui correcte.
    user_otp = request.form['codigoVerificacion']
    if codigoVerificacion == user_otp:
        #Actualitzem l'usuari com a verificat.
        usuarioActual = txtController.readTxt(app.config['UPLOAD_FOLDER'] + "/usuarioActual.txt")
        mongoController.updateMongo(db, {'name' : usuarioActual[0][:-1], 'email' : usuarioActual[1]}, {"$set" : {'valid' : True}})
        #Entra a la plantilla de verificat.
        return render_template('verificado.html')
    #Si el codi no és correcte, entra a la plantilla de no verificat.
    return render_template('noVerificado.html')

#Definim la ruta per pujar imatges.
@app.route('/Uploader')
def uploader():
    #Entra a la plantilla d'uploader.
    return render_template('uploader.html')

#Definim la ruta per entrenament.
@app.route('/Entrenar')
def entrenament():
    #Definim l'usuari actual.
    usuarioActual = txtController.readTxt(app.config['UPLOAD_FOLDER'] + "/usuarioActual.txt")
    #Busquem l'usuari.
    user = mongoController.findMongo(db, {'name' : usuarioActual[0][:-1], 'email' : usuarioActual[1]})
    #Si no hi ha imatges pujades va a la plantilla de sense imatges.
    if len(user['imagesId']) == 0:
        return render_template('sinImagenes.html')
    #Si té, entrenem el model.
    Entrenament(user['imagesId'], fs)
    #Obrim l'arxiu pickle.
    pickle = pickleController.openPickle(app.config['UPLOAD_FOLDER'] + '/labels.pickle', 'rb')
    #Llegim l'arxiu pickle.
    dataPickle = pickleController.readPickle(pickle)
    #Afegim l'arxiu pickle al fs.
    fsController.putFs(fs, dataPickle, 'labels.pickle')
    #Fem el mateix procés amb l'arxiu yml.
    trainer = pickleController.openPickle(app.config['UPLOAD_FOLDER'] + '/trainer.yml', 'rb')
    dataTrainer = pickleController.readPickle(trainer)
    fsController.putFs(fs, dataTrainer, 'trainer.yml')
    #Entra a la plantilla d'entrenat.
    return render_template('entrenat.html')

#Definim la ruta per predeïr amb el model.
@app.route('/Predictor')
def predicio():
    #Busquem l'arxiu yml.
    file = fsController.findFs(fs, {"filename" : "trainer.yml"})
    #Comprovem que prèviament s'ha entrenat el model.
    if file == None:
        #Si no entra a la plantilla de sense entrenament.
        return render_template('sinTrainer.html')
    #Entra a la plantilla de predictor.
    return render_template('predictor.html')

#Definim la ruta per la galería d'imatges.
@app.route('/Galeria')
def galeria():
    #Definim l'usuari actual.
    usuarioActual = txtController.readTxt(app.config['UPLOAD_FOLDER'] + "/usuarioActual.txt")
    #Busquem l'usuari.
    user = mongoController.findMongo(db, {'name' : usuarioActual[0][:-1], 'email' : usuarioActual[1]})
    #Si no hi ha imatges pujades va a la plantilla de sense imatges.
    if len(user['imagesId']) == 0:
        return render_template('sinImagenes.html')
    #Recorrem el nom de les imatges.
    for i in user['imagesId']:
        #Busquem la imatge.
        file = fsController.findFs(fs, {"filename" : i})
        #Processem la imatge.
        image = pickleController.readPickle(file)
        ima_IO = imageController.decodeImage(image)
        img_PIL = imageController.openImage(ima_IO)
        #Guardem la imatge al directori temporal.
        imageController.saveImage(img_PIL, "./Archivos/" + str(i) + ".jpeg")
    #Llistem el contingut del directori temporal.
    images = osController.listDir("./Archivos")
    images = [i for i in images if ".jpeg" in i]
    #Entra a la plantilla de galería.
    return render_template('galeria.html', images = images)

#Aquesta funció és per visualitzar una imatge de la galería.
@app.route('/Galeria/Visualizar', methods = ['POST', 'GET'])
def visualizacion():
    #Llegim la imatge del directori temporal    .
    if request.method == "POST":
        image = pickleController.readPickle(pickleController.openPickle(app.config['UPLOAD_FOLDER'] + "/" + request.form['nombre'], "rb"))
        return responseController.makeResponse(image)
    #Entra a la plantilla de visualització amb la imatge.
    return render_template('visualizacion.html', images = request.form['nombre'])

#Definim la ruta per descomprimir zips i pujar las imatges de dins.
@app.route('/UploaderZip', methods = ['POST'])
def uploaderZip():
    if request.method == "POST":
        #Guardem el zip al directori temporal.
        f = request.files['Imagen']
        filename = secure_filename(f.filename)
        f.save(osController.join(app.config['UPLOAD_FOLDER'], filename))
        #Definim l'usuari actual.
        usuarioActual = txtController.readTxt(app.config['UPLOAD_FOLDER'] + "/usuarioActual.txt")
        #Busquem l'usuari actual.
        user = mongoController.findMongo(db, {'name' : usuarioActual[0][:-1], 'email' : usuarioActual[1]})
        #Guardem les llistes de les imatges.
        userImages = user['images']
        userImagesId = user['imagesId']
        #Definim l'arxiu zip.
        ruta = app.config['UPLOAD_FOLDER'] + "/" + filename
        archivo_zip = zipfile.ZipFile(ruta, "r")
        try:
            #Descomprimir l'arxiu zip.
            archivo_zip.extractall(pwd = None, path = app.config['UPLOAD_FOLDER'])
            #Definim una llista amb les carpetas dins del zip.
            directorios = osController.listDir(app.config['UPLOAD_FOLDER'] + "/" + archivo_zip.namelist()[0][:-1])
            #Recorrem las carpetas.
            for i in directorios:
                #Definim una llista amb el contingut de las carpetas.
                imagenes = osController.listDir(app.config['UPLOAD_FOLDER'] + "/" + archivo_zip.namelist()[0] + i)
                #Recorrem las imatges.
                for j in imagenes:
                    #Obrim la imatge i la guardem al fs.
                    with open(app.config['UPLOAD_FOLDER'] + "/" + archivo_zip.namelist()[0] + i + "/" + j, "rb") as image_file:
                        posicio = len(j) - j.index(".")
                        encoded_string = imageController.encodeImage(pickleController.readPickle(image_file))
                        fielid = fsController.putFs(fs, encoded_string, i + j[:-posicio])
                        #Guardem la id de la imatge i el seu nom.
                        userImages.append(fielid)
                        userImagesId.append(i + j[:-posicio])
        except:
            pass
        #Tanca l'arxiu zip.
        archivo_zip.close()
        #Actualitza l'usuari.
        mongoController.updateMongo(db, {'name' : usuarioActual[0][:-1], 'email' : usuarioActual[1]}, {"$set" : {'images' : userImages, 'imagesId' : userImagesId}})
        #Entra a la plantilla d'upload.
        return render_template('upload.html')

#Definim la ruta per predicció.
@app.route('/UploaderPredictor', methods = ['POST', 'GET'])
def uploaderPredictor():
    if request.method == "POST":
        #Guardem la imatge al directori temporal.
        f = request.files['Imagen']
        filename = 'Imagen.jpg'
        f.save(osController.join(app.config['UPLOAD_FOLDER'], filename))
        #Cridem al predictor.
        p = PredictorImagenes(fs)
        p.Main()
        #Llegim la imatge resultant.
        image = pickleController.readPickle(pickleController.openPickle(app.config['UPLOAD_FOLDER'] + "/p.jpg", "rb"))
        #Fem un response de la imatge.
        return responseController.makeResponse(image)
    #Entra a la plantilla de visualització amb la imatge resultant.
    return render_template('visualizacion.html', images = 'p.jpg')

#Aquí s'executa l'app.
if __name__ == '__main__':
    #Executem l'app.
    app.run(debug = True)
    #Borrem el directori temporal.
    rmtree(app.config['UPLOAD_FOLDER'])