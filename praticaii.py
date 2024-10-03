from urllib.request import urlopen
from PIL import Image # package pillow
import math

def criarImagemRGB():
    img = Image.new( "RGB", (512,256))
    raster = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            raster[i,j] = (220,219,97,255)
    (r, g, b) = img.getpixel((0, 0))
    print(r, g, b)
    return img

def criarImagemCinza():
    img = Image.new( "L", (256,256))
    raster = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            raster[i,j] = i
    y = img.getpixel((5, 5))
    print(y)
    return img

def criarImagemBinaria():
    # checkerboard pattern.
    img = Image.new("1", (500,500))
    raster = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if ((int(i/50)+int(j/50)) % 2 == 0):
                raster[i,j] = 0
            else:
                raster[i,j] = 1
    y = img.getpixel((0, 0))
    print(y)
    return img

img = Image.open(urlopen("https://www.inf.ufsc.br/~roberto.willrich/INE5431/RGB.jpg"))
img.show()
criarImagemRGB().show()
criarImagemCinza().show()
criarImagemBinaria().show()
