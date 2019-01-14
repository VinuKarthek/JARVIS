
import webbrowser
chrome = r'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe %s'
url = "https://www.google.com.sg/search?q=intel stock price"
print(url)
webbrowser.get(chrome).open(url)


