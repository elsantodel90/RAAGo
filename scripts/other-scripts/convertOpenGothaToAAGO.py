#!/usr/bin/python3

from lxml import etree
import collections

INITIAL_SCORES={
    "SALERNOLUCIANO" : 1,
    "MOONSUNGCHIN" : 1,
    "LAPLAGNESANTIAGO" : 1,
    "COMITOANDRES" : 1,
    "GARCIANAHUEL" : 1,
    "PAPESCHIROSARIO" : 1,
    "CORREAFRANCO" : 1,
    "PICCIONIJOSE" : 1,
    "DEFINEFERNANDO" : 1,
    "ACOSTAJOEL" : 1,
    "LINDENBAUMENRIQUE" : 0,
    "ANDINIARMANDO" : 0,
    "FRANCOHAROLUCAS" : 0,
    "LONGAPABLO" : 0,
    "ONEGAJOSEMARIA" : 0,
    "VIÑASJUAN" : 0,
    "MARENGONICOLAS" : 0,
    "OROZCOJUANMANUEL" : 0,
}

def formatRank(rankString):
    return rankString.replace("D", " dan").replace("K", " kyu")

def parseResult(resultString):
    return {
              "RESULT_UNKNOWN" : "N",
              "RESULT_WHITEWINS" : "W",
              "RESULT_BLACKWINS" : "B",
           }[resultString]

# round, white, black, handicap, result
def parseGame(game):
    return (int(game.get("roundNumber"))-1, game.get("whitePlayer") , game.get("blackPlayer"), int(game.get("handicap")), parseResult(game.get("result")))

def groupByRounds(games):
    ret = collections.defaultdict(list)
    for g in games:
        roundNumber = g[0]
        ret[roundNumber].append(g)
    return ret

def value(rankString):
    numString, kind = rankString.split()
    num = int(numString)
    assert(num != 0) 
    if kind == "dan":
        return num
    elif kind == "kyu":
        return -num
    else:
        assert(False)

def toAago(inputFile, outputFile):
    outputFile.write("[Options]\n")
    
    tree = etree.parse(inputFile).getroot()
    participants = dict()
    # Los ids son apellidonombre en mayusculas sin espacios.
    # Y si esos ids colapsan? Testear...
    for p in tree.find("Players").findall("Player"):
        playerFirstName = p.get("firstName") 
        playerSurname = p.get("name")
        playerId = (playerSurname + playerFirstName).replace(" ","").upper()
        rank = formatRank(p.get("rank"))
        assert(playerId not in participants)
        participants[playerId] = (playerFirstName + " " + playerSurname, rank)
    allRounds = groupByRounds(map(parseGame, tree.find("Games").findall("Game")))
    totalRounds = int(tree.find("TournamentParameterSet").find("GeneralParameterSet").get("numberOfRounds"))
    outputFile.write("Rounds={}\n".format(totalRounds))
    outputFile.write("ActualRound={}\n".format(len(allRounds)-1))
    outputFile.write("Numberofplayers={}\n".format(len(participants)))
    participantsToId = dict()
    for i, (pid, (name, rank)) in enumerate(sorted(participants.items(), key = lambda item : value(item[1][1]), reverse = True )):
        participantsToId[pid] = i+1
        outputFile.write("[Player{}]\n".format(i+1))
        outputFile.write('Name="{}"\n'.format(name))
        outputFile.write("Category={}\n".format(rank))
        if pid in INITIAL_SCORES:
            outputFile.write("InitialScore={}\n".format(INITIAL_SCORES[pid]))
    for roundNumber, games in allRounds.items():
        outputFile.write("[Round{}]\n".format(roundNumber))
        for gameId, (_, whitePlayer, blackPlayer, handicap, result) in enumerate(games):
            outputFile.write("Game{}Player1={}\n".format(gameId, participantsToId[whitePlayer]))
            outputFile.write("Game{}Player2={}\n".format(gameId, participantsToId[blackPlayer]))
            #outputFile.write("Game{}Handicap={}\n".format(gameId, handicap)) Revisar bien en el parsing, como se guarda el handicap, que sea compatible [casi seguro lo es]
            #outputFile.write("Game{}VictoriaPor={}\n".format(gameId, ¿¿reason??)) Ver que onda la reason
            outputFile.write("Game{}Result={}\n".format(gameId, result))

if __name__ == "__main__":
    import sys
    toAago(sys.stdin, sys.stdout)
