# Participantes do Grupo 9: Guilherme Augusto, Julia Macedo e Victor Henrique Labes

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

################ Item I: ####################
def criarImagemMetadeRGB(img): 
    img_rgb = img  
    original_raster = img_rgb.load()

    # cria a nova imagem com as dimensões reduzidas
    nova_img = Image.new("RGB", (img_rgb.size[0] // 2, img_rgb.size[1] // 2))
    nova_raster = nova_img.load()

    
    for i in range(img_rgb.size[0] // 2): #laços para percorrer com as novas dimensões.
        for j in range(img_rgb.size[1] // 2):
            r_total = 0
            g_total = 0
            b_total = 0
            for x in range(2):
                for y in range(2):
                    r, g, b = original_raster[i * 2 + x, j * 2 + y]
                    r_total += r
                    g_total += g
                    b_total += b
            
            # calculando a média dos 4 pixels
            r_medio = r_total // 4
            g_medio = g_total // 4
            b_medio = b_total // 4

            # atribuindo o pixel resultante à nova imagem
            nova_raster[i, j] = (r_medio, g_medio, b_medio)

    return nova_img
################ Item I: ####################

def criarImagemCinza():
    img = Image.new( "L", (256,256))
    raster = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            raster[i,j] = i
    y = img.getpixel((5, 5))
    print(y)
    return img

################ Item II: ####################
def converterParaEscalaDeCinza(img):
    img_rgb = img
    img_cinza = Image.new("L", img_rgb.size)

    raster_rgb = img_rgb.load() # carrega os pixels da imagem original
    raster_cinza = img_cinza.load() # carrega os pixels da imagem cinza

    for u in range(img_rgb.size[0]):
        for v in range(img_rgb.size[1]): 
            r, g, b = raster_rgb[u, v] # obtém o valor de cada pixel
            raster_cinza[u, v] = int(0.3*r + 0.59*g + 0.11*b) # atribui cada pixel da imagem cinza, através do calculo da luminância
    return img_cinza
################ Item II: ####################

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

################ Item III: ####################
def criarRGBBinaria(img):
    img_rgb = img
    raster_rgb = img_rgb.load()  # carrega os pixels da imagem RGB
    img_binaria = Image.new("1", img_rgb.size)  # cria uma nova imagem binária
    raster_binaria = img_binaria.load()  # carrega os pixels da imagem binária

    
    for i in range(img_rgb.size[0]): # laços que percorrem em todos os pixels da imagem RGB
        for j in range(img_rgb.size[1]):
            r, g, b = raster_rgb[i, j]  # obtém o valor RGB do pixel
            tom_cinza = int(0.3 * r + 0.59 * g + 0.11 * b)  # cálculo do tom de cinza

            if tom_cinza >= 127:
                raster_binaria[i, j] = 1  # branco
            else:
                raster_binaria[i, j] = 0  # preto

    return img_binaria
################ Item III: ####################

################ Item IV: ####################
def separarCanaisRGB(img):
   
    img_r = Image.new("RGB", img.size)  # imagens para os canais R, G e B
    img_g = Image.new("RGB", img.size)
    img_b = Image.new("RGB", img.size)

    raster_rgb = img.load()  # carrega os pixels da imagem original
    raster_r = img_r.load()  # carrega os pixels da imagem R
    raster_g = img_g.load()  # carrega os pixels da imagem G
    raster_b = img_b.load()  # carrega os pixels da imagem B

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = raster_rgb[i, j]  # Obtém os valores RGB do pixel

            raster_r[i, j] = (r, 0, 0) #para a imagem do canal R
            raster_g[i, j] = (0, g, 0) #para a imagem do canal G
            raster_b[i, j] = (0, 0, b) #para a imagem do canal B

    return img_r, img_g, img_b
################ Item IV: ####################

img = Image.open(urlopen("https://www.inf.ufsc.br/~roberto.willrich/INE5431/RGB.jpg"))
#img.show()
#criarImagemRGB().show()
#criarImagemCinza().show()
#criarImagemBinaria().show()
#############################################
imagem_reduzida = criarImagemMetadeRGB(img) # item I
imagem_reduzida.show() # item I
imagem_cinza = converterParaEscalaDeCinza(img) # item II
imagem_cinza.show() # item II
imagem_binaria = criarRGBBinaria(img) # item III
imagem_binaria.show() # item III
img_r, img_g, img_b = separarCanaisRGB(img) # item IV 
img_r.show() # item IV 
img_g.show() # item IV
img_b.show() # item IV
#############################################
