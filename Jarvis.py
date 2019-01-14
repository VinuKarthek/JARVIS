
from chatterbot import ChatBot
#System imports
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import sys

import nltk_API as wit 
import json_api as json
import System_Ops as syst
import Google_Ops as google
import Engine as cpu

sys.path.append(r'..\Jarvis\Typedefs')
#Custom imports
import path_def as path

debug = True
def toprint(printcontent):
    if(debug):
        print ('{}'.format(printcontent))

def Chatbot():
    chatbot = ChatBot('Ron Obvious',trainer='chatterbot.trainers.ChatterBotCorpusTrainer')
    # Train based on the English corpus
    chatbot.train("chatterbot.corpus.english")
    text = input("You : ")
    print("Bot : ")
    print(chatbot.get_response(text))
    
def jarvis(Engine,sys_obj,google_obj,String):
    
    wit_json = Engine.wit_decode(String)
    print(wit_json["msg_id"]+ "-" + wit_json["_text"])
    entity = wit_json["entities"]
    
    if 'intent' in entity:
        
        intent_list = entity["intent"]
        intent = ''
        for item in intent_list:
            if (float(item['confidence']) *100) >= 90:
                intent = item['value']
    

        if intent == "greeting":
            sys_obj.greeting(String)
        
        if intent == "open_app" or intent == "close_app":
            app_list = entity['app']
            sys_obj.openclose_application(intent , app_list)
        
        if intent == "get_time":
            sys_obj.clock()
        
        if intent == "get_direction":
            google_obj.google_maps(String)
        
        if intent == "google_search":
            google_obj.google_search(String)
            
        if intent == "weather":
            location = entity['location'][0]
            google_obj.google_search('weather '+location)
            
        if intent== "stock_market":
            for company in entity['company']:
                for info in entity['stock_info']:
                    google_obj.google_search(company['value']+ " "+ info['value'])
                        
    elif(float(entity['wikipedia_search_query'][0]['confidence'])>=0.9):
        google_obj.google_search(String)
    
    else:
        print("No Intent detected!!")
        
    #print (text2int("seven billion one hundred million thirty one thousand three hundred thirty seven"))

def main():
    Engine = cpu.engine()
    sys_obj = syst.system_operations(Engine,path)
    google_obj = google.google_opertaions(Engine,path)
    #syst.online()
    while 1:
        command = Engine.recordAudio()  #"close excel and outlook"#
        command = command.lower()   
        if not command == 'error':
            jarvis(Engine,sys_obj,google_obj,command)
        if command == 'stop':
            break
        #quit()
    sys_obj.offline()    
    
    
if __name__ == '__main__': 
    main()