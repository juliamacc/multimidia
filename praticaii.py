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

def converterParaEscalaDeCinza(caminho_imagem):
    img = Image.open(caminho_imagem)
    img_cinza = Image.new("L", img.size)

    pixels_originais = img.load()
    pixels_cinza = img_cinza.load()
    
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels_originais[i, j] # Obtém o valor RGB do pixel
            cinza = int(0.3 * r + 0.59 * g + 0.11 * b) # Y = 0.3R + 0.59G + 0.11B
            pixels_cinza[i, j] = cinza
    return img_cinza

def criarImagemBinaria():
    # Cria uma nova imagem em tons de cinza
    img = Image.new("L", (500, 500))  # "L" para imagem em tons de cinza
    raster = img.load()
    
    # Preenche a imagem com um padrão de tons de cinza
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            # Definindo um padrão baseado na posição
            valor_cinza = (i + j) % 256  # Valores de 0 a 255
            raster[i, j] = valor_cinza

    # Converte a imagem para binário
    img_binaria = Image.new("1", img.size)  # "1" para imagem binária
    raster_binario = img_binaria.load()

    for i in range(img_binaria.size[0]):
        for j in range(img_binaria.size[1]):
            # Define preto ou branco com base no valor de cinza
            if raster[i, j] >= 127:
                raster_binario[i, j] = 1  # Branco
            else:
                raster_binario[i, j] = 0  # Preto

    # Exibe um pixel para verificação
    y = img_binaria.getpixel((0, 0))
    print(y)
    return img_binaria
'''
# Chamada da função
imagem_binaria = criarImagemBinaria()
imagem_binaria.show()
'''

img = Image.open(urlopen("https://www.inf.ufsc.br/~roberto.willrich/INE5431/RGB.jpg"))
img.show()
criarImagemRGB().show()
criarImagemCinza().show()
criarImagemBinaria().show()
