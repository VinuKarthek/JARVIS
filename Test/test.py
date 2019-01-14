import subprocess
import time, os
import speech_recognition as sr
from gtts import gTTS
import pyglet
from chatterbot import ChatBot
import webbrowser as wb

#System imports
import random
import time, os
from time import ctime
import sys
import subprocess

sys.path.append(r'..\Jarvis\Typedefs')

#Text Processing
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import nltk_API as wit 

import pyttsx3

engine = pyttsx3.init()
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
#subprocess.Popen(["cmd"])

#subprocess.Popen(["mspaint"])
# subprocess.Popen(["calc"])
# subprocess.Popen(["notepad"])
# subprocess.Popen(["snippingtool"])
# subprocess.Popen(["stikynot"])
# subprocess.Popen(["lync"])
# 
#   
# subprocess.Popen([r"OUTLOOK"])
# 
# subprocess.Popen(["%windir%\System32\Control.exe"])
# subprocess.Popen(["ONENOTE"])
# subprocess.Popen(["EXCEL"])
# subprocess.Popen(["WINWORD"])
# subprocess.Popen(["POWERPNT"])
# #"C:\Program Files (x86)\Notepad++\notepad++.exe"
# #C:\Users\vinuk\eclipse\java-neon\eclipse\eclipse.exe
# #"C:\Users\vinuk\Downloads\VNC-Viewer-6.1.1-Windows-64bit.exe"
# 
# app_dict = {'command prompt': 'cmd', 'paint' : 'mspaint', 'calculator':'calc', 'notepad': 'notepad', 
#             'snipping tool' : 'snippingtool', 'sticky note': 'stikynot', 'skype' : 'Lync',
#             'outlook' : 'OUTLOOK' , 'settings' : '%windir%\System32\Control.exe', 'one note': 'ONENOTE',
#             'word' : 'WINWORD', 'excel':'EXCEL', 'ppt':'POWERPNT','vnc viewer':r'C:\Users\vinuk\Downloads\VNC-Viewer-6.1.1-Windows-64bit.exe',
#             'notepad plus':r'C:\Program Files (x86)\Notepad++\notepad++.exe','eclipse' : r'C:\Users\vinuk\eclipse\java-neon\eclipse\eclipse.exe'}
# 
# print(app_dict['outlook'])
# 
# subprocess.Popen(["calc"])
# subprocess.Popen(app_dict['notepad'])
# print(subprocess.call(["pwd"], shell=True))
# office = r"C:\Program Files (x86)\Microsoft Office\root\Office16\\"
# subprocess.Popen(["calc"])
# subprocess.Popen(["mspaint"])
# 
# subprocess.Popen(["notepad"])
# subprocess.Popen(["snippingtool"])
# subprocess.Popen(["%windir%\System32\Control.exe"])
# quit()'''

from wit import Wit

debug = True

def toprint(printcontent):
    if(debug):
        print ('{}'.format(printcontent))
        
def init_wit(): 
    #Error - 'Wit' object has no attribute 'message'
    #Fix - pip uninstall pywit & pip install wit
    access_troken = "2EQHV7Q7EKT2XEOLC3HSO3KKIY2V2B3E" #Cell bot
    handle = Wit(access_troken)
    return handle

def decode(string):
    #Initialize wit.i
    handle = init_wit()
    #Get response message
    response =  handle.message(string)
    toprint(response)
    
    entities = response['entities'] ##Get entities from response
    #Get the intent & it's confidence
    intent, intent_confidence = "",0.0    
    out_dict = {}
    
    if 'intent' in entities:
        intent_list = entities['intent']
        for intent_dict in intent_list:
            
            if (float(intent_dict['confidence']) *100) >= intent_confidence:
                intent_confidence = (float(intent_dict['confidence']) *100) 
                intent = intent_dict['value']
        out_dict['intent'] = intent
        del entities['intent'] 
        
        
        for entity_name in entities:
            entity_list = entities[entity_name]
            subitem_list = []
            for subitem in entity_list:
                if (float(subitem['confidence']) *100) >= 90:
                    subitem_content = subitem['value']
                    subitem_content = subitem_content.split(" ")
                    subitem_list = subitem_list +subitem_content
            out_dict[entity_name] = subitem_list          
        print (out_dict)

    else:
        toprint('Response from with.ai: No intent detected!!')
    return out_dict

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recordAudio():
    # Record Audio, converts audio to Text
    # Returns Text
    r = sr.Recognizer()
    with sr.Microphone() as source: #Backgound Audio, Noise balanceing, Wake on call
        print("Say something!")
        audio = r.listen(source)
 
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        toprint("You said: " + data)
    except sr.UnknownValueError:
        data = 'error'
        speak("if you need motivation, you shouldn't be doing it")
        toprint("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        toprint("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data  



while 1 :
    #data = recordAudio()
    data = "open chrome outlook skype and eclipse"
    data = data.lower()  
    if not data == 'error':
        print(decode(data))