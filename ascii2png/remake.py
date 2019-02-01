from __future__ import division

from PIL import ImageFont, ImageDraw, ImageStat, Image
from argparse import ArgumentParser
from os.path import exists
from random import choice


def configFont(name=''):
    """configura el valor de intensidad para cada letra"""
    if name:
        font = ImageFont.truetype(name, 20)
    else:
        font = ImageFont.load_default()

    img = Image.new('L', font.getsize(' '), 255)
    text = ImageDraw.Draw(img, 'L')
    name = name.replace('.ttf', '') + 'setup.txt'
    with open(name, 'w') as file:
        for i in range(0, 256):
            size = text.textsize(chr(i))
            if size[0] and size[1]:
                text.rectangle([(0, 0), img.size], 255, 255)
                text.text((0, 0), chr(i), font=font)
                px = ImageStat.Stat(img)._getmean()[0]
                px = int(round(px))
                file.write('{} {} {}\n'.format(i, chr(i), px))
    img.close()


def grayImage(filename):
    img = Image.open(filename)
    gray = img.convert('L')

    img.close()

    return gray


def loadSetup(font_name):
    name = font_name.replace('.ttf', '') + 'setup.txt'
    if not exists(name):
        configFont(font_name)

    dictr = {}
    with open(name, 'r') as file:
        for line in file:
            words = line.replace('\n', '').split()
            if not len(words) == 3:
                continue
            key = int(words[2])
            if dictr.get(key, 0):
                dictr[key].append(words[1])
            else:
                dictr[key] = [words[1]]

    return dictr


def bijection(y, a, b, c, d):
    """y in (c, d) to (a, b)"""
    # (c, d) to (0, 1)
    zero_one = (y - c) / (d - c)
    # (0, 1) to (a, b)
    a_b = zero_one * (b - a) + a
    return a_b


def changeRange(dictr, minimum=0, maximum=255):
    keys = dictr.keys()
    new_dictr = {}

    c, d = min(keys), max(keys)
    for key in keys:
        new_dictr[int(bijection(key, minimum, maximum, c, d))] = dictr[key]

    return new_dictr


def toAscii(gray_image, dictr, uniform=False):
    string = ''

    keys = dictr.keys()
    keys.sort()

    for i in range(gray_image.height):
        for j in range(gray_image.width):

            index = None
            pixel_value = gray_image.getpixel((j, i))
            if 0 <= pixel_value <= keys[0]:
                index = 0

            for k in range(1, len(keys)):
                if keys[k - 1] < pixel_value <= keys[k]:
                    index = k
                    break

            if isinstance(index, int):
                if uniform:
                    string_pixel = dictr[keys[index]][0]
                else:
                    string_pixel = choice(dictr[keys[index]])
                string += string_pixel

        string += '\n'

    return string


def main():
    parser = ArgumentParser(description='''This program converts an image to
                            ASCII and saves it in png and txt files''')
    parser.add_argument('-i', '--input', help='name of the input image',
                        type=str, metavar='INPUT')
    parser.add_argument('-o', '--output', default='ascii', type=str,
                        help='names of the output file without format')
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
    parser.add_argument('-a', '--autoscaled', default=0, type=int, dest='a',
                        help='''if this argument is passed, the output image
                        will be proportional to the input image''',
                        nargs='?', const=-1)
    parser.add_argument('-s', action='count', default=0, dest='space',
                        help='separation between the characters')
    parser.add_argument('-f', '--font', default='', type=str,
                        help='font to be used in the conversion')
    parser.add_argument('--invert', action='store_true',
                        help='''invert output image. Use if your display has
                        a dark background''')
    parser.add_argument('-u', '--uniform', action='store_true',
                        help='''Uses same character for same intensity.
                        The characters will be random by default''')

    args = parser.parse_args()

    gray_image = grayImage(args.input)
    gray_image = gray_image.resize((int(gray_image.width / 10),
                                    int(gray_image.height / 10)))
    dictr = loadSetup(args.font)
    new_dictr = changeRange(dictr)

    string = toAscii(gray_image, new_dictr, uniform=args.uniform)
    print(string)
    gray_image.close()


if __name__ == '__main__':
    main()
