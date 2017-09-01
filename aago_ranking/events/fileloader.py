import sys
import re
from collections import defaultdict

class InvalidEventFileError(Exception):
    def __init__(self, message):
        super().__init__(message)

def loadEventRecord(event, _none, key, value):
    if key in ["Name", "StartDate", "EndDate"]:
        event[0][key] = value

def createNewPlayer(event, playerId):
    if playerId != len(event[1]):
        raise InvalidEventFileError("Player section id does not match section position within file: " + str(playerId))
    event[1].append({"id" : playerId})


def loadPlayerRecord(event, playerId, key, value):
    if key in ["Name", "Category"]:
        event[1][-1][key] = value

def createNewRound(event, roundId):
    if roundId != len(event[2]):
        raise InvalidEventFileError("Round section id does not match section position within file: " + str(roundId))
    event[2].append({"id" : roundId, "games" : defaultdict(dict)})

gamePattern = re.compile("(Game[0-9]+)(Player1|Player2|Result)$")

def loadRoundRecord(event, roundId, key, value):
    if key == "Date":
        event[2][-1]["date"] = value
        return
    m = re.match(gamePattern, key)
    if not m:
        raise InvalidEventFileError("Invalid game record key: '" + key + "'")
    gameId, attribute = m.groups()
    if attribute == "Result":
        if value == "B":
            value = "black"
        elif value == "W":
            value = "white"
        else:
            raise InvalidEventFileError("Invalid game record result: '" + value + "'")
        attribute = "result"
    elif attribute == "Date":
        attribute = "date"
    else:
        assert attribute in ["Player1", "Player2"]
        if attribute == "Player1":
            attribute = "white_player"
        else:
            attribute = "black_player"
        try:
            ival = int(value)
            if ival < 0 or ival >= len(event[1]):
                raise ValueError()
        except ValueError:
            raise InvalidEventFileError("Invalid player id: '" + value + "'")
        value = ival
    event[2][-1]["games"][gameId][attribute] = value


sectionPattern = re.compile("([^0-9]+)([0-9]+)$")

def loadEventFile(f):
    event = ({},[],[]) # Event data, players, rounds
    sectionName = sectionNumber = None
    sectionCreationFunction         = { "Player" : createNewPlayer, "Round" : createNewRound} 
    recordLoadingFunctionForSection = { "Options" : loadEventRecord , "Player" : loadPlayerRecord, "Round" : loadRoundRecord} 
    validSections = recordLoadingFunctionForSection.keys()
    for l in f:
        l = l.strip()
        if l.startswith('[') and l.endswith(']'):
            sectionName = l[1:-1]
            m = re.match(sectionPattern, sectionName)
            if m:
                sectionName , sectionNumber = m.groups()
                sectionNumber = int(sectionNumber)
            else:
                sectionNumber = None
            if not sectionName in validSections:
                raise InvalidEventFileError("Invalid section: '" + sectionName + "'")
            if sectionName in sectionCreationFunction:
                sectionCreationFunction[sectionName](event, sectionNumber)
        else:
            parts = l.split('=')
            if len(parts) != 2:
                raise InvalidEventFileError("Line is neither 'key=value' nor '[section]' : '" + l + "'")
            key, value = parts
            recordLoadingFunctionForSection[sectionName](event, sectionNumber, key, value)
    for r in event[2]:
        r["games"] = list(r["games"].values())
    return event

if __name__ == "__main__":
    with open(sys.argv[1],"r", encoding="latin-1") as f:
        print(loadEventFile(f)[2])
