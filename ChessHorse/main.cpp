#include <iostream>
#include "chess_horse.h"
#include <time.h>

int main() {
    srand (time(nullptr));
    auto game = ChessHorse();
    game.start();
    game.a_star();
    print(game.state);
    return 0;
}
