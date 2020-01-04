from argparse import ArgumentParser, RawDescriptionHelpFormatter
from cellgraph import CellGraph, System, COLORS
from collections import deque
from random import randint
from copy import deepcopy


DIRECTIONS = [(1, 0), (-1, 0), (0, -1), (0, 1)]


class Snake(System):
    """1: snake, 2: food, 3: wall"""

    def __init__(self, width, height, colors, food=1, filename=None, add=True):
        if filename:
            matrix = self.getMatrixFromFile(filename)
        else:
            matrix = [[0] * width for i in range(height)]

        self.baseMatrix = matrix

        super(Snake, self).__init__(matrix, colors=colors, name='Snake',
                                    clear=False, export=False, add=add)

        self.event['keyDown'].append(self.keyDown)
        self.gameover = False
        self.pause = False

        self.size = self.height, self.width
        self.dir = (0, 0)
        self.pos = deque([(randint(0, self.height - 1),
                           randint(0, self.width - 1))])
        self.food = deque([])

        for i in range(food):
            self.getFood()

    def getCaption(self):
        if self.gameover:
            return 'Game Over ' + str(len(self.pos))
        return 'Snake ' + str(len(self.pos))

    def getColor(self, i, j):
        key = self.matrix[i][j] or self.baseMatrix[i][j]
        return self.colors.get(key, 'BLACK')

    def add(self, pos, _):
        """agrega celulas al tablero"""
        super(Snake, self).add(pos, _, self.baseMatrix, 3, 6)

    def collide(self, pos=None, wall=False, direction=None):
        direction = direction or self.dir
        posy = (self.pos[0][0] + direction[0]) % self.size[0]
        posx = (self.pos[0][1] + direction[1]) % self.size[1]

        if wall:
            return self.baseMatrix[posy][posx] == 3

        for i, j in pos:
            if i == posy and j == posx:
                return True

        return False

    def keyDown(self, key):
        if key == 'r':
            self.dir = (0, 0)
            self.pos = deque([(randint(0, self.height - 1),
                               randint(0, self.width - 1))])
        if key == 'p' or key == 'space':
            self.pause = not self.pause
        if not self.pause and not self.gameover:
            if (key == 'up' and not
                    self.collide([self.pos[int(len(self.pos) > 1)]],
                                 direction=DIRECTIONS[1])):
                self.dir = DIRECTIONS[1]
            elif (key == 'down' and not
                    self.collide([self.pos[int(len(self.pos) > 1)]],
                                 direction=DIRECTIONS[0])):
                self.dir = DIRECTIONS[0]
            elif (key == 'right' and not
                    self.collide([self.pos[int(len(self.pos) > 1)]],
                                 direction=DIRECTIONS[3])):
                self.dir = DIRECTIONS[3]
            elif (key == 'left' and not
                    self.collide([self.pos[int(len(self.pos) > 1)]],
                                 direction=DIRECTIONS[2])):
                self.dir = DIRECTIONS[2]
            else:  # solo por simetria
                pass

    def getFood(self):
        posy = randint(0, self.height - 1)
        posx = randint(0, self.width - 1)

        while self.matrix[posy][posx] != 0:
            posy = randint(0, self.height - 1)
            posx = randint(0, self.width - 1)

        self.food.append((posy, posx))

    def move(self, grow=False):
        posy = (self.pos[0][0] + self.dir[0]) % self.size[0]
        posx = (self.pos[0][1] + self.dir[1]) % self.size[1]

        self.pos.appendleft((posy, posx))

        if grow:
            self.food.remove((posy, posx))
            self.getFood()
        else:
            self.pos.pop()

    def update(self):
        self.gameover = self.collide(wall=True) or (
            self.collide(self.pos) and len(self.pos) != 1)

        if not self.pause and not self.gameover:
            self.move(self.collide(self.food))
            self.matrix = deepcopy(self.baseMatrix)

            for i, j in self.food:
                self.matrix[i][j] = 2

            for i, j in self.pos:
                self.matrix[i][j] = 1


