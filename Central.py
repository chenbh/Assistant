import Speech
moduleNames = ["Weather", "Testing", "Bus"]
modules = map (lambda e: __import__ ("modules." + e, fromlist=["__name__"]), moduleNames)

audio = Speech.Speech (True)
print "listening"
audio.toggleSpeak ()
while True:
    command = audio.getCommand ().lower ()
    print "command: " + command
    if any (x in command for x in ["exit", "quit", "stop"]):
        audio.speak ("Stopping program.")
        break
    elif "switch" in command:
        audio.toggleGoogle ()
    elif "sound" in command:
        audio.toggleSpeak ()

    if (audio.google):
        for module in modules:
            if any (x in command for x in module.getCommands ()):
                audio.speak (module.processCommand (command))
    

