//
// Created by Anastaisha on 28.10.2021.
//

#ifndef CONNECTFOUR_GAME_H
#define CONNECTFOUR_GAME_H

#include <array>
#include <map>
#include <vector>
#include <limits>
#include <iostream>
#include <algorithm>
#include <climits>
#include <stdlib.h>
#include <time.h>
#include <list>

const int HEIGHT = 6;
const int WIDTH = 7;
const int NUM_OF_DIRECTIONS = 8;
const int DEPTH = 8;
const int WIN = 10000000;


using namespace std;

class Game {

    int game[HEIGHT][WIDTH];
    int winner;

    int winningMove;

    array<int, NUM_OF_DIRECTIONS> SEARCH_X;
    array<int, NUM_OF_DIRECTIONS> SEARCH_Y;

    int check_win(int slot);

    int unmove(int slot);

    int find_available_index(int slot);

    int min_max(int move, int depth, int alpha, int beta, int player, int boardScore);

public:
    int botTurn;

    Game();

    int move(int player, int slot);

    bool move_is_valid(int move);

    int computer_move(int player);

    int get_winner();

    void show(bool error = false);

};

#endif //CONNECTFOUR_GAME_H
