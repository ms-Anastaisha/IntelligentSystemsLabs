//
// Created by anastasia on 30.10.2021.
//
#include "chess_horse.h"

array<int, 8> VERTICAL{-2, -1, 1, 2, 2, 1, -1, -2};
array<int, 8> HORIZONTAL{1, 2, 2, 1, -1, -2, -2, -1};
array<int, 8> INDICES{0, 1, 2, 3, 4, 5, 6, 7};

bool inside_board(int i, int j) {
    return (0 <= i) && (0 <= j) && (DIM > i) && (DIM > j);
}

int heuristic(const bitset<DIM * DIM> &board, int i, int j) {
    int h = 0;
    for (int k = 0; k < HORIZONTAL.size(); ++k) {
        auto i_ = i + VERTICAL[k], j_ = j + HORIZONTAL[k];
        if (inside_board(i_, j_) && !board.test(i_ * DIM + j_))
            h += 1;
    }
    return h - static_cast<int>(board.count());
}

void ChessHorse::start() {
    auto inner_state = new ChessState();
    inner_state->position = {rand() % DIM, rand() % DIM};
    inner_state->board.set(inner_state->position.first * DIM +
                           inner_state->position.second);
    state = inner_state;
}

void ChessHorse::dfs() {
    random_device rd;
    mt19937 g(rd());
    stack<ChessState *> s;
    s.push(state);
    while (!s.empty()) {
        auto cur = s.top();
        s.pop();
        if (cur->board.all()) {
            state = cur;
            cout << cur->board << endl;
            return;
        }
        shuffle(INDICES.begin(), INDICES.end(), g);
        for (int k: INDICES) {
            auto i = cur->position.first + VERTICAL[k],
                    j = cur->position.second + HORIZONTAL[k];
            if (!inside_board(i, j)) continue;
            if (cur->board.test(i * DIM + j)) continue;

            auto child = new ChessState();
            child->board = cur->board;
            child->board.set(i * DIM + j);

            child->position = {i, j};
            child->prev = cur;
            s.push(child);
        }
    }
}

void ChessHorse::bfs() {
    random_device rd;
    mt19937 g(rd());
    queue<ChessState *> s;
    s.push(state);
    while (!s.empty()) {
        auto cur = s.front();
        s.pop();
        closed_set.insert(cur->board.to_ullong());
        if (cur->board.all()) {
            state = cur;
            cout << cur->board << endl;
            return;
        }
        shuffle(INDICES.begin(), INDICES.end(), g);
        for (int k: INDICES) {
            auto i = cur->position.first + VERTICAL[k],
                    j = cur->position.second + HORIZONTAL[k];
            if (!inside_board(i, j)) continue;
            if (cur->board.test(i * DIM + j)) continue;

            auto child = new ChessState();
            child->board = cur->board;
            child->board.set(i * DIM + j);

            child->position = {i, j};
            child->prev = cur;
            s.push(child);
        }
    }
}

void ChessHorse::a_star() {
    random_device rd;
    mt19937 g(rd());
    set<unsigned long long> closed_set;
    closed_set.insert(state->board.to_ullong());
    auto cmp = [](ChessState *lhs, ChessState *rhs) {
        return lhs->h > rhs->h;
    };
    priority_queue<ChessState *, vector<ChessState *>, decltype(cmp)> opened_set(cmp);
    opened_set.push(state);
    while (!opened_set.empty()) {
        auto cur = opened_set.top();
        opened_set.pop();
        if (cur->board.all()) {
            state = cur;
            cout << "Solution reached" << endl;
            return;
        }
        closed_set.insert(cur->board.to_ullong());
        shuffle(INDICES.begin(), INDICES.end(), g);
        for (int k: INDICES) {
            auto i = cur->position.first + VERTICAL[k],
                    j = cur->position.second + HORIZONTAL[k];
            if (!inside_board(i, j)) continue;
            if (cur->board.test(i * DIM + j)) continue;

            auto child = new ChessState();
            child->board = cur->board;
            child->board.set(i * DIM + j);
            if (closed_set.count(child->board.to_ullong()) == 1) {
                delete child;
                continue;
            }
            child->position = {i, j};
            child->prev = cur;
            child->h = heuristic(cur->board, i, j);
            opened_set.push(child);
        }

    }
}


void print(ChessState *chessState) {
    auto cur = chessState;
    vector<ChessState *> chess_states;
    while (cur != nullptr) {
        chess_states.push_back(cur);
        cur = cur->prev;
    }
    reverse(chess_states.begin(), chess_states.end());
    for (auto state: chess_states)
        cout << state->position.first * DIM + state->position.second << " ";
    cout << endl;

    for (auto state: chess_states) {
        for (int i = 0; i < DIM; ++i) {
            for (int j = 0; j < DIM; ++j)
                if (state->board.test(i * DIM + j))
                    cout << 'X';
                else
                    cout << "O";
            cout << endl;
        }
        cout << "--------" << endl;
    }
}