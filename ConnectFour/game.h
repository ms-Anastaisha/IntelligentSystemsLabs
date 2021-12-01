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
using namespace std;
using State = array<array<char, 7>, 6>;

class Game {
public:
    char player, comp;
    bool isCurrentPlayerTurn;
    bool isStarted = false;
    bool isOver = false;
    bool isTie = false;
    bool playerWin = false;
    Game(char playerTurn, char compTurn);
    char check(const State &state);
    void show();
    void make_turn(int column, char turn);

    static vector<int> possible_columns(const State& state);

    int find_available_index(int column);
    State main_state = {
            array<char, 7>{'*', '*', '*', '*', '*', '*', '*'},
            array<char, 7>{'*', '*', '*', '*', '*', '*', '*'},
            array<char, 7>{'*', '*', '*', '*', '*', '*','*'},
            array<char, 7>{'*', '*', '*', '*', '*', '*','*'},
            array<char, 7>{'*', '*', '*', '*', '*', '*', '*'},
            array<char, 7>{'*', '*', '*', '*', '*', '*', '*'}};
private:



    bool cmp(char first, char second, char third, char fourth);

    char check_horizontal(const State &state);

    char check_vertical(const State &state);

    char check_right_diagonal(const State &state);

    char check_left_diagonal(const State &state);
};

class Computer {

    map<State, int> generate_successors(const State& state, char turn);
    State make_turn(int column, const State& state, int turn);
    int min_max(const State& state, int depth, int alpha, int beta, bool maximizing);
public:
    Game game;
    void make_best_turn();
    explicit  Computer(const Game& game1): game(game1){}
};

#endif //CONNECTFOUR_GAME_H
