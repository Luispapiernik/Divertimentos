#ifndef BOARD_H
#define BOARD_H

#include <curses.h>


class Board{
    int m_width, m_height;
    int m_posx, m_posy;
    int m_mines;
    int m_num_flags=0, m_num_picked=0;
    short **m_logic_board, **m_board;
    WINDOW *m_win, *m_info_win;

    void init();
    void enumerate();
    int pickPosition(int x, int y, short option=1);
    void pickEmpty(int x, int y);
    void pickAll();
    void refresh_board();
    void refresh_info();

public:
    Board(int posx, int posy, int width, int height, int mines);

    ~Board();

    int loop();
};



#endif
