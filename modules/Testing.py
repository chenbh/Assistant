def getCommands ():
    return {"speak", "say"}


def processCommand (command):
    return command.split (" ", 1)[1]
