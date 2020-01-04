#include <iostream>
#include "board.h"


void getConfig(int *config){
    WINDOW *win = newwin(5, 20, LINES / 2 - 2, COLS / 2 - 10);

    box(win, 0, 0);

    mvwprintw(win, 1, 1, "Width: ");
    mvwprintw(win, 2, 1, "Height: ");
    mvwprintw(win, 3, 1, "Mines: ");

    wrefresh(win);

    echo();

    mvwscanw(win, 1, 8, "%d", config);
    mvwscanw(win, 2, 9, "%d", config + 1);
    mvwscanw(win, 3, 8, "%d", config + 2);

    wclear(win);
    wrefresh(win);

    noecho();
}



int getPosx(int width){
    return (COLS - width) / 2;
}


int main(int argc, char const *argv[]){
    // width, height, mines
    int config[3];

    initscr();
    cbreak();
    noecho();

    start_color();

    getConfig(config);

    if(0 < config[0] && config[0] <= LINES - 2 && 0 < config[1] &&
        config[1] <= COLS - 2 - COLS / 2 && 0 < config[2] && config[2] <= config[0] * config[1]){
        //Board board(0, getPosx(COLS - 2 - COLS / 2), COLS - 2 - COLS / 2, LINES - 2, 200);
        Board board(0, getPosx(config[0]), config[0], config[1], config[2]);

        board.loop();
    }
    else{
        mvprintw(LINES / 2, COLS / 2 - 15, "Error with the configuration!");

        config[0] = getch();
    }

    endwin();

    return 0;
}
