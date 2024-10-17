''' 
INE5431 Sistemas Multimí­dia
Prof. Roberto Willrich

Aula Prática IV: Compressão de Entropia

'''

from PIL import Image
from Cuif import Cuif
import math

def PSNR(original,decodificada,b):
    try:
        mse = MSE(original,decodificada) 
        psnr = 10*math.log10(((2**b-1)**2)/mse)
        return psnr
    except ZeroDivisionError:
        return "Infinito"

def MSE(ori, dec):
    nsymbols = ori.width * ori.height * 3
    for i in range(ori.width):
        for j in range(ori.height):
            ori_r, ori_g, ori_b = ori.getpixel((i, j))
            dec_r, dec_g, dec_b = dec.getpixel((i, j))
    return 0

if __name__ == "__main__":
    
    # Leitura da imagem 
    filepath = 'lena.bmp'

    img = Image.open(filepath)
    
    # Indique a matrí­cula dos alunos do grupo na lista abaixo
    matriculas = [17100532,21220183]
    
    
    # Geração do arquivo Cuif.1, converte o arquivo Cuif.1 em BMP, e calcula o PSNR
    cuif1 = Cuif(img,1,matriculas)
    cuif1.printHeader()
    cuif1.show()
    cuif1.save('lena1.cuif')
    cuif1.saveBMP('lena1.bmp')
    img1 = Image.open('lena1.bmp')
    print("PSNR do CUIF.1",PSNR(img,img1,8)) 
    

    print("THE END")
