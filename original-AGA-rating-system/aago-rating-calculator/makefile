# Makefile for BayRate
#
# Program requires the following libraries:
#   - MySql development libraries
#   - MySql++ library
#   - GNU Scientific Library
#   - Boost Library 

LIBS=-lm -lgsl -lgslcblas
INC=-I/usr/include/mysql
FLAGS=-O2 -Wall -Wextra -Wshadow

all: raago

raago: raago.cpp collection.o game.o player.o
	g++ $(FLAGS) collection.o game.o raago.cpp player.o $(INC) $(LIBS) -o raago

game.o: game.cpp game.h
	g++ $(FLAGS) -c game.cpp -o game.o $(INC) $(LIBS)

player.o: player.cpp player.h
	g++ $(FLAGS) -c player.cpp -o player.o $(INC) $(LIBS)

collection.o: collection.cpp collection.h
	g++ $(FLAGS) -c collection.cpp -o collection.o $(INC) $(LIBS)

clean:
	rm *.o
	rm raago
