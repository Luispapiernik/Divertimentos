#include <iostream>
#include "board.h"
#include "io.h"


int main(int argc, char const *argv[]){
    initscr();
    cbreak();
    noecho();

    Board board(0, 0, 10, 20, 5);
    board.loop();

    endwin();

    return 0;
}
