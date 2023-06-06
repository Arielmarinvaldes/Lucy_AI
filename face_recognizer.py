import cv2
import os
import pyttsx3
import threading as tr
import winsound
import sys
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yagmail

engine = pyttsx3.init()
# Motor de voz
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)


def talk(text):
    engine.say(text)
    engine.runAndWait()

# def enviar_correo():
#     smtp_server = 'smtp.gmail.com'
#     smtp_port = 587
#     smtp_username = 'espana.dev.1@gmail.com'
#     smtp_password = 'Espana.0101'
#     destinatario = 'amvaldes010117@gmail.com'

#     msg = MIMEMultipart()
#     msg['From'] = smtp_username
#     msg['To'] = destinatario
#     msg['Subject'] = 'Rostro Desconocido Detectado'

#     mensaje = 'Se ha detectado un rostro desconocido en la cámara.'
#     msg.attach(MIMEText(mensaje, 'plain'))

#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()
#         server.login(smtp_username, smtp_password)
#         server.send_message(msg)

#     talk("Correo electrónico enviado exitosamente")

#-------------------------------------------------------------------------------------
# username = 'espana.dev.1@gmail.com'
# password = 'Espana.0101'

# yag = yagmail.SMTP(username, password)

# def enviar_correo(destinatario, asunto, cuerpo):
#     yag.send(destinatario, asunto, cuerpo)
#     print("Correo electrónico enviado exitosamente")


intrusos_path = 'C:\\Users\\amval\\OneDrive\\Escritorio\\Lucy_AI\\intrusos'
data_path = 'C:\\Users\\amval\\OneDrive\\Escritorio\\Lucy_AI\\Data_Face'
image_paths = os.listdir(data_path)


face_recognizer = cv2.face.LBPHFaceRecognizer_create()
# Leyendo el modelo
face_recognizer.read('C:\\Users\\amval\\OneDrive\\Escritorio\\Lucy_AI\\LBPHFaceModel.xml')
face_classif = cv2.CascadeClassifier('C:\\Users\\amval\\OneDrive\\Escritorio\\Lucy_AI\\haarcascade_frontalface_default.xml')


def face_rec(state):
    capture = cv2.VideoCapture(0)
    while True:
        comp, frame = capture.read()
        if not comp:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aux_frame = gray.copy()

        faces = face_classif.detectMultiScale(gray, 1.3, 5)

        recognized = False
        unknown_detected = False
        for (x, y, w, h) in faces:
            face = aux_frame[y:y + h, x:x + w]
            face = cv2.resize(face, (150, 150), interpolation=cv2.INTER_CUBIC)
            result = face_recognizer.predict(face)

            cv2.putText(frame, f'{result}', (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

            # LBPHFace
            if result[1] < 76:
                recognized = True
                cv2.putText(frame, f'{image_paths[result[0]]}', (x, y - 25), 2, 1.1,
                            (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                nombre_rostro = image_paths[result[0]]
                talk(f'Bienvenido {nombre_rostro}')
                return 'reconocido'  # Retorna 'reconocido' cuando se reconoce un rostro

            else:
                unknown_detected = True
                thread_alarma_song(0)
                cv2.putText(frame, 'Desconocido', (x, y - 20), 1, 0.8, (0, 0, 255), 1,
                            cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                talk('Rostro Desconocido')
                
                # Tomar la foto del rostro desconocido
                img_name = f'imagen_{np.random.randint(100000)}.jpg'  # Generar un nombre aleatorio para la imagen
                img_path = os.path.join(intrusos_path, img_name)
                cv2.imwrite(img_path, frame)
                print(f"Se ha guardado la imagen del rostro desconocido: {img_name}")
                # enviar_correo()  # Llamada a la función para enviar correo electrónico
                # enviar_correo('amvaldes010117@gmail.com', 'Rostro Desconocido Detectado', 'Se ha detectado un rostro desconocido en la cámara.')


        cv2.imshow('frame', frame)
        # if recognized:
        #     talk(f'Bienvenido {nombre_rostro}')
        #     break

        # elif unknown_detected:
        #     talk('Rostro desconocido')
        #     break
        key = cv2.waitKey(1)
        if key == 27 or recognized or unknown_detected:
            break

    capture.release()
    cv2.destroyAllWindows()
    # sys.exit()
    return 'no_reconocido'  # Retorna 'no_reconocido' cuando no se reconoce ningún rostro

def alarma_song(state):
    if state == 0:
        winsound.PlaySound("repeating-alarm-tone-metal-detector.wav", winsound.SND_FILENAME)


def thread_alarma_song(state):
    ta = tr.Thread(target=alarma_song, args=(state,))
    ta.start()
