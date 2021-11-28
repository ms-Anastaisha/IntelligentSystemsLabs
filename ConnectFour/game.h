//
// Created by Anastaisha on 28.11.2021.
//

#ifndef CONNECTFOUR_GAME_H
#define CONNECTFOUR_GAME_H

#include <array>
#include <map>
#include <vector>

using namespace std;
using State = array<array<char, 6>, 7>;

class Game {
public:
    bool isFirstTurn = true;
    bool isCurrentPlayerTurn = true;
    bool isStarted = false;
    bool isOver = false;
    bool isTie = false;
    bool humanWin = false;

    int check(const State &state);

    void make_turn(int column);

    static vector<int> possible_columns(const State state);


private:
    State inner_state = {
            array<char, 6>{'*', '*', '*', '*', '*', '*'},
            array<char, 6>{'*', '*', '*', '*', '*', '*'},
            array<char, 6>{'*', '*', '*', '*', '*', '*'},
            array<char, 6>{'*', '*', '*', '*', '*', '*'},
            array<char, 6>{'*', '*', '*', '*', '*', '*'},
            array<char, 6>{'*', '*', '*', '*', '*', '*'},
            array<char, 6>{'*', '*', '*', '*', '*', '*'}};

    int find_available_index(int column);

    bool cmp(char first, char second, char third, char fourth);

    char check_horizontal(const State &state);

    char check_vertical(const State &state);

    char check_right_diagonal(const State &state);

    char check_left_diagonal(const State &state);
};

class Gamer {
    map<State, int> generate_successors(const State& state, int turn);
    State make_turn(int column, const State& state, int turn);
    int min_max(const State& state, int depth, int alpha, int beta, bool maximizing);
public:
    void make_best_turn(const State& state);
};

#endif //CONNECTFOUR_GAME_H
