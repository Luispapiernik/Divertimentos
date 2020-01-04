from argparse import ArgumentParser
from shutil import get_terminal_size
from PIL import Image, ImageDraw, ImageFont, ImageStat
from os import path
import random


# function of configuration
def setup(name=''):
    if name:
        font = ImageFont.truetype(name, 20)
    else:
        font = ImageFont.load_default()
    img = Image.new('L', (30, 30), 255)
    text = ImageDraw.Draw(img, 'L')
    name = name.replace('.ttf', '') + 'setup.txt'
    with open(name, 'w') as file:
        for i in range(32, 256):
            size = text.textsize(chr(i))
            if size[0] and size[1]:
                text.rectangle([(0, 0), img.size], 255, 255)
                text.text((5, 5), chr(i), font=font)
                px = ImageStat.Stat(img)._getmean()[0]
                file.write('{} {} {} {}\n'.format(i, chr(i), size, px))
    img.close()


def get_dict(name=''):
    dicc = {}
    name = name.replace('.ttf', '') + 'setup.txt'
    with open(name, 'r') as file:
        for line in file:
            if line:
                split = line.split()
                value = int(split[0])
                key = float(split[-1].replace('\n', ''))
                if dicc.get(key, 0):
                    dicc[key].append(value)
                else:
                    dicc[key] = [value]
    return dicc


def convert(x, a, b, c, d):
    # (a, b) to (0, 1)
    zo = (x - a) / (b - a)
    # (0, 1) to (c, d)
    cd = c + (d - c) * zo
    return cd


def resize(dicc, c, d):
    keys = list(dicc.keys())
    keys.sort()
    a, b = min(keys), max(keys)
    dicc1 = {}
    for key in keys:
        key1 = convert(key, a, b, c, d)
        dicc1[key1] = dicc[key]
    return dicc1


def to_ascii(img, args):
    c, d = img.getextrema()
    if args.c != 1:
        c, d = 0, 255
    if args.invert:
        c, d = d, c

    dicc = get_dict(args.font)
    dicc = resize(dicc, c, d)
    keys = list(dicc.keys())
    keys.sort()
    keys = keys[::args.c]

    string = ''
    if args.margen:
        string += '+' + '-' * img.width + '+\n'
    for y in range(img.height):
        if args.margen:
            string += '|'
        for x in range(img.width):
            mean = img.getpixel((x, y))
            for i in range(1, len(keys)):
                if keys[i - 1] < mean < keys[i]:
                    key = (args.u and dicc[keys[i]][0]) or \
                        random.choice(dicc[keys[i]])
                    string += chr(key) + ' ' * args.space
                    break
                if 0 < mean < keys[0]:
                    key = (args.u and dicc[keys[0]][0]) or \
                        random.choice(dicc[keys[0]])
                    string += chr(key) + ' ' * args.space
                    break
            else:
                string += chr(dicc[keys[-1]][0]) + ' ' * args.space
        string += args.margen * '|' + '\n'
    if args.margen:
        string += '+' + '-' * img.width + '+\n'
    return string[:-1]


def average1(img, a, b, c, d):
    mean = 0
    for x in range(a, b):
        for y in range(c, d):
            mean += img.getpixel((x, y))
    return mean / ((b - a) * (d - c))


def to_ascii_blocks(img, args):
    c, d = img.getextrema()
    if args.c != 1:
        c, d = 0, 255
    if args.invert:
        c, d = d, c

    dicc = get_dict(args.font)
    dicc = resize(dicc, c, d)
    keys = list(dicc.keys())
    keys.sort()
    keys = keys[::args.c]

    b = args.blocks
    index_x = img.height // b[1]
    index_y = img.width // b[0]
    string = ''
    if args.margen:
        string += '+' + '-' * index_y + '+\n'
    for y in range(index_x):
        if args.margen:
            string += '|'
        for x in range(index_y):
            mean = average1(img, x * b[0], (x + 1) * b[0], y * b[1],
                            (y + 1) * b[1])
            for i in range(1, len(keys)):
                if keys[i - 1] < mean < keys[i]:
                    key = (args.u and dicc[keys[i]][0]) or \
                        random.choice(dicc[keys[i]])
                    string += chr(key) + ' ' * args.space
                    break
                if 0 < mean < keys[0]:
                    key = (args.u and dicc[keys[0]][0]) or \
                        random.choice(dicc[keys[0]])
                    string += chr(key) + ' ' * args.space
                    break
            else:
                string += chr(dicc[keys[-1]][0]) + ' ' * args.space
        string += args.margen * '|' + '\n'
    if args.margen:
        string += '+' + '-' * index_y + '+\n'
    return string[:-1]


