from google.transit import gtfs_realtime_pb2
import time
import json
import urllib

grtURL = "http://192.237.29.212:8080/gtfsrealtime/TripUpdates"
ttcURL = "http://webservices.nextbus.com/service/publicJSONFeed?"

saved = [[], []]
companies = ["grt", "ttc"]

def readSavedLoc ():
    ## [{stop, routeID, stopID}]
    f = open ("Saved bus.txt", "r")
    for i in range (2):
        saved [i] = []
        for n in range (int (f.readline ())):
            tokens = f.readline ().rstrip("\n").split (">")
            saved [i].append ({"stop": tokens [0],
                               "routeID": tokens [1],
                               "stopID": tokens [2]})
    f.close ()


def getBus (route, num):
    if num >= len (saved [route]) or num < 0:
        return "ID out of bounds."
    stopName = saved [route] [num] ["stop"]
    routeID = saved [route] [num] ["routeID"]
    stopID = saved [route] [num] ["stopID"]
    ## data = [route[i] = {routeName, times[i] = sec}]
    data = getGRT (routeID, stopID) if route == 0 else getTTC (routeID, stopID)
    result = "Here are the predictions for the stop " + stopName + ".\n"
    if len (data [0] ["times"]) != 0:
        for route in data:
            route ["times"].sort ()
            result += "The " + route["routeName"] + " bus is in.\n"
            for i in range (min (3, len (route ["times"]))):
                time = int (route["times"][i])
                if time > (60 * 60):
                    result += str (i + 1) + ". Over an hour.\n"
                elif time < 60:
                    result += str (i + 1) + ". %d seconds.\n" % (time)
                else:
                    result += str (i + 1) + ". %d minutes and %d seconds.\n" % (divmod (time, 60))
    else:
        result += "There are no buses in the foreseeable future." 
    return result

def getTTC (routeID, stopID):
    predictionURL = ttcURL + "command=predictions&a=ttc&r=%s&s=%s" % (routeID, stopID)
    predictions = json.load (urllib.urlopen (predictionURL)) ["predictions"]

    if isinstance (predictions ["direction"], list):
        return map (lambda e: {"routeName": e ["title"],
                               "times": map (lambda x: x ["seconds"],
                                             e ["prediction"])},
                               predictions ["direction"])
    else:
        return [{"routeName": predictions ["direction"] ["title"],
                 "times": map (lambda x: x ["seconds"],
                               predictions ["direction"] ["prediction"])}]
    

def getGRT (routeID, stopID):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = urllib.urlopen(grtURL)
    feed.ParseFromString(response.read())
    times = []
    for entity in feed.entity:
        if entity.trip_update.trip.route_id == routeID:
            for s in entity.trip_update.stop_time_update:
                if s.stop_id == stopID:
                    times.append (int (s.arrival.time - time.time ()) - 30)
    return [{"routeName": routeID,
             "times": times}]

def getUsage ():
    result = "Invalid command. The recognized commands are: \n"
    result += "For saved stops: bus, list, optional company. \n"
    result += "For predictions: bus, company, ID. \n"
    result += "Where the company is either TTC or GRT and the ID is from the list command:"
    return result

def getList (level):
    result = "Listing saved stops: \n"
    for i in range (2) if level == -1 else [level]:
        result += "For Grand River Transit. \n" if i == 0 else "For Toronto Transit Commission. \n"
        for n in range (len (saved [i])):
            result += str (n + 1) + ". " + saved [i][n]["routeID"] + " bus at " + saved [i][n]["stop"] + ".\n"
    return result.rstrip ("\n")


def getCommands ():
    return ["bus"]

def getCompany (string):
    return 0 if "GRT" in command else 1

def processCommand (command):
    tokens = command.split ()
    if len (tokens) >= 2 and tokens [1] == "list":
        if len (tokens) == 3 and tokens [2] in companies:
            return getList (companies.index (tokens [2]))
        else:
            return getList (-1)
    
    if len (tokens) != 3 or (tokens [1] not in companies):
        return getUsage ()
    try:
        return getBus (companies.index (tokens [1]), int (tokens [2]) - 1)
    except ValueError:
        return getUsage ()

readSavedLoc ()
