//
// Created by Anastaisha on 28.10.2021.
//
#include "game.h"


int main() {
    int turn;
    while (true) {
        cout << "choose your turn(enter 1 or 2): " << endl;
        cin >> turn;
        if (turn == 1 || turn == 2)
            break;
        else
            cout << "try again!" << endl;
    }
    char computer, player;
    if (turn == 1) {
        computer = 'O';
        player = 'X';
    } else {
        computer = 'X';
        player = 'O';
    }
    Game game(player, computer);
    Computer comp(game);
    int playerTurn = -1;
    while (true) {
        if(turn == 1) {
            comp.game.show();
            cin >> playerTurn;
            cout<<endl;
            comp.game.make_turn(playerTurn, player);
            comp.make_best_turn();
        }
        else{
            comp.make_best_turn();
            comp.game.show();
            cin>>playerTurn;
            cout<<endl;
            comp.game.make_turn(playerTurn, player);
        }
        if(comp.game.isOver) {
            break;
        }
    }
    if(comp.game.isTie)
        cout << "It's a tie";
    else if(comp.game.playerWin)
        cout << "You win";
    else
        cout << "Triumph of artificial intelligence";
    return 0;
}
