#ifndef BOARD_H
#define BOARD_H

#include <curses.h>


class Board{
    int m_width, m_height;
    int m_posx, m_posy;
    int m_mines;
    short **m_logic_board, **m_board;
    WINDOW *m_win;

    void init();
    void enumerate();
    int pickPosition(int x, int y, short option=1);
    void pickEmpty(int x, int y);
    void pickAll();
    void refresh();

public:
    Board(int posx, int posy, int width, int height, int mines);

    ~Board();

    WINDOW* getWindow(){return m_win;}

    void loop();
};



#endif
