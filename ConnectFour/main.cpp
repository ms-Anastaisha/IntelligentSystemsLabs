//
// Created by Anastaisha on 28.10.2021.
//
#include "game.h"

int start() {
    Game *game = new Game();
    int playerTurn = -1;
    int player = 1;

    bool error = false;
    int turn;
    while (true) {
        cout << "choose your turn(enter 1 or 2): " << endl;
        cin >> turn;
        if (turn == 1 || turn == 2)
            break;
        else
            cout << "try again!" << endl;
    }
    if (turn == 1) {
        game->botTurn = 2;
    } else {
        game->botTurn = 1;
    }

    while (true) {
        if (turn == 2) {
            game->computer_move(player);
            if (!error)
                player *= -1;
        }
        game->show(error);
        if (game->get_winner() != 0) {
            break;
        }
        cout << "Enter valid column" << ": ";
        cin >> playerTurn;
        if (!game->move(player, playerTurn))
            error = true;
        if (turn == 1) {
            if (!error)
                player *= -1;
            game->computer_move(player);
        }
        if (game->get_winner() != 0) {
            game->show(error);
            break;
        }
        if (!error)
            player *= -1;

    }
    return 0;
}


int main() {

    start();
    return 0;
}
