#include <curses.h>
#include <random>
#include <ctime>
#include "board.h"


void Board::enumerate(){
    int neighbor(0);
    for (int i = 0; i < m_height; ++i){
        for (int j = 0; j < m_width; ++j){
            neighbor = 0;
            if (m_board[i][j] == -1)
                continue;
            if (i - 1 >= 0 && j - 1 >= 0 && m_board[i - 1][j - 1] == -1)
                ++neighbor;
            if (i - 1 >= 0 && m_board[i - 1][j] == -1)
                ++neighbor;
            if (i - 1 >= 0 && j + 1 < m_width && m_board[i - 1][j + 1] == -1)
                ++neighbor;
            if (j - 1 >= 0 && m_board[i][j - 1] == -1)
                ++neighbor;
            if (j + 1 < m_width && m_board[i][j + 1] == -1)
                ++neighbor;
            if (i + 1 < m_height && j - 1 >= 0 && m_board[i + 1][j - 1] == -1)
                ++neighbor;
            if (i + 1 < m_height && m_board[i + 1][j] == -1)
                ++neighbor;
            if (i + 1 < m_height && j + 1 < m_width && m_board[i + 1][j + 1] == -1)
                ++neighbor;
            m_board[i][j] = neighbor;
        }
    }
}


void Board::init(){
    int mines(m_mines);
    int row, column;

    while(mines){
        row = rand() % m_height;
        column = rand() % m_width;

        if(m_board[row][column] != -1){
            m_board[row][column] = -1;
            --mines;
        }
    }

    enumerate();
}


Board::Board(int posx, int posy, int width, int height, int mines):
    m_width(width), m_height(height), m_posx(posx), m_posy(posy), m_mines(mines){

    srand(time(0));

    // inicializacion de elementos relacionados con curses
    m_win = newwin(m_height + 2, m_width + 2, m_posx, m_posy);

    m_logic_board = new short*[m_height];
    m_board = new short*[m_height];

    for (int i = 0; i < m_height; ++i){
        m_logic_board[i] = new short[m_width]{};
        m_board[i] = new short[m_width]{};
    }

    init();
}


Board::~Board(){
    for (int i = 0; i < m_height; ++i){
        delete[] m_logic_board[i];
        delete[] m_board[i];
    }

    delete[] m_logic_board;
    delete[] m_board;
}


void Board::pickEmpty(int x, int y){
    if(m_logic_board[x][y] != 2 && m_board[x][y] != -1){
        m_logic_board[x][y] = 1;

        if(x - 1 >= 0){
            m_logic_board[x - 1][y] = 1;
            if(m_board[x - 1][y] == 0)
                pickEmpty(x - 1, y);
        }

        if(y - 1 >= 0){
            m_logic_board[x][y - 1] = 1;
            if(m_board[x][y - 1] == 0)
                pickEmpty(x, y - 1);
        }

        if(x + 1 < m_height){
            m_logic_board[x + 1][y] = 1;
            if(m_board[x + 1][y] == 0)
                pickEmpty(x + 1, y);
        }

        if(y + 1 < m_width){
            m_logic_board[x][y + 1] = 1;
            if(m_board[x][y + 1] == 0)
                pickEmpty(x, y + 1);
        }
    }
}


int Board::pickPosition(int x, int y, short option){
    int row = x - 1;
    int column = y - 1;

    if(m_board[row][column] == 0 && option == 1)
        pickEmpty(row, column);

    m_logic_board[row][column] = option;

    return m_board[row][column];
}


void Board::pickAll(){
    for (int i = 0; i < m_height; ++i){
        for (int j = 0; j < m_width; ++j){
            m_logic_board[i][j] = 1;
        }
    }
}



void Board::refresh(){
    box(m_win, 0, 0);
    for (int i = 0; i < m_height; ++i){
        for (int j = 0; j < m_width; ++j){
            if(m_logic_board[i][j] == 1)
                mvwaddch(m_win, i + 1, j + 1, m_board[i][j] != 0 ? (m_board[i][j] == -1 ? '#' : m_board[i][j] + 48) : ' ');
            else if(m_logic_board[i][j] == 2)
                mvwaddch(m_win, i + 1, j + 1, '@');
            else
                mvwaddch(m_win, i + 1, j + 1, '-');
        }
    }
}


void Board::loop(){
    int ch, column(1), row(1), lose(1);

    keypad(m_win, TRUE);
    refresh();

    wmove(m_win, 1, 1);

    while(1){
        ch = wgetch(m_win);
        switch(ch){
            case KEY_UP: row > 1 ? wmove(m_win, --row, column) : 1;
                break;
            case KEY_DOWN: row < m_height ? wmove(m_win, ++row, column) : 1;
                break;
            case KEY_RIGHT: column < m_width ? wmove(m_win, row, ++column) : 1;
                break;
            case KEY_LEFT: column > 1 ? wmove(m_win, row, --column) : 1;
        }

        if(ch == 'm'){
            lose = pickPosition(row, column);
            refresh();
        }

        if(ch == 'f'){
            lose = pickPosition(row, column, 2);
            refresh();
        }

        if(lose == -1){
            pickAll();
            refresh();
        }

        wmove(m_win, row, column);

        wrefresh(m_win);
    }
}
