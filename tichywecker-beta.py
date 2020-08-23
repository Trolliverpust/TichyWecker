from pygame import mixer
import phatbeat
import time, random, copy
from datetime import datetime

mixer.init(frequency=44100)

stundenzeiten = ["5uhr.mp3","6uhr.mp3","7uhr.mp3","8uhr.mp3","9uhr.mp3","10uhr.mp3","11uhr.mp3"]

minutenzeiten = ["fünf.mp3","zehn.mp3","fünfzehn.mp3","zwanzig.mp3","fünfundzwanzig.mp3","dreißig.mp3","fünfunddreißig.mp3","vierzig.mp3","fünfundvierzig.mp3","fünfzig.mp3","fünfundfünfzig.mp3","leer.mp3"]

weckermodus = True

bearbeitungsmodus = False

heuteschongeweckt = False

weckstunde = 7
weckminute = 30

stundenzeiger = 2
minutenzeiger = 5

def eine_aussage(a1):
    mixer.music.load(a1)
    mixer.music.play(0)
    while mixer.music.get_busy():
        pass

def drei_aussagen(a1,a2,a3):
    mixer.music.load(a1)
    mixer.music.play(0)
    while mixer.music.get_busy():
        pass

    mixer.music.load(a2)
    mixer.music.play(0)
    while mixer.music.get_busy():
        pass

    mixer.music.load(a3)
    mixer.music.play(0)
    while mixer.music.get_busy():
        pass

eine_aussage("tichy-startup.mp3")

@phatbeat.on(phatbeat.BTN_PLAYPAUSE)
def stoppen(pin):
    mixer.music.stop()

@phatbeat.on(phatbeat.BTN_ONOFF)
def weckmodus_umschalten(pin):
    global weckermodus
    weckermodus = not weckermodus
    if weckermodus:
        mixer.music.load("wecker_an.mp3")
        mixer.music.play(0)
    else:
        mixer.music.load("wecker_aus.mp3")
        mixer.music.play(0)

@phatbeat.on(phatbeat.BTN_REWIND)
def uhrzeitansagen(pin):
    drei_aussagen("aktuelleUhrzeit.mp3",stundenzeiten[stundenzeiger],minutenzeiten[minutenzeiger])

@phatbeat.on(phatbeat.BTN_FASTFWD)
def zeitsetzen(pin):
    global bearbeitungsmodus, weckstunde, weckminute, stundenzeiger, minutenzeiger
    if bearbeitungsmodus:
        drei_aussagen("einstellung_ende.mp3",stundenzeiten[stundenzeiger],minutenzeiten[minutenzeiger])
        heuteschongeweckt = False
        bearbeitungsmodus = False
        weckstunde = stundenzeiger + 5
        weckminute = ((minutenzeiger+1)*5)%60
        print(weckstunde, weckminute)
        if weckstunde == 8 and weckminute == 0:
            eine_aussage("dieArbeitbeginntum8Uhr.mp3")
        elif weckstunde == 6 and weckminute == 0:
            eine_aussage("sechsuhrfrüh.mp3")
        elif weckstunde == 7 and weckminute == 30:
            eine_aussage("siebenuhrdreißignichtfrüh.mp3")
        elif weckstunde > 8:
            eine_aussage("bisschenspät.mp3")

    else:
        bearbeitungsmodus = True
        drei_aussagen("aktuelleUhrzeit.mp3",stundenzeiten[stundenzeiger],minutenzeiten[minutenzeiger])
        eine_aussage("einstellung_start.mp3")

@phatbeat.on(phatbeat.BTN_VOLUP)
def stundenplus(pin):
    global bearbeitungsmodus, stundenzeiger, stundenzeiten
    if bearbeitungsmodus:
        stundenzeiger = (stundenzeiger+1)%7
        eine_aussage(stundenzeiten[stundenzeiger])
    else:
        eine_aussage("kein_bearbeitungsmodus.mp3")

@phatbeat.on(phatbeat.BTN_VOLDN)
def minutenplus(pin):
    global bearbeitungsmodus, minutenzeiger, minutenzeiten
    if bearbeitungsmodus:
        minutenzeiger = (minutenzeiger+1)%12
        eine_aussage(minutenzeiten[minutenzeiger])
    else:
        eine_aussage("kein_bearbeitungsmodus.mp3")


while True:
    n = datetime.now().time()

    if n.hour == 12 and heuteschongeweckt:
        heuteschongeweckt = False

    time.sleep(5)

    if weckermodus and not heuteschongeweckt:
        if weckstunde == n.hour and weckminute == n.minute:
            mixer.music.set_volume(1)

            heuteschongeweckt = True

            mixer.music.load("tichy.mp3")

            mixer.music.play(-1)
            while mixer.music.get_busy():
                pass
        n = datetime.now().time()
