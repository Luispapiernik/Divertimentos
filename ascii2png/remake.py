from PIL import ImageFont, ImageDraw, ImageStat, Image


def configFont(name=''):
    """configura el valor de intensidad para cada letra"""
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


def loadGray(filename):
    """Carga la matrix de una imagen en escala de grises"""
    img = Image.open(filename)
    gray = img.convert('L')

    matrix = [[0] * img.width for i in range(img.height)]

    for i in range(img.height):
        for j in range(img.width):
            matrix[i][j] = gray.getpixel(i, j)

    gray.close()
    img.close()

    return matrix


def main():
    configFont()


if __name__ == '__main__':
    main()
