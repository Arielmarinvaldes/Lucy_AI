import speech_recognition as sr
import subprocess as sub
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, lucy_cam, lucy_face, os
from pygame import mixer

name = "lucy"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)

sites = {
                'google':'google.com',
                'youtube':'youtube.com',
                'facebook':'facebook.com',
                'whatsapp':'web.whatsapp.com',
                'cursos':'freecodecamp.org/learn'
            }

file = {
                'despertador': 'Game-of-Thrones.mp3'
}

programs = {
    'whatsapp': r'C:\Users\amval\AppData\Local\WhatsApp.exe',
    'spotify': r'C:\Program Files\WindowsApps\SpotifyAB.SpotifyMusic_1.200.1165.0_x86__zpdnekdrzrea0\Spotify.exe',
    'nombre del programa': r'ruta del programa',
    'nombre del programa': r'ruta del programa'
}

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando... ")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()
            if name in rec:
                rec = rec.repalce(name, '')
    except:
        pass
    return rec

def run_lucy():
    while True:
        rec = listen()

        if 'reproduce' in rec:
            music = rec.replace('reproduce','')
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)

        elif 'busca'in rec:
            search = rec.replace('busca','')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            print(search +": " + wiki)
            talk(wiki)

        elif 'lucy alarma' in rec:
            num = rec.replace('alarma', '')
            num = num.strip()
            talk("Alarma activada a las " + num + " horas")

            while True:
                if datetime.datetime.now().strftime('%H:%M') == num:
                    print("DESPIERTA!!!")
                    mixer.init()
                    mixer.music.load("Game-of-Thrones.mp3")
                    mixer.music.play()
                    if keyboard.read_key() == "s" or 'stop' in rec == 'stop':
                        mixer.music.stop()
                        break

        elif 'lucy cámara' in rec:
            talk("Enseguida")
            lucy_cam.capture()

        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'start chrome.exe {sites[site]}', shell=True)
                    talk(f'Abriendo {site}')
            for app in programs:
                if app in rec:
                    talk(f'Abriendo {app}')
                    os.startfile(programs[app])

        elif 'lucy búscame un archivo' in rec:
            for file in files:
                if file in rec:
                    sub.Popen([files[file]], shell=True)
                    talk(f'Abriendo {file}')

        elif 'lucy escribe' in rec:
            try:
                with open("nota.txt", 'a') as f:
                    write(f)

            except FileNotFoundError as e:
                file = open("nota.txt", 'w')
                write(file)

        elif 'lucy termina' in rec:
            talk('Yá no necesitas de mi  e,    que te follen, Entonces me voy a dormir  adioss')
            break

def write(f):
    talk("¿Qué quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)



if __name__ == '__main__':
    run_lucy()
