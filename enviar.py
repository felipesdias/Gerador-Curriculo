# encoding: utf-8

import smtplib
import codecs
import os
import getpass
import sys, traceback
from time import gmtime, strftime
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def saveLog(local, error):
    file = open("logError.txt", "a") 
    file.write("".join(["[", local, " - ", strftime("%Y-%m-%d %H:%M:%S", gmtime()), "]"]))
    file.write("\n")
    file.write("".join(['mensagem: ', str(error)]))
    file.write("\n")
    file.write(traceback.format_exc())
    file.write("\n\n")
    file.close()

def enviarLog(fromaddr):
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls()
    s.login("email", "senha")

    # instance of MIMEMultipart 
    msg = MIMEMultipart() 

    # storing the senders email address 
    msg['From'] = "email" 

    # storing the receivers email address 
    msg['To'] = "felipe.s.dias@outlook.com"

    # storing the subject 
    msg['Subject'] = "Log error curriculo email"

    # string to store the body of the mail 
    body = "Log de error"

    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 

    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 


    # open the file to be sent 
    filename = "logError.txt"

    attachment = open(filename, "rb")

    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 

    # encode into base64 
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment", filename=os.path.basename(filename))

    # attach the instance 'p' to instance 'msg' 
    msg.attach(p) 

    # Converts the Multipart msg into a string 
    text = msg.as_string() 

    # sending the mail 
    s.sendmail(fromaddr, nome[1], text)

    s.quit()

# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 

error = False

# start TLS for security 
s.starttls()

#pyinstaller --onefile enviar.py
# Authentication 
while True:
    try:
        fromaddr = input("Digite o email: ")
        password = getpass.getpass("Digite a senha: ")
        s.login(fromaddr, password)
        break
    except Exception as e:
        saveLog('login', e)
        error = True
        print("\nDados incorretos, tente novamente")

try:
    with codecs.open("config/titulo.txt",'r',encoding='utf-8-sig') as f:
        titulo = f.read()
except Exception as e:
    saveLog('titulo', e)
    error = True
    print("Erro ao ler arquivo titulo.txt")

try:
    with codecs.open("config/mensagem.txt",'r',encoding='utf-8-sig') as f:
        mensagem = f.read()
except Exception as e:
    saveLog('mensagem', e)
    error = True
    print("Erro ao ler arquivo mensagem.txt")

try:
    with codecs.open("config/nomes.txt",'r', encoding='utf-8-sig') as f:
        nomes = [x.strip().split('\t') for x in f.read().split('\n') if len(x) > 2 and "\t" in x]
except Exception as e:
    saveLog('nomes', e)
    error = True
    print("Erro ao ler arquivo nomes.txt")


print("Será enviado", len(nomes), "emails\n")

falhas = 0

index = 0
for nome in nomes:
    index += 1
    try:
        # instance of MIMEMultipart 
        msg = MIMEMultipart() 

        # storing the senders email address 
        msg['From'] = fromaddr 

        # storing the receivers email address 
        msg['To'] = nome[1] 

        # storing the subject 
        msg['Subject'] = titulo

        # string to store the body of the mail 
        body = mensagem

        # attach the body with the msg instance 
        msg.attach(MIMEText(body, 'plain')) 

        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 

        # open the file to be sent 
        filename = nome[0] + ".pdf"

        attachment = open("pdf/" + filename, "rb")

        # To change the payload into encoded form 
        p.set_payload((attachment).read()) 

        # encode into base64 
        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment", filename=os.path.basename(filename))

        # attach the instance 'p' to instance 'msg' 
        msg.attach(p) 

        # Converts the Multipart msg into a string 
        text = msg.as_string() 

        # sending the mail 
        s.sendmail(fromaddr, nome[1], text)

        print("Email enviado para ", nome[0], " - Restam ", len(nomes) - index, " emails", sep="")
    except Exception as e:
        error = True
        print("Falhou: ", nome[0], " <", nome[1], ">", sep="")
        saveLog('eviar', e)

if error == True:
    enviarLog(fromaddr)

print("Processo finalizado")
input("Aperte uma tecla para fechar")


# terminating the session 
s.quit()
