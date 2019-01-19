#!/usr/bin/python3

from lxml import etree
import collections

INITIAL_SCORES={
#    "VILLASALTEGOMEZCRISTIANALBERTO" : 1,
#    "ARESFEDERICO" : 0,
#    "BENROBERTO" : 1,
#    "GUIAMETJAIME" : 1,
#    "CHAVEZMATIAS" : 1,
#    "PAPESCHIROSARIO" : 1,
#    "COMITOANDRES" : 1,
#    "D'ALBUQUERQUEFRANCISCOMANUEL" : 1,
#    "GARROFEMARTÍN" : 1,
#    "LAPLAGNESANTIAGO" : 1,
#    "ACOSTAJOEL" : 0,
#    "MACGOWANDWAYNE" : 0,
#    "ONEGAMURRAYJOSÉMARÍA" : 0,
#    "DEFINEFERNANDOARIEL" : 0,
#    "ZINNILUCIANO" : 0,
#    "PEREIRAGONZALO" : 0,
#    "VIÑASJUAN" : 0,
#    "PICCIONIJOSE" : 0,
#    "CHINMOONSUNG" : 1,
#    "GARCÍANAHUEL" : 1,
#    "TABARESSANTIAGO" : 1,
#    "ROMEROMARIAAGOSTINA" : 1,
#    "BROWNHAROLDO" : 1,
#    "CORREAFRANCOIGNACIO" : 1,
#    "ALBORNOZMATEO" : 0,
#    "GASTINGISSELLA" : 1,
#    "LINDENBAUMENRIQUE" : 0,
#    "GIMENEZHORACIO" : 0,
#    "VÁZQUEZCAMILO" : 0,
#    "CIFREBERNARDO" : 0,
#    "MARENGONICOLÁS" : 0,
#    "BYEBYE" : 0,
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
        participants[playerId] = (playerFirstName + " " + playerSurname, rank)
    allRounds = groupByRounds(map(parseGame, tree.find("Games").findall("Game")))
    totalRounds = int(tree.find("TournamentParameterSet").find("GeneralParameterSet").get("numberOfRounds"))
    print("Rounds={}".format(totalRounds))
    print("ActualRound={}".format(len(allRounds)-1))
    print("Numberofplayers={}".format(len(participants)))
    participantsToId = dict()
    for i, (pid, (name, rank)) in enumerate(sorted(participants.items(), key = lambda item : value(item[1][1]), reverse = True )):
        participantsToId[pid] = i+1
        print("[Player{}]".format(i+1))
        print('Name="{}"'.format(name))
        print("Category={}".format(rank))
        if pid in INITIAL_SCORES:
            print("InitialScore={}".format(INITIAL_SCORES[pid]))
    #for x in dir(tree):
    #    print(x)
    #exit()
    for roundNumber, games in allRounds.items():
        print("[Round{}]".format(roundNumber))
        for gameId, (_, whitePlayer, blackPlayer, handicap, result) in enumerate(games):
            print("Game{}Player1={}".format(gameId, participantsToId[whitePlayer]))
            print("Game{}Player2={}".format(gameId, participantsToId[blackPlayer]))
            #print("Game{}Handicap={}".format(gameId, handicap)) Revisar bien en el parsing, como se guarda el handicap, que sea compatible [casi seguro lo es]
            #print("Game{}VictoriaPor={}".format(gameId, handicap)) Ver que onda la reason
            print("Game{}Result={}".format(gameId, result))

    #print(tree.tag)
    #print(tree.attrib)
    #print(repr(tree.text))
    #print("*")
    #for cosa in tree.iterchildren():
    #    print(cosa)
    pass

if __name__ == "__main__":
    import sys
    toAago(sys.stdin, sys.stdout)
