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
    m_info_win = newwin(7, 17, 0, 0);

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
    if(m_logic_board[x][y] == 0 && m_board[x][y] != -1){
        m_logic_board[x][y] = 1;
        ++m_num_picked;

        if(x - 1 >= 0){
            if(m_board[x - 1][y] == 0)
                pickEmpty(x - 1, y);
            if(m_board[x - 1][y] != -1 && m_logic_board[x - 1][y] != 2)
                m_logic_board[x - 1][y] = 1;
        }

        if(y - 1 >= 0){
            if(m_board[x][y - 1] == 0)
                pickEmpty(x, y - 1);
            if(m_board[x][y - 1] != -1 && m_logic_board[x][y - 1] != 2)
                m_logic_board[x][y - 1] = 1;
        }

        if(x + 1 < m_height){
            if(m_board[x + 1][y] == 0)
                pickEmpty(x + 1, y);
            if(m_board[x + 1][y] != -1 && m_logic_board[x + 1][y] != 2)
                m_logic_board[x + 1][y] = 1;
        }

        if(y + 1 < m_width){
            if(m_board[x][y + 1] == 0)
                pickEmpty(x, y + 1);
            if(m_board[x][y + 1] != -1 && m_logic_board[x][y + 1] != 2)
                m_logic_board[x][y + 1] = 1;
        }
    }
}


int Board::pickPosition(int x, int y, short option){
    int row = x - 1;
    int column = y - 1;

    if(option == 2 && m_logic_board[row][column] != 1){
        m_logic_board[row][column] = m_logic_board[row][column] == 2 ? 0 : 2;

        if(m_logic_board[row][column] == 2)
            ++m_num_flags;
        else
            --m_num_flags;

        return 1;
    }else{
        if(m_board[row][column] == 0 && m_logic_board[row][column] == 0)
            pickEmpty(row, column);
        else{
            if(m_logic_board[row][column] == 0)
                ++m_num_picked;
            m_logic_board[row][column] = (m_logic_board[row][column] != 2) && (m_board[row][column] != -1) ? 1 : 2;
        }
    }

    return m_board[row][column];
}


void Board::pickAll(){
    for (int i = 0; i < m_height; ++i){
        for (int j = 0; j < m_width; ++j){
            m_logic_board[i][j] = 1;
        }
    }
}


void Board::refresh_board(){
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


void Board::refresh_info(){
    box(m_info_win, 0, 0);
    mvwprintw(m_info_win, 1, 1, "Cells: %d", m_width * m_height);
    mvwprintw(m_info_win, 2, 1, "Picked: %d", m_num_picked);
    mvwprintw(m_info_win, 3, 1, "Flags: %d", m_num_flags);
    mvwprintw(m_info_win, 4, 1, "Mines: %d", m_mines);
    mvwprintw(m_info_win, 5, 1, "Percent: %.2f", 100.0 * m_num_picked / (m_width * m_height));
}


int Board::loop(){
    keypad(m_win, TRUE);

    refresh_board();
    refresh_info();

    wrefresh(m_win);
    wrefresh(m_info_win);

    int ch, column(1), row(1), lose(1);

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

        if(ch == 'p'){
            lose = pickPosition(row, column);
            refresh_board();
        }

        if(ch == 'f'){
            lose = pickPosition(row, column, 2);
            refresh_board();
        }

        if(lose == -1){
            pickAll();
            refresh_board();
            ch = wgetch(m_win);
            return -1;
        }

        if(m_width * m_height - m_num_picked == m_mines)
            return 1;

        refresh_info();

        wrefresh(m_win);
        wrefresh(m_info_win);

        wmove(m_win, row, column);
    }
}
