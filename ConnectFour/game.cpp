//
// Created by Anastaisha on 28.11.2021.
//

#include "game.h"

Game::Game() {
    winner = 0;
    winningMove = -1;
    SEARCH_Y = {0, 0, -1, 1, -1, 1, -1, 1};
    SEARCH_X = {-1, 1, 0, 0, 1, -1, -1, 1};
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            game[y][x] = 0;
        }
    }
}

bool Game::move_is_valid(int move) {
    if (move < 0 || move > WIDTH)
        return false;
    return game[0][move] == 0;
}

int Game::get_winner() {
    return winner;
}

void Game::show(bool error) {
    cout << endl << "             1   2   3   4   5   6   7 ";
    cout << endl << "           |---------------------------|" << endl;
    cout << "           |";

    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            if (game[y][x] == 1)
                cout << " X |";
            else if (game[y][x] == -1)
                cout << " O |";
            else
                cout << " * |";
        }

        cout << endl << "           |---------------------------|" << endl;

        //Output the bottom of the game.
        if (y + 1 < HEIGHT)
            cout << "           |";
        else {
            if (winner != 0) {
                if (get_winner() == botTurn)
                    cout << "          Triumph of artificial intelligence !!";
                else
                    cout << "          Argh! Skin-tube won :(";
            } else if (error) {
                cout << "           !! INVALID MOVE, TRY AGAIN !!";
            } else {
                cout << "           |                           |";
            }
        }
    }
    cout << endl;
}

int Game::find_available_index(int slot) {
    int i = 0;
    for (i = 0; i < HEIGHT; i++) {
        if (game[i][slot] != 0)
            break;
    }
    return i;
}

int Game::move(int player, int slot) {
    if (!move_is_valid(slot)) {
        return 0;
    }
    int index = find_available_index(slot);

    if (--index >= 0) {
        game[index][slot] = player;

        if (this->check_win(slot) == WIN) {
            winner = player;
            winningMove = slot;
        }
    }

    return 1;
}

int Game::unmove(int slot) {
    int removed = 0;

    if (slot == winningMove) {
        winner = 0;
        winningMove = -1;
    }

    for (int i = 0; removed == 0 && i < HEIGHT; i++) {
        if (game[i][slot] != 0) {
            game[i][slot] = 0;
            removed = 1;
        }
    }

    return removed;
}


int Game::computer_move(int player) {
    if (winner != 0) {
        return 0;
    }

    srand(time(NULL));
    int bestMove = 4;
    int currScore = 0;
    int bestScore = INT_MIN;
    int worstScore = INT_MAX;
    array<int, 7> moveScores = {0, 0, 0, 0, 0, 0, 0};
    vector<int> bestScoreMoves;

    for (int move = 0; move < WIDTH; move++) {
        if (this->move_is_valid(move)) {
            currScore = this->min_max(move, DEPTH, INT_MIN, INT_MAX, player, 0);
            moveScores[move] = currScore;

            if (currScore > bestScore) {
                bestMove = move;
                bestScore = currScore;
            } else if (currScore < worstScore) {
                worstScore = currScore;
            }
        }
    }

    for (int i = 0; i < WIDTH; i++) {
        if (moveScores[i] == bestScore) {
            bestScoreMoves.push_back(i);
        }
    }

    if (bestScoreMoves.size() > 1) {
        do {
            bestMove = rand() % bestScoreMoves.size();
        } while (!this->move(player, bestScoreMoves[bestMove]));
    } else
        this->move(player, bestScoreMoves[0]);

    return 1;
}

int Game::min_max(int move, int depth, int alpha, int beta, int player, int boardScore) {
    this->move(player, move);
    boardScore += this->check_win(move);

    if (depth == 0 || winner != 0) {
        this->unmove(move);
        return boardScore;
    }
    int bestScore = INT_MIN;

    for (int childMove = 0; childMove < WIDTH; childMove++) {
        if (this->move_is_valid(childMove)) {
            int v = min_max(childMove, depth - 1, beta * -1, alpha * -1, player * -1, boardScore * -1);
            bestScore = max(bestScore, v);
            alpha = max(bestScore, v);
            if (alpha >= beta)
                break;
        }
    }
    this->unmove(move);
    return (bestScore * -1) - 10000;
}


int Game::check_win(int slot) {
    int y = find_available_index(slot);

    int player = game[y][slot];
    int yt, xt;
    int score = 0, count = 1, countMax = 1;
    int verticalHeight = 0, verticalHeightOfMax = 0;
    int dir1, dir2;
    bool inter = false;

    for (int axis = 0; axis < NUM_OF_DIRECTIONS; axis += 2) {
        dir1 = 3;
        dir2 = 0;
        while (dir1 >= 0) {
            yt = y;
            xt = slot;
            for (int j = 0; j < dir1 && !inter; j++) {
                yt += SEARCH_Y[axis];
                xt += SEARCH_X[axis];
                if (yt >= HEIGHT || yt < 0 || xt >= WIDTH || xt < 0)
                    break;

                if (game[yt][xt] == player) {
                    count++;
                } else if (game[yt][xt] == 0) {
                    for (int i = yt; i < HEIGHT; i++) {
                        if (game[i][xt] != 0)
                            break;

                        verticalHeight++;
                    }
                } else if (game[yt][xt] == player * -1) {
                    inter = true;
                }
            }
            if (count >= 4) {
                return WIN;
            } else if (inter) {
                count = 1;
            }
            yt = y;
            xt = slot;
            for (int j = 0; j < dir2 && !inter; j++) {
                yt += SEARCH_Y[axis + 1];
                xt += SEARCH_X[axis + 1];
                if (yt >= HEIGHT || yt < 0 || xt >= WIDTH || xt < 0)
                    break;

                if (game[yt][xt] == player) {
                    count++;
                } else if (game[yt][xt] == 0) {
                    for (int i = yt; i < HEIGHT; i++) {
                        if (game[i][xt] != 0)
                            break;

                        verticalHeight++;
                    }
                } else if (game[yt][xt] == player * -1) {
                    inter = true;
                }
            }
            if (count >= 4) {
                return WIN;
            } else if (inter) {
                count = 1;
            }
            if (count > countMax) {
                countMax = count;
                verticalHeightOfMax = verticalHeight;
            } else if (count == countMax && verticalHeight < verticalHeightOfMax) {
                verticalHeightOfMax = verticalHeight;
            }
            dir1--;
            dir2++;
            count = 1;
            verticalHeight = 0;
            inter = false;
        }
        if (countMax == 3) {
            score += 100000 - (verticalHeightOfMax);
        } else if (countMax == 2) {
            score += 10000 - (verticalHeightOfMax);
        } else {
            score += 100 - (verticalHeightOfMax);
        }
        countMax = 1;
    }
    return score;
}




