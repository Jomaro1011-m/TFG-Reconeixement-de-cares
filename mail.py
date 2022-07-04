'''Aquest script serveix per enviar mails.'''

#Importem las llibrerias necessàries.
import smtplib
from email.mime.text import MIMEText

#Aquesta funció és per enviar mails.
def sendmail(to, code):
    #Definim l'estructura del missatge.
    msg = MIMEText("El código de verificación es: " + str(code))
    msg['Subject'] = "Código de verificación"
    msg['From'] = "jorditon736372@gmail.com"
    msg['To'] = "jorditon736372@gmail.com"
    debuglevel = True
    #Definim el servidor del mail.
    mail = smtplib.SMTP("smtp.gmail.com", 587)
    mail.set_debuglevel(debuglevel)
    mail.starttls()
    #Carreguem el mail personal.
    mail.login("jorditon736372@gmail.com", "zgtmxkoawiekahgn")
    #Enviem el mail.
    mail.sendmail("jorditon736372@gmail.com", to, msg.as_string())
    #Tanquem el mail.
    mail.quit()