def main():
    parser = ArgumentParser(description='''This program converts an image to
                            ASCII and saves it in png and txt files''')

    parser.add_argument('-i', '--input', help='name of the input image',
                        type=str, dest='i', metavar='INPUT')
    parser.add_argument('-o', '--output', default='', type=str,
                        help='names of the output images without format')
    parser.add_argument('--format', default='PNG', metavar='PNG/TXT/BOTH',
                        help='''PNG tells the program that the output is an
                        image, TXT indicates the output is in plain text and
                        and BOTH indicates both formats''',
                        choices=['PNG', 'TXT', 'BOTH'])
    parser.add_argument('--size', default=(0, 0), type=int, nargs=2,
                        metavar=('WIDTH', 'HEIGHT'), dest='s',
                        help='''size of the output string''')
    parser.add_argument('-w', '--width', default=0, type=int, dest='w',
                        help='width of the output string', metavar='WIDTH')
    parser.add_argument('--height', default=0, type=int, dest='h',
                        help='height of the output string', metavar='HEIGHT')
    parser.add_argument('-f', '--font', default='', type=str,
                        help='font to be used in the conversion')
    parser.add_argument('--invert', action='store_true',
                        help='''invert output image. Use if your display has
                        a dark background''')
    parser.add_argument('-b', '--blocks', nargs=2, type=int, default=(0, 0),
                        metavar=('WIDTH', 'HEIGHT'),
                        help='''tuple that indicates the size of the grid in
                        which the image will be subdivided. By default
                        the image won't be subdivided''')
    parser.add_argument('-a', '--autoscaled', default=0, type=int, dest='a',
                        help='''if this argument is passed, the output image
                        will be proportional to the input image''',
                        nargs='?', const=-1)
    parser.add_argument('-c', '--contrast', default=1, type=int, dest='c',
                        help='int between 2 and 29 the specifica the contrast',
                        choices=range(1, 30), metavar='1_TO_29')
    parser.add_argument('-u', '--uniform', action='store_true', dest='u',
                        help='''Uses same character for same intensity.
                        The characters will be random by default''')
    parser.add_argument('-m', '--margen', action='store_true',
                        help='print a border around the output image')
    parser.add_argument('-s', action='count', default=0, dest='space',
                        help='separation between the characters')
    parser.add_argument('-v', '--verbose', help='''if this argument is passed
                        the output is shown in terminal''',
                        action='store_true')

    args = parser.parse_args()

    args.output = args.output or args.i[:-4]
    if not path.exists(args.font.replace('.ttf', '') + 'setup.txt'):
        setup(args.font)

    if args.i:
        img = Image.open(args.i)

        gray = img.convert('L')
        text = ImageDraw.Draw(gray, 'L')

        if (args.w or args.s[0]) or (args.h or args.s[1]):
            args.blocks = (img.width // (args.w or args.h or args.s[0] or img.width),
                           img.height // (args.h or args.w or args.s[1] or img.height))
            string = to_ascii_blocks(gray, args)
        elif args.blocks[0] and args.blocks[1]:
            string = to_ascii_blocks(gray, args)
        elif args.a:
            size = img.height > img.width and img.width or img.height
            scale = -1 == args.a and img.height or args.a
            x = scale * 2 <= size and size // (scale * 2) or size // scale
            y = scale * 2 <= size and size // (scale) or size // (scale // 2)
            args.blocks = (x, y)
            string = to_ascii_blocks(gray, args)
        elif args.verbose and (not args.blocks[0] and not args.blocks[1]):
            sh_w, sh_h = get_terminal_size()
            sh_h -= 2 + args.margen * 2
            args.blocks = (img.width // (sh_h * 2),
                           img.height // sh_h)
            string = to_ascii_blocks(gray, args)
        else:
            string = to_ascii(gray, args)

        size = text.multiline_textsize(string, spacing=0)
        img.close()

        img = Image.new('L', size, 255)
        draw = ImageDraw.Draw(img, 'L')

        if args.font:
            font = ImageFont.truetype(args.font)
        else:
            font = ImageFont.load_default()

        draw.text((0, 0), string, font=font, spacing=0)
        if args.format == 'PNG' or args.format == 'BOTH':
            img.save(args.output + 'ascii.png')

        if args.format == 'TXT' or args.format == 'BOTH':
            with open(args.output + 'ascii.txt', 'w') as file:
                file.write(string)

        if args.verbose:
            print(string)

        img.close()
        gray.close()


if __name__ == '__main__':
    main()
