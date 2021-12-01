//
// Created by Anastaisha on 28.11.2021.
//

#include "game.h"

char Game::check(const State &state) {
    auto res = check_horizontal(state);
    res = res == '*' ? check_vertical(state) : res;
    res = res == '*' ? check_left_diagonal(state) : res;
    res = res == '*' ? check_right_diagonal(state) : res;
    bool tie = true;
    for (int i = 0; i < 6; ++i) {
        tie &= state[0][i] != '*';
    }
    if (tie)
        return '_';
    return res;
}

void Game::make_turn(int column, char turn) {
    if (main_state[0][column] != '*')
        return;
    auto index = find_available_index(column);
    main_state[index][column] = turn;
    isCurrentPlayerTurn = !isCurrentPlayerTurn;
    auto win = check(main_state);
    if (win != '*') {
        isOver = true;
        if (win == '_')
            isTie = true;
        if (win == player)
            playerWin = true;
        else
            playerWin = false;
    }
}

int Game::find_available_index(int column) {
    for (int i = 5; i >= 0; --i)
        if (main_state[column][i] == '*')
            return i;
    return -1;
}

vector<int> Game::possible_columns(const State &state) {
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
    for (int i = 0; i < state.size(); ++i)
        for (int j = 0; j <= state.size() - 4; ++j)
            if (cmp(state[i][j], state[i][j + 1], state[i][j + 2], state[i][j + 3]))
                return state[i][j];
    return '*';
}

char Game::check_vertical(const State &state) {
    for (int i = 0; i <= state.size() - 4; i++)
        for (int j = 0; j < state[0].size(); j++)
            if (cmp(state[i][j], state[i + 1][j], state[i + 2][j], state[i + 3][j]))
                return state[i][j];
    return '*';
}

char Game::check_right_diagonal(const State &state) {
    for (int i = 0; i <= state.size() - 4; i++)
        for (int j = 0; j <= state.size() - 4; j++)
            if (cmp(state[i][j + 3], state[i + 1][j + 2], state[i + 2][j + 1], state[i + 3][j]))
                return state[i][j + 3];
    return '*';
}

char Game::check_left_diagonal(const State &state) {
    for (int i = 0; i < 3; i++)
        for (int j = 6; j > 2; j--)
            if (cmp(state[i + 3][j], state[i + 2][j - 1], state[i + 1][j - 2], state[i][j - 3]))
                return state[i][j + 3];
    return '*';
}

Game::Game(char playerTurn, char compTurn) : player(playerTurn), comp(compTurn) {
    isCurrentPlayerTurn = player == 'X';
}

void Game::show() {
    cout << "=====Game======" << endl;
    for (int i = 0; i < main_state.size(); ++i) {
        cout << "    ";
        for (int j = 0; j < main_state[0].size(); ++j)
            cout << main_state[i][j];
        cout << "    \n";
    }
    cout << "    ";
    for (int i = 0; i < main_state[0].size(); ++i) {
        cout << i;
    }
    cout << "    \n";
    cout << "===============\n";
    cout << "Enter valid column: " << endl;
}


map<State, int> Computer::generate_successors(const State &state, char turn) {
    map<State, int> successors;
    for (auto column: Game::possible_columns(state)) {
        successors[make_turn(column, state, turn)] = column;
    }
    return successors;
}

State Computer::make_turn(int column, const State &state, int turn) {
    State new_state(state);
    auto index = game.find_available_index(column);
    new_state[index][column] = turn;
    return new_state;
}

int Computer::min_max(const State &state, int depth, int alpha, int beta, bool maximizing) {
    auto res = game.check(state);
    if (res != '*') {
        if (res == '_')
            return 0;
        if (res == game.player)
            return -1;
        if (res == game.comp)
            return 1;
    }
    if (depth > 7)
        return 0;
    if (maximizing) {
        int best_score = INT_MIN;
        auto successors = generate_successors(state, game.comp);
        for (auto succ: successors) {
            auto score = min_max(succ.first, depth + 1, alpha, beta, false);
            best_score = score > best_score ? score : best_score;
            if (best_score > alpha)
                alpha = best_score;
            if (alpha >= beta)
                break;
        }
        return best_score;
    } else {
        int best_score = INT_MAX;
        auto successors = generate_successors(state, game.player);
        for (auto succ: successors) {
            auto score = min_max(succ.first, depth + 1, alpha, beta, true);
            best_score = score < best_score ? score : best_score;
            if (best_score < beta)
                beta = best_score;
            if (alpha >= beta)
                break;
        }
        return best_score;
    }
}

void Computer::make_best_turn() {
    int best_score = INT_MIN;
    auto best_turn = -1;
    auto successors = generate_successors(game.main_state, game.comp);
    for (auto succ: successors) {
        auto score = min_max(succ.first, 0, INT_MIN, INT_MAX, false);
        if (score > best_score) {
            best_score = score;
            best_turn = succ.second;
        }
    }
    game.make_turn(best_turn, game.comp);
}
