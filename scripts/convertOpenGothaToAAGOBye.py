#!/usr/bin/python3

from lxml import etree
import collections

INITIAL_SCORES={
"ACOSTAJOEL" : 2,
"LAPLAGNESANTIAGO" : 2,
"GASTINGISSELLA" : 2,
"CHAVEZMATIAS" : 2,
"CHINMOONSUNG" : 2,
"BROWNHAROLDO" : 2,
"GUTIERREZAGUSTIN" : 2,
"GARROFEMARTIN" : 2,
"GARCIANAHUEL" : 2,
"VIZZARROVALLEJOSPEDRO" : 2,
"VAZQUEZCAMILO" : 1,
"HAYASHIMASAAKI" : 1,
"LINDENBAUMENRIQUE" : 1,
"PICCIONIJOSE" : 1,
"CORREAFRANCOIGNACIO" : 1,
"REBAGLIATTIHECTOR" : 1,
"PEREIRAGONZALO" : 1,
"PAPESCHIROSARIO" : 1,
}

def formatRank(rankString):
    return rankString.replace("D", " dan").replace("K", " kyu")

def parseResult(resultString):
    return {
              "RESULT_BOTHLOSE" : "2",
              "RESULT_BOTHLOSE_BYDEF" : "2",
              "RESULT_UNKNOWN" : "N",
              "RESULT_WHITEWINS" : "W",
              "RESULT_WHITEWINS_BYDEF" : "W",
              "RESULT_BLACKWINS" : "B",
              "RESULT_BLACKWINS_BYDEF" : "N",
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
    
    bye = 0
    for p in tree.find("ByePlayers").findall("ByePlayer") if tree.find("ByePlayers") is not None else []: 
        bye = 1

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
    if (bye == 1):
        outputFile.write("Numberofplayers={}\n".format(len(participants)+1))
    else:
        outputFile.write("Numberofplayers={}\n".format(len(participants)))
    outputFile.write("FirstPlayer=1\n")
    participantsToId = dict()
    for i, (pid, (name, rank)) in enumerate(sorted(participants.items(), key = lambda item : value(item[1][1]), reverse = True )):
        participantsToId[pid] = i+1
        outputFile.write("[Player{}]\n".format(i+1))
        #name8 = name.encode('utf-8')
        outputFile.write('Name="{}"\n'.format(name))
        outputFile.write("Category={}\n".format(rank))
        if pid in INITIAL_SCORES:
            outputFile.write("InitialScore={}\n".format(INITIAL_SCORES[pid]))
    if(bye == 1):
        outputFile.write("[Player{}]\n".format(len(participants)+1))
        outputFile.write('Name="{}"\n'.format("BYE"))
        outputFile.write("Category={}\n".format("30 kyu"))

    for roundNumber, games in allRounds.items():
        outputFile.write("[Round{}]\n".format(roundNumber))
        for gameId, (_, whitePlayer, blackPlayer, handicap, result) in enumerate(games):
            outputFile.write("Game{}Player1={}\n".format(gameId, participantsToId[whitePlayer]))
            outputFile.write("Game{}Player2={}\n".format(gameId, participantsToId[blackPlayer]))
            outputFile.write("Game{}Result={}\n".format(gameId, result))
            gg = gameId
            
        for p in tree.find("ByePlayers").findall("ByePlayer") if tree.find("ByePlayers") is not None else []:
            #outputFile.write("HOLAA!{}---{}--{}".format(p.get("roundNumber"), gg+1, participantsToId[p.get("player")]))            
            if p.get("roundNumber") == str(roundNumber+1):
                #outputFile.write("CHAUU")            
                outputFile.write("Game{}Player1={}\n".format(gg+1, participantsToId[p.get("player")]))
                outputFile.write("Game{}Player2={}\n".format(gg+1, len(participants)+1))
                outputFile.write("Game{}Result={}\n".format(gg+1, "W"))
            

if __name__ == "__main__":
    import sys
    import io
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    #input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    toAago(sys.stdin, sys.stdout)
