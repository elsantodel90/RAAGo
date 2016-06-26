/*************************************************************************************

	Copyright 2010 Philip Waldron
	
    This file is part of BayRate.

    BayRate is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    BayRate is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with BayRate.  If not, see <http://www.gnu.org/licenses/>.
    
***************************************************************************************/

#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <map>
#include <algorithm>
#include <cassert>
#include "tdListEntry.h"
#include "collection.h"

using namespace std;

// trim from start (in place)
static inline void ltrim(std::string &s) {
    s.erase(s.begin(), std::find_if(s.begin(), s.end(), std::not1(std::ptr_fun<int, int>(std::isspace))));
}

// trim from end (in place)
static inline void rtrim(std::string &s) {
    s.erase(std::find_if(s.rbegin(), s.rend(), std::not1(std::ptr_fun<int, int>(std::isspace))).base(), s.end());
}

// trim from both ends (in place)
static inline void trim(std::string &s) {
    ltrim(s);
    rtrim(s);
}

string nextLine() {
    string line;
    getline(cin, line);
    trim(line);
    return line;
}

class BadRank : public exception {};

double parseRank(const string &category) {
    istringstream ss(category);
    int rankPartNumber; char rankPartKyuDan;
    ss >> rankPartNumber >> rankPartKyuDan;

    if  ( (rankPartKyuDan == 'k') || (rankPartKyuDan == 'K') )
        return -(rankPartNumber+0.5);
    else if  ( (rankPartKyuDan == 'd') || (rankPartKyuDan == 'd') )
        return rankPartNumber+0.5;
    else
        throw BadRank();
}

double stringToDouble(const string &s) {
    double ret; istringstream(s) >> ret;
    return ret;
}

void readPlayersInformation(map<int, tdListEntry> &tdList, collection &tournamentCollection) {
    string line = nextLine();
    assert(line == "PLAYERS");
	while (line = nextLine() , line != "END_PLAYERS") {
        istringstream lineInput(line);
        
        int playerId; string category;
        string previousRatingMuString , previousRatingSigmaString, previousRatingAgeInDaysString;
        lineInput >> playerId >> category >> previousRatingMuString >> previousRatingSigmaString >> previousRatingAgeInDaysString;
        const string NULL_STRING = "NULL";
        if (previousRatingMuString == NULL_STRING) {
            assert(previousRatingSigmaString == NULL_STRING);
            assert(previousRatingAgeInDaysString == NULL_STRING);
        }
        else {
            assert(previousRatingSigmaString != NULL_STRING);
            assert(previousRatingAgeInDaysString != NULL_STRING);
            tdListEntry entry;
            entry.id               = playerId;            
            entry.rating           = stringToDouble(previousRatingMuString);
            entry.sigma            = stringToDouble(previousRatingSigmaString);
            entry.ratingAgeInDays  = stringToDouble(previousRatingAgeInDaysString);
            entry.ratingUpdated    = false;
            tdList[entry.id] = entry;
        }
        
        player p;
        p.id = playerId;
        try {
            p.seed = parseRank(category);
        }
        catch (BadRank &) {
            cerr << "Player " << playerId << " has invalid rank: " << category << endl;
            exit(1);
        }
        tournamentCollection.playerHash[p.id] = p;
	}
}


void readGamesInformation(collection &tournamentCollection) {
    string line = nextLine();
    assert(line == "GAMES");
	while (line = nextLine() , line != "END_GAMES") {
        istringstream lineInput(line);
        string winner;
        game g;
        lineInput >> g.white >> g.black >> g.handicap >> g.komi >> winner;
        g.komi++; // Ajuste porque el modelo esta ajustado con reglas chinas, y usamos japonesas.
                
		if (winner == "WHITE")
			g.whiteWins = true;
		else if (winner == "BLACK")
			g.whiteWins = false;
		else {
			cerr << "Fatal error: unknown game winner " << winner << endl;
			exit (1);
		}
				
		tournamentCollection.gameList.push_back(g);
        
        assert(tournamentCollection.playerHash.find(g.white) != tournamentCollection.playerHash.end());
        assert(tournamentCollection.playerHash.find(g.black) != tournamentCollection.playerHash.end());
    }
}

int main()
{	
 	map<int, tdListEntry> tdList;
 	map<string, bool> argList;
 	collection c;
		
	readPlayersInformation(tdList, c);
    readGamesInformation(c);
	
    if (!c.gameList.empty()) {
        c.initSeeding(tdList);
        
        // Start with the fast rating algorithm.  If it fails, then go for the simplex method as a backup. 
        if (c.calc_ratings_fdf() != 0) {
            if (c.calc_ratings() != 0) {
                cerr << "Fatal error processing tournament" << endl;
                exit(1); 
            }
        }
        
        // Copy the new ratings into the internal TDList for the next tournament update
        for (map<int, player>::iterator It = c.playerHash.begin(); It != c.playerHash.end(); It++) {
            tdList[It->second.id].id     = It->second.id;			
            tdList[It->second.id].rating = It->second.rating;
            tdList[It->second.id].sigma  = It->second.sigma;
            tdList[It->second.id].ratingUpdated = true;
        }
    }
	
	for (map<int, tdListEntry>::iterator tdListIt = tdList.begin(); tdListIt != tdList.end(); tdListIt++) {
		if (tdListIt->second.ratingUpdated)
			cout << tdListIt->second.id << '\t' << tdListIt->second.rating << '\t' << tdListIt->second.sigma << endl;
	}
    return 0;
}
