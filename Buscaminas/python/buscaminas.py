from cellgraph import CellGraph, System
from random import randint


class Board(System):
    """-1 para minas"""

    def __init__(self, width, height, mines):
        matrix = [[j for j in range(width)] for i in range(height)]

        super(Board, self).__init__(matrix, {})

        self.mines = mines
        self.flags = 0
        self.found = 0

        # self.putMines(self.mines)

    def putMines(self, n):
        ready = n
        while ready != 0:
            i = randint(0, self.height - 1)
            j = randint(0, self.width - 1)

            if not self.matrix[i][j]:
                self.matrix[i][j] = 1
                ready -= 1


def main():
    board = Board(10, 10, 20)

    game = CellGraph(board, background_color='BLACK', cellwidth=10,
                     cellheight=10, fps=60, separation_between_cells=1)

    game.draw = game.draw_font

    game.run()


if __name__ == '__main__':
    main()
