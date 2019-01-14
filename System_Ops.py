import random
import time, os
from time import ctime
import subprocess
import win32con
import win32gui
import webbrowser as wb
import sys


class system_operations():
    
    def __init__(self,engine_object,sys_filepath):
        self.engine_object= engine_object
        self.path = sys_filepath
        self.browser = wb
        return 


    def text2int(self, textnum, numwords={}):
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
     
    def greeting(self, String):
        
        if "how are you" in String:
            #chooses a reply in randomn
            #later request reply from a Chatbot
            greet_responses = ["Never better", "doing awesome", "awesome", "doing great", "i am fine", "feeling like Version 2.0 already"]
            reply_responses = ["How can I assist you", "How can I be of service to you", "anything that I can help you with"]
            reply = (random.choice(greet_responses) +". "+ random.choice(reply_responses))
            self.engine_object.speak(reply)
            
        if "hello" in String or "hi" in String or "hey" in String:
            #chooses a reply in randomn
            #later request reply from a Chatbot
            greet_responses = ["yo buddy", "namaste", "yes boss", "welcome", "howdy","hello","hey watsupp"]
            reply_responses = ["How can I assist you", "How can I be of service to you", "anything that I can help you with"]
            reply = (random.choice(greet_responses) +". "+ random.choice(reply_responses))
            self.engine_object.speak(reply)
        return
            
    def openclose_application(self, intent, apps):
        app_dict = {'command prompt': 'cmd', 'paint' : 'mspaint', 'calculator':'calc', 'notepad': 'notepad', 
                'snipping tool' : 'snippingtool', 'sticky note': 'stikynot', 'skype' : self.path.office+'Lync.exe',
                'outlook' : self.path.office+'OUTLOOK.EXE' , 'settings' : '%windir%\System32\Control.exe', 'one note' : self.path.office+'ONENOTE.EXE',
                'word' : self.path.office+'WINWORD.EXE', 'excel':self.path.office+'EXCEL.EXE', 'ppt':self.path.office+'POWERPNT.EXE','vnc viewer': self.path.vncviewer,
                'notepad plus':self.path.notepadpp,'eclipse' : self.path.eclipse}
        for app in apps:
            if intent == "open_app":
                self.engine_object.speak( "opening "+app['value'])
                if app['value'] == "chrome" or app['value'] == "internet": 
                    wb.get(self.path.chrome).open("https://www.google.com.sg") 
                else:
                    print(app_dict[app['value']])
                    subprocess.Popen([app_dict[app['value']]])
            else: #Close_app intent


                self.engine_object.speak( "Closing "+app['value'])
                command = ("taskkill /im \""+app['value']+ ".exe\" /t")
                print(command)
                subprocess.call([command])
        return
    
    def clock(self):
        self.engine_object.speak(ctime())
        return
    
    def online(self):
        self.engine_object.speak('Booting......................')
        self.engine_object.speak('Checking driver status')
        self.engine_object.speak('Driver Initialization Complete')
        self.engine_object.speak('All Systems are at go')
        
    def offline(self):
        self.engine_object.speak('ok sir')
        self.engine_object.speak('closing system')
        self.engine_object.speak('disconnecting from server')
        self.engine_object.speak('going offline')
        quit()
        
    def shutdown(self):
        self.engine_object.speak('Initiating Shutdown')
        self.engine_object.speak('connecting to command prompt')
        self.engine_object.speak('shutting down your pc.')
        os.system('shutdown -s')
        quit()
        
    def logoff(self):
        return
    
    def close(self):
        handle = win32gui.FindWindow(None, '')
        win32gui.SetForegroundWindow(handle)
        win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)
    
    def maximize(self):
        Maximize = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(Maximize, win32con.SW_MAXIMIZE)
    
    def minimize(self):
        Minimize = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)




<!--stackedit_data:
eyJoaXN0b3J5IjpbLTY0MjE2OTEwNV19
-->