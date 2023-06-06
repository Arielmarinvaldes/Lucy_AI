import ast
import browser
import datetime
import database as db
import face_recognizer as fr
import geocoder
import keyboard
import lucy_cam
import operaciones_mate as mat
import operator
import os
import pyttsx3
import pywhatkit
import requests
import speech_recognition as sr
import subprocess as sub
import sys
import threading as tr
import time
import urllib
import whatsapp as whapp
import wikipedia
import collections.abc as collections
from chatterbot import ChatBot
from chatterbot import preprocessors
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from collections.abc import MutableMapping
from googletrans import Translator
from num2words import num2words
from tkinter import *
from PIL import Image, ImageTk
from pygame import mixer

def init():
    t = tr.Thread(target=fr.face_rec, args=(0,))
    t.start()
init()

# Establece el nombre del asistente en la ventada
main_window = Tk()
main_window.title("GUI")
main_window.geometry("700x700")
main_window.resizable(0, 0)
main_window.configure(bg='#FF9EA0')

# establece el nombre visible del asistente en el GUI
Label_title = Label(main_window, text="Lucy", bg="#FF9EA0",
                    fg="#2c3e50", font=('Arial', 12, 'bold'))
Label_title.pack(pady=10)

# comandos q puede ejecutar Lucy
cm = """ 
Comandos que puedes usar:
---------------------------------------------
-Reproduce: lo que quieras
-Busca: en wikipedia
-Alarma: establece alarmas
-Camara: detector de color
-Abre : aplicaciones
-Búscame un archivo: 
-Escribe: lo q le digas
-Envia un mensaje:
-Buscame: lo que quieras
-Conversar: hablar
-Reconocimiento: A o D
-Termina: fin de la app
-Clinma: saber el clima
-Qué: hora es o dia es hoy
-Gps: a donde quieres ir
"""
# canvas
canvas_comandos = Canvas(bg="#2193b0", height=230, width=144)
canvas_comandos.place(x=1, y=60)
canvas_comandos.create_text(75, 115, text=cm, fill="black", font='Arial 5')

Text_info = Text(main_window, bg="#C3C8D3", fg="#434343")
Text_info.place(x=1, y=294, height=169, width=149)

# fotos de luci en el GUI
lucy_photo = ImageTk.PhotoImage(Image.open("lucy_foto.jpg"))
window_photo = Label(main_window, image=lucy_photo)
window_photo.pack(pady=5)


# tipo de voz del asistente
def spanish_voice():
    change_voice(0)


def english_voice():
    change_voice(1)


def change_voice(id):
    engine.setProperty('voice', voices[id].id)
    engine.setProperty('rate', 145)
    talk("Hola soy Lucy")


# nombre de el asistente
name = "lucy"
engine = pyttsx3.init()

# Motor de voz de Lucy
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)


# funcion para recorrer los archivos de los diccionarios
def change_data(name_dict, name_file):
    try:
        with open(name_file) as f:
            for line in f:
                (key, val) = line.split(",")
                val = val.rstrip("\n")
                name_dict[key] = val

    except FileNotFoundError as e:
        print(e)
        
if not hasattr(time, 'clock'):
    time.clock = time.perf_counter

# diccionarios
sites = dict()
change_data(sites, "web.txt")

files = dict()
change_data(files, "file.txt")

contact = dict()
change_data(contact, "contact.txt")

apps = dict()
change_data(apps, "app.txt")


def talk(text):
    engine.say(text)
    engine.runAndWait()


def read_and_talk():
    text = Text_info.get("1.0", "end")
    talk(text)


def write_text(text_wiki):
    Text_info.insert(INSERT, text_wiki)


# funcion de escuchar
def listen():
    listener = sr.Recognizer()

    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        talk("Te escucho")
        pc = listener.listen(source)
    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
    except sr.UnknownValueError:
        print("No te entendi. intenta de nuevo")
    except sr.RequestError as e:
        print(
            "Cloud not request result from Google Speech Recofnition serevice; {0}".format(e))
    return rec


# Funciones asociadas a las palabras claves
def reproduce(rec):
    music = rec.replace('reproduce', '')
    print("Reproduciendo " + music)
    talk("Reproduciendo " + music)
    pywhatkit.playonyt(music)


def busca(rec):
    search = rec.replace('busca', '')
    wikipedia.set_lang("es")
    wiki = wikipedia.summary(search, 1)
    talk(wiki)
    write_text(search + ": " + wiki)


def camara(rec):
    talk("Enseguida")
    t = tr.Thread(target=lucy_cam.capture)
    t.start()


