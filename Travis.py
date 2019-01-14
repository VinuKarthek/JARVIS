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
import win32con
import win32gui

sys.path.append(r'..\Travis\Typedefs')
#Custom imports
import path_def as path

#Text Processing
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import NLP_API as wit 
import pyttsx3

engine = pyttsx3.init()
rate = engine.getProperty('rate')
volume = engine.getProperty('volume')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


debug = True

def toprint(printcontent):
    if(debug):
        print ('{}'.format(printcontent))

def text2int(textnum, numwords={}):
    if not numwords:
        units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",      ]
        
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        
        scales = ["hundred", "thousand", "million", "billion", "trillion"]
        
        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):    numwords[word] = (1, idx)
        for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

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
        toprint("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        toprint("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data    
 
def greeting(String):
    
    if "how are you" in String:
        #chooses a reply in randomn
        #later request reply from a Chatbot
        greet_responses = ["Never better", "doing awesome", "awesome", "doing great", "i am fine", "feeling like Version 2.0 already"]
        reply_responses = ["How can I assist you", "How can I be of service to you", "anything that I can help you with"]
        reply = (random.choice(greet_responses) +". "+ random.choice(reply_responses))
        speak(reply)
        
    if "hello" in String or "hi" in String:
        #chooses a reply in randomn
        #later request reply from a Chatbot
        greet_responses = ["yo buddy", "namaste", "yes boss", "welcome", "howdy","hello","hey watsupp"]
        reply_responses = ["How can I assist you", "How can I be of service to you", "anything that I can help you with"]
        reply = (random.choice(greet_responses) +". "+ random.choice(reply_responses))
        speak(reply)
    return
        
def openclose_application(intent, apps):
    app_dict = {'command prompt': 'cmd', 'paint' : 'mspaint', 'calculator':'calc', 'notepad': 'notepad', 
            'snipping tool' : 'snippingtool', 'sticky note': 'stikynot', 'skype' : path.office+'Lync.exe',
            'outlook' : path.office+'OUTLOOK.EXE' , 'settings' : '%windir%\System32\Control.exe', 'one note' : path.office+'ONENOTE.EXE',
            'word' : path.office+'WINWORD.EXE', 'excel':path.office+'EXCEL.EXE', 'ppt':path.office+'POWERPNT.EXE','vnc viewer': path.vncviewer,
            'notepad plus':path.notepadpp,'eclipse' : path.eclipse}
    for app in apps:
        if intent == "open_app":
            for app in app.split(" "):
                speak( "opening "+app)
                if input == "chrome" or input == "internet": 
                    wb.get(path.chrome).open("https://www.google.com.sg") 
                else:
                    print(app_dict[app])
                    subprocess.Popen([app_dict[app]])
        else: #Close_app intent
            for app in app.split(" "):
                speak( "Closing "+app)
                command = ("taskkill /im \""+app+ ".exe\" /t")
                print(command)
                subprocess.call([command])
    return

def clock():
    
    speak(ctime())
    return

def google_maps(String):
    
    if "where is" in String:
        String = String.split(" ")
        location = String[2]
        speak("Hold on, I will show you where " + location + " is.")
        wb.get(path.chrome).open("https://www.google.nl/maps/place/" + location + "/&amp;")
    return

def google_search(String):
    url = "https://www.google.com.sg/search?q="
    wb.get(path.chrome).open(url+String)
    return

def online():
    speak('Booting......................')
    speak('Checking driver status')
    speak('Driver Initialization Complete')
    speak('All Systems are at go')
    
def offline():
    speak('ok sir')
    speak('closing system')
    speak('disconnecting from server')
    speak('going offline')
    quit()
    
def shutdown():
    speak('Initiating Shutdown')
    speak('connecting to command prompt')
    speak('shutting down your pc.')
    os.system('shutdown -s')
    quit()
    
def logoff():
    return

def close():
    handle = win32gui.FindWindow(None, '')
    win32gui.SetForegroundWindow(handle)
    win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)

def maximize():
    Maximize = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(Maximize, win32con.SW_MAXIMIZE)

def minimize():
    Minimize = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)

def jarvis(String):
    
    decode_dict = wit.decode(String)
    
    if 'intent' in decode_dict:
        
        if decode_dict['intent'] == "greeting":
            greeting(String)
        
        if decode_dict['intent'] == "open_app" or decode_dict['intent'] == "close_app":
            intent = decode_dict['intent']
            app_list = decode_dict['app']
            openclose_application(intent , app_list)
            
                
        if decode_dict['intent'] == "pc_ctrl":
            for app in decode_dict['app']:
                open_application(app)        
        
        if decode_dict['intent'] == "get_time":
            clock()
        
        if decode_dict['intent'] == "get_direction":
            google_maps(String)
        
        if decode_dict['intent'] == "google_search":
            google_search(String)
            
        if decode_dict['intent'] == "weather":
            location = decode_dict['location'][0]
            google_search('weather '+location)
            
        if decode_dict['intent'] == "stock_market":
            for company in decode_dict['company']:
                for info in decode_dict['stock_info']:
                    google_search(company+ " "+ info)
                    
                    
    
    else:
        print("No Intent detected!!")
        
    #print (text2int("seven billion one hundred million thirty one thousand three hundred thirty seven"))


def Chatbot():
    chatbot = ChatBot('Ron Obvious',trainer='chatterbot.trainers.ChatterBotCorpusTrainer')
    # Train based on the english corpus
    chatbot.train("chatterbot.corpus.english")
    text = input("You : ")
    print("Bot : ")
    print(chatbot.get_response(text))

def main():
    online()
    while 1:
        command = recordAudio()  #"close excel and outlook"#
        command = command.lower()   
        if command == 'stop':
            break
        elif command == 'minimize':
            minimize()
        elif command == 'maximize':
            maximize()
        elif command == 'close':
            close()
        elif not command == 'error':
            jarvis(command)
        
        #quit()
    offline()    
    
    
if __name__ == '__main__': 
    main()