import os                       # Zugriff auf Systembefehle
import re                       # Regulaere Ausdruecke
from pathlib import Path        # Zugriff auf Systempfade
from random import shuffle      # Zufaelliges Anordnen von Listenelementen
from playsound import playsound # Einzige Funktion: Audiodateien abspielen

# Eine Installation des VLC-Players zur Nutzung dieses Moduls
# ist derzeit nicht notwendig!
# VLC kann allerdings einiges mehr als playsound()
# Zur Verwendung die beiden Zeilen einkommentieren
#from time import sleep      # Zeitliche Verzoegerung
#import vlc

############################# GLOBALE VARIABLEN ################################
musicFiles = list()

################################ OPERATIONEN ###################################
# Rekursive Operation entfernt alle problematischen Sonderzeichen wie ', ",
# Space, etc. aus Datei- und Verzeichnisnamen, sodass sichergestellt ist, dass
# playsound alle Dateien fehlerfrei wiedergeben kann
def renameFiles(currentWorkingDirectory):

    # Erzeugt Liste mit allen Dateien und Verzeichnissen im aktuellen
    # Verzeichnis
    files = os.listdir(currentWorkingDirectory)

    # Wechselt das Arbeitsverzeichnis in das aktuelle Verzeichnis
    os.chdir(currentWorkingDirectory)

    # Fuer jede Datei und jedes Verzeichnis im aktuellen Arbeitsverzeichnis
    for file in range(len(files)):

        # makefile hat eine Sonderrolle und sollte nicht angefasst werden
        # weitere Ausnahmen koennen hier verundet werden 
        if(str(files[file]) != "makefile"
        and str(files[file]) != "LICENSE"
        and str(files[file]) != "README.md"
        and str(files[file]) != "randomPlaylistGenerator.py"):
            
            # Datei gefunden, da "." enthalten => Datei umbenennen
            # find() liefert -1, wenn Zeichen nicht in String enthalten
            if str(files[file]).find(".") >= 0:
                stringOld = str(files[file])
                stringNew = re.sub('[^A-Za-z0-9./()-]+', '', stringOld)
                os.rename(stringOld, stringNew)

            # Verzeichnis gefunden, falls kein "." enthalten
            # => Verzeichnis umbenennen und rekursiver Aufruf in umbenannten
            # Verzeichnis
            else:
                stringOld = str(files[file])
                stringNew = re.sub('[^A-Za-z0-9/()-]+', '', stringOld)
                os.rename(stringOld, stringNew)

                # Merken des umbenannten Verzeichnisnamens anstelle des alten
                files[file] = stringNew

                # Rekursiver Aufruf mit identifiziertem und umbenannten Verzeichnis
                renameFiles(str(files[file]))

                # Nach dem rekursiven Aufruf wird wieder eine Ebene nach oben
                # gewechselt und dort weitergemacht
                os.chdir("..")


# Erzeugt eine zufaellige Liste aller im Verzeichnis befindlichen Musikdateien
def generatePlaylist():

    global musicFiles
    # Erzeugung einer Liste mit rekursiver Suche
    # nach allen Dateien mit der Endung .mp3
    musicFiles = list(Path(".").rglob("*.mp3"))

    # Anhanegen aller .wav und .m4a Dateien an die Liste
    musicFiles.extend(list(Path(".").rglob("*.wav")))
    musicFiles.extend(list(Path(".").rglob("*.m4a")))

    # Erzeugung der zufaelligen Reihenfolge der Musikdateien
    shuffle(musicFiles)

    for line in musicFiles:
        print(line)


# Erzeugt oder ueberschreibt eine reine Textdatei (.txt) mit Informationen ueber
# die Anzahl an enthaltenen Titeln und einer nummerierten Liste der enthaltenen
# Titel
def writePlaylistToFile():
    global musicFiles

    # "a" -> anhaengen, "w" -> ueberschreiben
    playList = open("playList.txt", "w")
    playList.write("In der Playlist sind " +
        str(len(musicFiles)) +
        " Dateien enthalten. \n \n")

    for file in range(len(musicFiles)):
        playList.write(str(file + 1) + ". " + str(musicFiles[file]) + "\n")

    playList.close()
    

# Spielt die aktuelle playlist ab und ordnet die Titel nach dem letzten Titel
# zufaellig neu an
def playPlaylist():
    global musicFiles

    print()
    print("In der Playlist sind " + str(len(musicFiles)) + " Dateien enthalten. \n")

    # Fuer jede Musikdatei in der playlist
    for file in range(len(musicFiles)):
        # Schreibe Namen des aktuellen Tracks auf die Konsole
        print(str(file + 1) + ". " + str(musicFiles[file]))

        # Einfachste Wiedergabe von Musikdateien, keine Optionen moeglich
        playsound(str(musicFiles[file]))

        # Wiedergabe von Musikdateien mit dem vlc-Player
        # Erzeugung eines MediaPlayer Objektes mit dem Dateinamen als String
        #player = vlc.MediaPlayer(str(musicFiles[file]))
        #player.play()
        # Ermittlung der Dauer der aktuellen Datei um auf Ende zu warten
        #sleep(1.5)
        #duration = player.get_length() / 1000 # spielt gesamte Datei ab
        #duration = 5 # spielt erste 5 Sekunden der Datei
        #sleep(duration)
        #player.stop()

    # Erneute Erzeugung einer zufaelligen Reihenfolge der Musikdateien
    # nachdem die Liste komplett durchgelaufen ist
    shuffle(musicFiles)
    writePlaylistToFile()

############################## VORBEREITUNGEN ##################################
# Alle Verzeichnisse und Dateien muessen zunaechst umbenannt werden, damit
# playsound() fehlerfrei funktioniert (insb. Leerzeichen und ' fuehren zu einem
# Fehler) Dies wird rekursiv ab dem aktuellen Arbeitsverzeichnis durchgefuehrt.
renameFiles(os.getcwd())

########################### ERZEUGUNG DER PLAYLIST #############################
generatePlaylist()

if len(musicFiles) != 0:
    ##################### SPEICHERN DER PLAYLIST IN DATEI ##########################
    writePlaylistToFile()

    ######################### ABSPIELEN DER PLAYLIST ###############################
    while 1:
        playPlaylist()
else:
    print()
    print("KEINE MUSIKDATEIEN IN DIESEM VERZEICHNIS ZU FINDEN!")
    print()
