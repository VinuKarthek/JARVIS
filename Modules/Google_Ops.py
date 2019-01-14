import webbrowser as wb

class google_opertaions():

    def __init__(self,engine_object,sys_filepath):
        self.engine_object= engine_object
        self.sys_filepath = sys_filepath
        self.browser = wb
        return 
    
    def google_maps(self,String):
        
        if "where is" in String:
            String = String.split(" ")
            location = String[2]
            self.engine_object.speak("Hold on, I will show you where " + location + " is.")
            self.browser.get(self.sys_filepath.chrome).open("https://www.google.nl/maps/place/" + location + "/&amp;")
        return
    
    def google_search(self,String):
        url = "https://www.google.com.sg/search?q="
        self.browser.get(self.sys_filepath.chrome).open(url+String)
        return