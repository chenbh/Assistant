import json
import urllib

#ed3912f6a337ed4a
uwURL = "https://api.uwaterloo.ca/v2/weather/current.xml"

def getQuery (location):
    query = "select * from weather.forecast where woeid in "
    query = query + "(select woeid from geo.places(1) where text='%s') and u='c'" % (location)
    return "https://query.yahooapis.com/v1/public/yql?q=" + urllib.quote (query) + "&format=json"

def getData (location):
    yahooURL = getQuery (location)
    results = json.load (urllib.urlopen (yahooURL)) ["query"] ["results"]
    if results == "null" or ("Error" in results ["channel"] ["title"].split ()):
        return None
    else:
        report = results ["channel"]
        return [report ["location"] ["city"],
                report ["location"] ["country"],
                report ["item"] ["condition"] ["text"],
                report ["item"] ["condition"] ["temp"],
                report ["wind"] ["chill"],
                report ["item"] ["forecast"] [0] ["low"],
                report ["item"] ["forecast"] [0] ["high"]]


def getText (location):
    results = getData (location)
    
    if results is None:
        return "Could not find city %s" % (location)
    
    text = "The weather for %s, %s is %s. " % (results [0], results[1], results[2])
    text += "The current temperature is %s. " % (results [3])
    if results[4] < results[3]:
        text += "There is a windchill of %s. " % (results[4])
    text += "Today has a low of %s and a high of %s degrees." % (results[5], results[6])
    return text


def getCommands ():
    return {"weather", "temperature", "forecast"}


def processCommand (command):
    tokens = command.split (" ", 1)
    if len (tokens) > 1:
        return getText (tokens[1])
    return getText ("Waterloo,Ca")
    