def abre(rec):
    task = rec.replace('abre', '').strip()
    if task in sites:
        for task in sites:
            if task in rec:
                sub.call(f'start chrome.exe {sites[task]}', shell=True)
                talk(f'Abriendo {task}')
    elif task in apps:
        for task in apps:
            if task in rec:
                talk(f'Abriendo {task}')
                os.startfile(apps[task])
    else:
        talk(f'No se ha encontrado el programa {task}')


def archivo(rec):
    file = rec.replace('archivo', '').strip()
    if file in files:
        for file in files:
            if file in rec:
                sub.Popen([files[file]], shell=True)
                talk(f'Abriendo {file}')
    else:
        talk(f'No se ha encontrado el archivo {file}')


def escribe(rec):
    try:
        with open("nota.txt", 'a') as f:
            write(f)

    except FileNotFoundError as e:
        file = open("nota.txt", 'w')
        write(file)


def write(f):
    talk("¿Qué quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)


def termina(rec):
    talk("Hasta luego")
    main_window.destroy()
    sys.exit()


def clock(rec):
    num = rec.replace('alarma', '')
    num = num.strip()
    talk("Alarma activada a las " + num + " horas")
    if num[0] != '0' and len(num) < 5:
        num = '0' + num
    print(num)
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
            talk("DESPIERTA!!!")
            mixer.init()
            mixer.music.load("Game-of-Thrones.mp3")
            mixer.music.play()
        else:
            continue
        if keyboard.read_key() == "s" or 'stop' in rec == 'stop':
            mixer.music.stop()
            break


def thread_alarma(rec):
    t = tr.Thread(target=clock, args=(rec,))
    t.start()


def envia_mensaje(rec):
    talk("¿A quién quieres enviar el mensaje?")
    contacts = listen()
    contacts = contacts.strip().capitalize()

    if contacts in contact:
        for cont in contact:
            if cont == contacts:
                contacts = contact[cont]
                talk("Que mensaje quieres enviar")
                message = listen()
                talk("Enviando mensaje...")
                whapp.send_message(contacts, message)
    else:
        talk(f"No has agregado {contacts} a tu lista de contactos")


def buscame(rec):
    something = rec.replace('buscame', '').strip()
    talk("Buscando" + something)
    browser.search(something)


def conversar(rec):
    chat = ChatBot("lucy", database_uri=None)
    trainer = ListTrainer(chat)
    trainer.train([' '.join(tupla) for tupla in db.get_questionanswers()])
    talk("¿Quieres conversar?")

    while True:
        try:
            rec = listen()
        except UnboundLocalError:
            talk("No te entendí, intenta de nuevo")
            continue
        if 'busca' in rec:
            key_words['busca'](rec)
            break
        elif rec.split()[0] in key_words:
            key = rec.split()[0]        
            key_words[key](rec)
        else:
            print("Tú: ", rec)
            answer = chat.get_response(rec)
            print("Lucy: ", answer)
            talk(answer)
            if 'adios' in rec:
                break
    main_window.update()


def reconocimiento(rec):
    rec = rec.replace('reconocimiento', '').strip()
    if rec == 'activado':
        t = tr.Thread(target=fr.face_rec, args=(0,))
        t.start()
        talk("Activando reconocimiento")
    elif 'desactivado':
        talk("Desactivando reconocimiento")
        fr.face_rec(1)


def return_weather(city):
    url = f"https://es.wttr.in/{city}?format=j1"
    
    response = requests.get(url)
    weather_dic = response.json()

    temp_c = weather_dic["current_condition"][0]['temp_C']
    desc_temp = weather_dic["current_condition"][0]['lang_es']
    desc_temp = desc_temp[0]['value']
    return temp_c, desc_temp

def clima(rec):
    talk("De que pais o ciudad quiere saber el clima")
    city = listen()
    city = city.strip()
    temp_c, desc_temp = return_weather(city)
    talk(f"La temperatura actual de {city} es {temp_c} grados célcius, y esta {desc_temp}.")
    print(f"La temperatura actual de {city} es {temp_c} °C. {desc_temp}.")


def fecha(rec):
    fecha_actual = datetime.datetime.now()
    rec = rec.replace('qué', '').strip()
    if rec == 'hora':
        hour = fecha_actual.hour
        minute = fecha_actual.minute
        talk(f"Són las {hour} y {minute} minutos")

    elif 'dia es hoy':
        day = fecha_actual.day
        month = fecha_actual.strftime("%B")
        year = fecha_actual.year
        talk(f"La fecha actual es {day} de {month} de {year}.")


def gps(rec):
    api_url = "https://www.mapquestapi.com/directions/v2/route?"
    key = "gjf0lv1rsogl9qOiSoSpzkHVqUBTLcnn"
    talk("Diga el origen, o diga si para utilizar la ubicación actual")
    origin = listen()
    if origin == 'si':
        # Obtener la ubicación actual del usuario
        g = geocoder.ip('me')
        if not g.city:
            talk("No se pudo determinar la ubicación actual.")
        origin = g.city

    talk("Diga el destino")
    destination = listen()

    url = api_url + urllib.parse.urlencode({"key": key, "from": origin, "to": destination})
    json_data = requests.get(url).json()
    
    status_code = json_data["info"]["statuscode"]
    if status_code == 0:
        trip_duration = json_data["route"]["formattedTime"]
        distance = json_data["route"]["distance"] * 1.61
        talk(f"Información del viaje desde {origin.capitalize()} hasta {destination.capitalize()}.")
        talk(F"Duración del viaje: {trip_duration}")
        talk("Distancia: " + str("{:.2f}".format(distance) + " Kilómetros"))
        # talk("Indicaciones: de la ruta ")

        for each in json_data["route"]["legs"][0]["maneuvers"]:
            distance_remaining = distance - each["distance"] * 1.61
            texto_ingles = each["narrative"] + " (" + str("{:.2f}".format(distance_remaining)) + " Kilómetros faltantes)"
            distance = distance_remaining

            def traducir(texto):
                translator = Translator(service_urls=['translate.google.com'])
                translated = translator.translate(texto, src='en', dest='es')
                return translated.text

            texto_traducido = traducir(texto_ingles)
            talk(f"{texto_traducido}")


# Luego puedes utilizar el diccionario generado en tu función suma
def suma(rec):
    talk("Diga cuántos números quieres sumar")
    num = listen()
    num = mat.convertir_numero(num)
    
    if num is None:
        talk("No se pudo entender la cantidad de números.")
        return

    suma = 0
    for _ in range(num):
        talk("Diga un número:")
        num_input = listen()
        num_input = mat.convertir_numero(num_input)
        
        if num_input is None:
            talk("No se pudo entender el número.")
            return
        
        suma = suma + num_input
        
    talk(f"La suma es {suma}")


def traducir(rec):
    talk("Dime lo que quieres traducir")
    text = listen()
    translator = Translator(service_urls=['translate.google.com'])
    texto_traducido = translator.translate(text, src='en', dest='es')
    talk(f"Texto traducido: {texto_traducido.text}")


# diccionario con palabras claves
key_words = {
    "reproduce": reproduce,
    "busca": busca,
    "alarma": thread_alarma,
    "cámara": camara,
    "abre": abre,
    "búscame un archivo": archivo,
    "escribe": escribe,
    "termina": termina,
    "mensaje": envia_mensaje,
    "búscame": buscame,
    "conversar": conversar,
    "reconocimiento": reconocimiento,
    "clima": clima,
    "qué": fecha,
    "gps": gps,
    "suma": suma,
    "cálculo": realizar_operacion,
    "traducir": traducir
}

# funcion principal
def run_lucy():
    while True:
        try:
            rec = listen()
            arg = rec.split(" ")
            command = arg[0]
            word = ""
            if len(arg) > 1:
                word = arg[1]
            key_words[command](word)
            main_window.update()
        except UnboundLocalError:
            talk("No te entendi. intenta de nuevo")
            continue


# ventanas de Insertar
def open_app():
    global nameapp_entry, pathf_entry
    window_app = Toplevel()
    window_app.title("I-APP")
    window_app.geometry("300x200")
    window_app.resizable(0, 0)
    window_app.configure(background="#666F80")
    main_window.eval(f'tk::PlaceWindow {str(window_app)} center')

    title_label = Label(window_app, text="Insert APP",
                        fg="White", bg="#666F80", font=('Arial', 10, 'bold'))
    title_label.pack(pady=3)
    name_label = Label(window_app, text="Nombre", fg="White",
                       bg="#666F80", font=('Arial', 7, 'bold'))
    name_label.pack(pady=2)

    nameapp_entry = Entry(window_app)
    nameapp_entry.pack(pady=1)

    path_label = Label(window_app, text="Ruta", fg="White",
                       bg="#666F80", font=('Arial', 7, 'bold'))
    path_label.pack(pady=2)

    pathf_entry = Entry(window_app)
    pathf_entry.pack(pady=1)

    save_button = Button(window_app, text="Guardar", bg='#FF9EA0',
                         fg="black", width=7, height=1, command=add_app)
    save_button.pack(pady=4)


def open_web():
    global nameweb_entry, patha_entry
    window_web = Toplevel()
    window_web.title("I-WEB")
    window_web.geometry("300x200")
    window_web.resizable(0, 0)
    window_web.configure(background="#666F80")
    main_window.eval(f'tk::PlaceWindow {str(window_web)} center')

    title_label = Label(window_web, text="Insert WEb",
                        fg="White", bg="#666F80", font=('Arial', 10, 'bold'))
    title_label.pack(pady=3)
    name_label = Label(window_web, text="Nombre", fg="White",
                       bg="#666F80", font=('Arial', 7, 'bold'))
    name_label.pack(pady=2)

    nameweb_entry = Entry(window_web)
    nameweb_entry.pack(pady=1)

    path_label = Label(window_web, text="Ruta", fg="White",
                       bg="#666F80", font=('Arial', 7, 'bold'))
    path_label.pack(pady=2)

    patha_entry = Entry(window_web)
    patha_entry.pack(pady=1)

    save_button = Button(window_web, text="Guardar", bg='#FF9EA0',
                         fg="black", width=7, height=1, command=add_web)
    save_button.pack(pady=4)


def open_file():
    global namefile_entry, pathe_entry
    window_files = Toplevel()
    window_files.title("I-FILE")
    window_files.geometry("300x200")
    window_files.resizable(0, 0)
    window_files.configure(background="#666F80")
    main_window.eval(f'tk::PlaceWindow {str(window_files)} center')

    title_label = Label(window_files, text="Insert FILE",
                        fg="White", bg="#666F80", font=('Arial', 10, 'bold'))
    title_label.pack(pady=3)
    name_label = Label(window_files, text="Nombre", fg="White",
                       bg="#666F80", font=('Arial', 7, 'bold'))
    name_label.pack(pady=2)

    namefile_entry = Entry(window_files)
    namefile_entry.pack(pady=1)

    path_label = Label(window_files, text="Ruta", fg="White",
                       bg="#666F80", font=('Arial', 7, 'bold'))
    path_label.pack(pady=2)

    pathe_entry = Entry(window_files)
    pathe_entry.pack(pady=1)

    save_button = Button(window_files, text="Guardar", bg='#FF9EA0',
                         fg="black", width=7, height=1, command=add_file)
    save_button.pack(pady=4)


def open_contact():
    global namecontact_entry, pathc_entry
    window_contact = Toplevel()
    window_contact.title("I-CONTACT")
    window_contact.geometry("300x200")
    window_contact.resizable(0, 0)
    window_contact.configure(background="#666F80")
    main_window.eval(f'tk::PlaceWindow {str(window_contact)} center')

    title_label = Label(window_contact, text="Insert CONTACT",
                        fg="White", bg="#666F80", font=('Arial', 10, 'bold'))
    title_label.pack(pady=3)
    name_label = Label(window_contact, text="Nombre", fg="White",
                       bg="#666F80", font=('Arial', 7, 'bold'))
    name_label.pack(pady=2)

    namecontact_entry = Entry(window_contact)
    namecontact_entry.pack(pady=1)

    path_label = Label(window_contact, text="Numero", fg="White",
                       bg="#666F80", font=('Arial', 7, 'bold'))
    path_label.pack(pady=2)

    pathc_entry = Entry(window_contact)
    pathc_entry.pack(pady=1)

    save_button = Button(window_contact, text="Guardar", bg='#FF9EA0',
                         fg="black", width=7, height=1, command=add_contact)
    save_button.pack(pady=4)

# ventanas de añadir


def add_app():
    name_app = nameapp_entry.get().strip()
    path_app = pathf_entry.get().strip()

    apps[name_app] = path_app
    save_datos(name_app, path_app, "app.txt")
    talk(f'Se ha añadido {name_app} a la lista de apps')
    nameapp_entry.delete(0, "end")
    pathf_entry.delete(0, "end")


def add_web():
    name_web = nameweb_entry.get().strip()
    path_web = patha_entry.get().strip()

    sites[name_web] = path_web
    save_datos(name_web, path_web, "web.txt")
    talk(f'Se ha añadido {name_web} a la lista de webs')
    nameweb_entry.delete(0, "end")
    patha_entry.delete(0, "end")


def add_file():
    name_file = namefile_entry.get().strip()
    path_file = pathe_entry.get().strip()

    files[name_file] = path_file
    save_datos(name_file, path_file, "file.txt")
    talk(f'Se ha añadido {name_file} a la lista de archivos')
    namefile_entry.delete(0, "end")
    pathe_entry.delete(0, "end")


def add_contact():
    name_contact = namecontact_entry.get().strip().capitalize()
    path_contact = pathc_entry.get().strip().capitalize()

    contact[name_contact] = path_contact
    save_datos(name_contact, path_contact, "contact.txt")
    talk(f'Se ha añadido {name_contact} a la lista de contactos')
    namecontact_entry.delete(0, "end")
    pathc_entry.delete(0, "end")


# guardar datos añadidos
def save_datos(key, value, file_name):
    try:
        with open(file_name, "a") as f:
            f.write(key + "," + value + "\n")
    except FileNotFoundError as f:
        files = open(file_name, 'a')
        files.write(key + "," + value + "\n")


# te dice cuantos
def talk_sites():
    if bool(sites) == True:
        talk("Has agregado las siguientes paginas")
        for site in sites:
            talk(site)
    else:
        talk("No hay ninguna pagina")


def talk_app():
    if bool(apps) == True:
        talk("Has agregado los siguientes programas")
        for app in apps:
            talk(app)
    else:
        talk("No hay ningun programa")


def talk_file():
    if bool(files) == True:
        talk("Has agregado los siguientes archivos")
        for file in files:
            talk(file)
    else:
        talk("No hay ningun archivo")


def talk_contact():
    if bool(contact) == True:
        talk("Has agregado los siguientes contactos")
        for contacts in contact:
            talk(contacts)
    else:
        talk("No hay ningun contacto")

# te pregunta tu nombre y te saluda
def give_me_name():
    talk("Hola como te llamas")
    name = listen()
    name = name.strip()
    talk(f"Bienvenido {name}")

    try:
        with open("name.txt", 'w') as f:
            f.write(name)
    except FileNotFoundError:
        file = open("name.txt", 'w')
        file.write(name)


def say_hello():
    if os.path.exists("name.txt"):
        with open("name.txt", "r") as f:
            for name in f:
                talk(f"Bienvenido {name}")
    else:
        give_me_name()

# def thread_hello():
#     t = tr.Thread(target=say_hello)
#     t.start()


# thread_hello()



# botones
Button_voice_es = Button(main_window, text="Voz Español", fg="white",
                         bg="#666F80", font=("Arial", 8, "bold"), command=spanish_voice)
Button_voice_es.place(x=160, y=20)

Button_voice_us = Button(main_window, text="Voz Ingles", fg="white",
                         bg="#666F80", font=("Arial", 8, "bold"), command=english_voice)
Button_voice_us.place(x=450, y=20)

Button_speak = Button(main_window, text="Hablar", fg="white", bg="#666F80", font=(
    "Arial", 8, "bold"), command=read_and_talk)
Button_speak.place(x=40, y=470)

Button_listen = Button(main_window, text="Escuchar", fg="black",
                       bg="#FFFFFF", font=("Arial", 8, "bold"), command=run_lucy)
Button_listen.pack(pady=10)

Button_add_app = Button(main_window, text="Insert APP", fg="white",
                        bg="#666F80", height=1, font=("Arial", 8, "bold"), command=open_app)
Button_add_app.place(x=552, y=60)

Button_add_web = Button(main_window, text="Insert WEB", fg="white",
                        bg="#666F80", height=1, font=("Arial", 8, "bold"), command=open_web)
Button_add_web.place(x=552, y=140)

Button_add_file = Button(main_window, text="Insert FILE", fg="white",
                         bg="#666F80", height=1, font=("Arial", 8, "bold"), command=open_file)
Button_add_file.place(x=552, y=100)

Button_add_contact = Button(main_window, text="Insert CONTACT", fg="white",
                            bg="#666F80", height=1, font=("Arial", 8, "bold"), command=open_contact)
Button_add_contact.place(x=552, y=180)

Button_tell_app = Button(main_window, text="APPs agregadas", fg="white",
                         bg="#666F80", height=1, width=17, font=("Arial", 8, "bold"), command=talk_app)
Button_tell_app.place(x=510, y=660)

Button_tell_app = Button(main_window, text="FILEs agregados", fg="white",
                         bg="#666F80", height=1, width=17, font=("Arial", 8, "bold"), command=talk_file)
Button_tell_app.place(x=510, y=620)

Button_tell_app = Button(main_window, text="WEBs agregados", fg="white",
                         bg="#666F80", height=1, width=17, font=("Arial", 8, "bold"), command=talk_sites)
Button_tell_app.place(x=510, y=580)

Button_tell_app = Button(main_window, text="CONTACTs agregados", fg="white",
                         bg="#666F80", height=1, width=17, font=("Arial", 8, "bold"), command=talk_contact)
Button_tell_app.place(x=510, y=540)

main_window.mainloop()
