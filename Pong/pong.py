from cellgraph import CellGraph, System


class Pong(System):
    """docstring for Pong"""

    def __init__(self, width, height, colors, table=0):
        matrix = [[0] * width for i in range(height)]
        super(Pong, self).__init__(matrix, colors, name='system', clear=False,
                                   add=False)

        self.table = table

        self.drawRackets()

        self.event['keyDown'].append(self.keyDown)

    def drawRackets(self):
        for i in range(5):
            self.matrix[5 + i][0] = 1
            self.matrix[5 + i][-1] = 1

    def keyDown(self, key):
        if key == 'up' and self.matrix[0][self.table * self.width - 1] == 0:
            for i in range(0, self.height - 2):
                self.matrix[i][self.table * self.width - 1] = self.matrix[i + 1][self.table * self.width - 1]
        if key == 'down' and self.matrix[-1][self.table * self.width - 1] == 0:
            for i in range(self.height - 1, 1, -1):
                self.matrix[i][self.table * self.width - 1] = self.matrix[i - 1][self.table * self.width - 1]


def main():
    colors = {0: 'BLACK', 1: 'WHITE'}
    pong = Pong(30, 15, colors)

    game = CellGraph(pong, cellwidth=20, cellheight=20)

    game.run()


if __name__ == '__main__':
    main()
