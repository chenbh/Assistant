import speech_recognition as sr
import gtts
import pygame
import tempfile

class Speech:
    
    
    def __init__ (self, debug):
        self.r = sr.Recognizer()
        self.r.pause_threshold = 0.6
        with sr.Microphone () as source:
            self.r.adjust_for_ambient_noise (source)
        pygame.mixer.init (16000)
        self.debug = debug
        self.mute = debug
        if debug:
            print "Debug mode on"
        self.google = True
        #self.toggleGoogle ()

    def toggleSpeak (self):
        self.mute = not self.mute
        print "Sound has been " + ("disabled." if self.mute else "enabled.")

    def speak (self, text):
        if self.mute:
            print "[mute spoke]" + text
            return
        f = tempfile.TemporaryFile (mode = "wb+")
        start = f.tell ()
        gtts.gTTS (text, lang = 'en').write_to_fp (f)
        f.seek (start)
        pygame.mixer.music.load (f)
        pygame.mixer.music.play ()
        while pygame.mixer.music.get_busy () == True:
            continue
        f.close ()
        print "[Spoke] " + text

    def toggleGoogle (self):
        if (self.google):
            self.speak ("Switching to Sphinx offline speech recognition.")
        else:
            self.speak ("Switching to Google online speech recognition.")
        self.google = not self.google

    def getCommand (self):
        if self.debug:
            return raw_input ("debug: ")
        googleKey = "AIzaSyAoWtaIKd4qVrcsNDrLJfmLqrpm9to-_fs"
        # obtain audio from the microphone
        with sr.Microphone () as source:
            audio = self.r.listen(source)
            
        try:
            if (self.google):
                return self.r.recognize_google(audio, key= googleKey)
            else:
                return self.r.recognize_sphinx(audio)
        except sr.UnknownValueError:
            return "Invalid command."
        except sr.RequestError as e:
            return "Could not request results from service; {0}".format(e)

##s = Speech ()
##s.speak ("test")
##s.speak ("heist")
##s.speak ("pest")
