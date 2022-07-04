REQUISITS

1. Instalar python3 https://www.python.org/downloads/
2. Executar la comanda "pip install -r requirements.txt"
3. Conectar-se a MongoDB https://qastack.mx/programming/20796714/how-do-i-start-mongo-db-from-windows

EXPLICACIÓ DEL REPOSITORI

1. HaarCascade-Files-master: És una carpeta que conté les diferents cascadas per trobar parts d'una cara en una imatge. Es crida des d'entrenament.py i els predictors.py
2. ImatgesProva: És la carpeta on posar las imatges per intentar predeïr la persona.
3. ImatgesReconegudas: És la carpeta on es guarden las imatges on s'ha reconegut una cara.
4. IamtgesTraining: És la carpeta on posar las imatges de les personas a entrenar. Es guarden en una carpeta amb el nom de la persona.
5. LBPCascade: És una carpeta que conté un altre tipus de cascada con las del Haar. Es crida des d'entrenament.py i els predictors.py
6. Static: És una carpeta per decorar la interfície gràfica amb diferents plantillas i fonts.
7. Templates: És una carpeta amb arxius HTML5 per definir la interfície gràfica.
8. App.py: Un script per executar l'app de manera local. Es pot provar per veure com és la interfície gràfica. Falta per fer la part del menú principal un cop inicia sessió un usuari.
9. Entrenament.py: Un script per entrenar el reconeixedor de caras. Es pot provar.
10. Predictor.py: Un script que es defineix una classe abstracte per les diferents maneras de predeïr. No s'ha d'executar.
11. PredictorImatges.py: Un script per recorre l'arxiu ImatgesProva i predeïr las caras de les diferents imatges. Es pot provar però després de executar el d'entrenament.
12. cv2Controller.py: Un script per fer servir els mètodes d'Opencv.
13. fsController.py: Un script per fer servir els mètodes de Gridfs.
14. imageController.py: Un script per fer servir els mètodes de Image.
15. mail.py: Un script per enviar mails.
16. mongoController.py: Un script per fer servir els mètodes de MongoDB.
17. osController.py: Un script per fer servir els mètodes d'Os.
18. pickleController.py: Un script per fer servir els mètodes de Pickle.
19. responseController.py: Un script per fer servir els mètodes de Response.
20. txtController.py: Un script per fer manipular arxius txt.
21. Labels.pickle: Un arxiu per guardar el diccionari amb els identificadors de les personas. 
22. Requirements.txt: Un txt per instalar els paquets de python que he fet servir.
23. Trainer.yml: Un yml on es guarda els paràmetres que s'han fet servir per entrenar el predictor (x_trains, y_labels).
