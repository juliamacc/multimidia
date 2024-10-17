import math
import numpy as np
from PIL import Image

#Implementação de alguns métodos de conversão de espaço de cores


# Converte um array com valores de y,cb,cr em 3 ndarrays (Y,Cb,Cr)
def array2YCbCr(data,width,height):
    Y = np.zeros([height,width], dtype=np.uint8)
    Cb = np.zeros([height,width], dtype=np.uint8)
    Cr = np.zeros([height,width], dtype=np.uint8)
 
    index=0        
    for i in range(width):
        for j in range(height):
            Y[j][i] =  data[index]
            index+=1
    for i in range(width):
        for j in range(height):
            Cb[j][i] =data[index]
            index+=1
    for i in range(width):
        for j in range(height):
            Cr[j][i] =data[index]
            index+=1
    return (Y,Cb,Cr)
    


# Converte Matrizes Y,Cb,Cr em uma imagem RGB
def convertToRGB(Y,Cb,Cr):
    # baseado em https://www.w3.org/Graphics/JPEG/jfif3.pdf
    arrayr = np.trunc(Y.astype(int)+1.402*(Cr.astype(int)-128))
    arrayg = np.trunc(Y.astype(int)-0.34414*(Cb.astype(int)-128)-0.71414*(Cr.astype(int)-128))
    arrayb = np.trunc(Y.astype(int)+1.772*(Cb.astype(int)-128))
    arrayr[arrayr<0]=0
    arrayg[arrayg<0]=0
    arrayb[arrayb<0]=0
    r = Image.fromarray(arrayr.astype(np.uint8))
    g = Image.fromarray(arrayg.astype(np.uint8))
    b = Image.fromarray(arrayb.astype(np.uint8))    
    return Image.merge('RGB', (r, g, b))


# Converte Imagem em três matrizes Y,Cb,Cr
def convertToYCbCr(img):
    # baseado em https://www.w3.org/Graphics/JPEG/jfif3.pdf
    imRGB = Image.Image.split(img) 
    r = np.array(imRGB[0])
    g = np.array(imRGB[1])
    b = np.array(imRGB[2])
    Y = np.trunc(0.299*r+0.587*g+0.114*b).astype(np.uint8)
    Cb = np.trunc(128-0.1687*r-0.3313*g+0.5*b).astype(np.uint8)
    Cr = np.trunc(128+0.5*r-0.4187*g-0.0813*b).astype(np.uint8) 
    Y[Y<0]=0
    Cb[Cb<0]=0
    Cr[Cr<0]=0
    return (Y,Cb,Cr)