def main():
    epilog = ''' Clasico juego Snake.

El programa permite 2 modos de simulacion, el
manual en el que se pasa al siguiente frame de simulacion mediante la pulsacion
de la tecla SPACE y otro en el que se fija los frames por segundo, se puede
pausar con la tecla p ademas se puede tomar una captura de pantalla con la
tecla s, si se presiona la tecla c se limpia el tablero y si se presiona la
tecla e la configuracion del tablero se guarda en un archivo de texto. Se
permite tambien agregar celulas vivas presionando con el mouse a la celula. El
programa tambien permite cargar configuraciones para el tablero desde un
archivo de texto.


Los colores disponibles son:
    - WHITE
    - BLACK
    - CYAN
    - GREEN
    - BLUE
    - YELLOW
    - ORANGE
    - MAGENTA
    - SILVER
    - PURPLE
    - TEAL
    - GRAY
    - RED
    - BROWN
    - GOLDEN'''

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            epilog=epilog)

    parser.add_argument('--filename', default=None,
                        help='''Archivo con la configuracion
                        inicial del tablero''')
    parser.add_argument('-o', '--output', default='gameoflife',
                        dest='name', help='''nombre con el que se guarda la
                        captura de pantalla(si se hace)''')
    parser.add_argument('-w', '--width', type=int, default=30,
                        help='numero de celdas horizontales')
    parser.add_argument('--height', type=int, default=30,
                        help='numero de celdas verticales')
    parser.add_argument('-mw', '--margin-width', type=int, default=0,
                        help='largo de la margen horizontal')
    parser.add_argument('-mh', '--margin-height', type=int, default=0,
                        help='largo de la margen vertical')
    parser.add_argument('-cw', '--cell-width', type=int, default=5,
                        help='ancho horizontal de las celdas(celulas)')
    parser.add_argument('-ch', '--cell-height', type=int, default=5,
                        help='ancho vertical de las celdas(celulas)')
    parser.add_argument('-sbc', '--separation-between-cells', type=int,
                        default=1, dest='sbc',
                        help='separacion entre las celdas(celulas)')
    parser.add_argument('-f', '--food', type=int, default=1,
                        help='cantidad de comida en el tablero')
    parser.add_argument('-bc', '--background-color', type=lambda x: x.upper(),
                        metavar='COLOR', default='BLACK',
                        choices=COLORS.keys(),
                        help='''color de fondo, es el mismo que el de la
                        margen y la separacion entre celdas''')
    parser.add_argument('-cf', '--color-food', type=lambda x: x.upper(),
                        metavar='COLOR', default='GREEN',
                        choices=COLORS.keys(),
                        help='color de celulas vivas')
    parser.add_argument('-cs', '--color-snake', type=lambda x: x.upper(),
                        metavar='COLOR', default='RED',
                        choices=COLORS.keys(),
                        help='color celulas muertas')
    parser.add_argument('-cc', '--color-cell', type=lambda x: x.upper(),
                        metavar='COLOR', default='WHITE',
                        choices=COLORS.keys(),
                        help='color de las celdas vacias')
    parser.add_argument('-v', '--velocity', type=int,
                        default=10, help='''velocidad de la culebrita''')
    parser.add_argument('-a', '--acceleration', type=float,
                        default=0, help='''aceleracion de la culebrita''')

    args = parser.parse_args()

    colors = {0: args.color_cell, 1: args.color_snake, 2: args.color_food}

    snake = Snake(args.width, args.height, colors, food=args.food,
                  filename=args.filename)

    game = CellGraph(snake, cellwidth=10, cellheight=10, fps=args.velocity,
                     separation_between_cells=1,
                     background_color=args.background_color)

    game.run(acceleration=args.acceleration)


if __name__ == '__main__':
    main()
