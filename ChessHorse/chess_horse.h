//
// Created by anastasia on 30.10.2021.
//

#ifndef UNTITLED_CHESS_HORSE_H
#define UNTITLED_CHESS_HORSE_H

#include <iostream>
#include <vector>
#include <stack>
#include <queue>
#include <array>
#include <bitset>
#include <utility>
#include <set>
#include <algorithm>
#include <random>
using namespace std;

const int DIM = 8;
extern array<int, 8> VERTICAL;
extern array<int, 8> HORIZONTAL;
extern array<int, 8> INDICES;

int heuristic(const bitset<DIM * DIM> &board, int i, int j);
bool inside_board(int i, int j);

struct ChessState {
    ChessState *prev = nullptr;
    bitset<DIM * DIM> board;
    pair<int, int> position = {rand() % DIM, rand() % DIM};
    int h = 0;
};

void print(ChessState* chessState);

class ChessHorse {
public:
    void bfs();

    void dfs();
    void a_star();
    void start();
    ChessState *state;
};

#endif //UNTITLED_CHESS_HORSE_H
