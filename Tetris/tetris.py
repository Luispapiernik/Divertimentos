from cellgraph import System


class Tetris(System):
    """docstring for Tetris"""

    def __init__(self, width, height):
        super(Tetris, self).__init__()

    def fillMatrix(self):
        matrix = [[0] * self.width for i in range(self.height)]

        for i in range(0, self.height):
            for j in range(0, self.width):
                pass

        return matrix
