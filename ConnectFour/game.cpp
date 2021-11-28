//
// Created by Anastaisha on 28.11.2021.
//

#include "game.h"


int Game::check(const State &state) {
    auto res = check_horizontal(state);
    res = res == '*' ? check_vertical(state) : res;
    res = res == '*' ? check_left_diagonal(state) : res;
    res = res == '*' ? check_right_diagonal(state) : res;
    bool tie = true;
    for (int i = 0; i < 6; ++i) {
        tie &= state[0][i] != '*';
    }
    return res == 'X' ? 0 : res == 'O' ? 1 : tie ? 2 : -1;
}

void Game::make_turn(int column) {
    if (inner_state[0][column] != '*')
        return;
    auto index = find_available_index(column);
    inner_state[index][column] = 'X';
    isCurrentPlayerTurn = false;
    auto win = check(inner_state);
    switch (win) {
        case -1:
            break;
        default:
            isOver = true;
        case 0:
            humanWin = true;
            break;
        case 1:
            humanWin = false;
            break;
        case 2:
            isTie = true;
            break;
    }
}

int Game::find_available_index(int column) {
    for (int i = 5; i >= 0; --i)
        if (inner_state[column][i] == '*')
            return i;
    return -1;
}

vector<int> Game::possible_columns(const State state) {
    vector<int> columns;
    for (int i = 0; i < 6; ++i)
        if (state[0][i] == '*')
            columns.push_back(i);
    return columns;
}


bool Game::cmp(char first, char second, char third, char fourth) {
    return first != '*' && first == second && first == third && first == fourth;
}

char Game::check_horizontal(const State &state) {
    for (int j = 0; j < 6; ++j)
        for (int i = 0; i < 4; ++i)
            if (cmp(state[i][j], state[i + 1][j], state[i + 2][j], state[i + 3][j]))
                return state[i][j];
    return '*';
}

char Game::check_vertical(const State &state) {
    for (int i = 0; i < 7; i++)
        for (int j = 0; j < 3; j++)
            if (cmp(state[i][j], state[i][j + 1], state[i][j + 2], state[i][j + 3]))
                return state[i][j];
    return '*';
}

char Game::check_right_diagonal(const State &state) {
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 3; j++)
            if (cmp(state[i][j + 3], state[i + 1][j + 2], state[i + 2][j + 1], state[i + 3][j]))
                return state[i][j + 3];
    return '*';
}

char Game::check_left_diagonal(const State &state) {
    for (int i = 6; i > 2; i--)
        for (int j = 0; j < 3; j++)
            if (cmp(state[i][j + 3], state[i - 1][j + 2], state[i - 2][j + 1], state[i - 3][j]))
                return state[i][j + 3];
    return '*';
}

map<State, int> Gamer::generate_successors(const State& state, int turn) {
    map<State, int> successors;
    for (auto column: Game::possible_columns(state)) {
        successors[make_turn(column, state, turn)] = column;
    }
    return successors;
}