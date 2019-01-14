import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import pyglet
from wit import Wit



class engine():
    
    def __init__(self):
        self.init_voice()
        self.init_sr()
        self.init_wit()
        self.debug = "True"
    
    def init_voice(self):
        #Voice Parameters
        self.engine = pyttsx3.init()
        self.rate = self.engine.getProperty('rate')
        self.volume = self.engine.getProperty('volume')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)
        
    def init_sr(self):
        #Recognition Parameters
        self.r = sr.Recognizer()
        self.uphones = sr.Microphone.list_microphone_names()
        
    def init_wit(self): 
        #Error - 'Wit' object has no attribute 'message'
        #Fix - pip uninstall pywit & pip install wit
        self.access_troken = "2EQHV7Q7EKT2XEOLC3HSO3KKIY2V2B3E" 
        self.wit_handle = Wit(self.access_troken)
        
    def wit_decode(self, decode_string):
        #Get response message
        json_response =  self.wit_handle.message(decode_string)
        self.toprint(str(json_response)+"\n")
        return json_response
        
    def toprint(self,printcontent):
        if( self.debug):
            print ('{}'.format(printcontent))
    
    def speak(self,text):
        self.engine.say(text)
        self.engine.runAndWait()
     
    def recordAudio(self):
        # Record Audio, converts audio to Text
        # Returns Text
        with sr.Microphone() as source: #Background Audio, Noise balancing, Wake on call
            # listen for 1 second and create the ambient noise energy level
            self.r.adjust_for_ambient_noise(source, duration=0.3)
            print("Say something!")
            audio = self.r.listen(source,phrase_time_limit=5)
     
        # Speech recognition using Google Speech Recognition
        data = ""
        try:
            # Uses the default API key
            # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            data = self.r.recognize_google(audio)
            self.toprint("You said: " + data)
        except sr.UnknownValueError:
            data = 'error'
            self.toprint("Google Speech Recognition could not understand audio")
        except self.sr.RequestError as e:
            self.toprint("Could not request results from Google Speech Recognition service; {0}".format(e))
     
        return data    
    
