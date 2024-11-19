''' 
INE5431 Sistemas Multim��dia
Prof. Roberto Willrich

Aula Pr�tica IV: Compress�o de Entropia

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
    mse = 0
    nsymbols = ori.width * ori.height * 3
    for i in range(ori.width):
        for j in range(ori.height):
            ori_r, ori_g, ori_b = ori.getpixel((i, j))
            dec_r, dec_g, dec_b = dec.getpixel((i, j))
            mse += (ori_r - dec_r) ** 2
            mse += (ori_g - dec_g) ** 2
            mse += (ori_b - dec_b) ** 2
    mse /= nsymbols
    return mse

if __name__ == "__main__":
    
    # Indique a matr��cula dos alunos do grupo na lista abaixo
    matriculas = [22100621, 23250860, 22200378]
    
    
    # Gera��o do arquivo Cuif.1, converte o arquivo Cuif.1 em BMP, e calcula o PSNR
    
    ## leitura dos arquivos
    for arquivo in ['lena', 'bandeira']:
       
        img = Image.open(arquivo + '.bmp')

        # Indique a matrícula dos alunos do grupo na lista abaixo
        matriculas = [17200449, 18200443, 20104138]

        # Geração do arquivo Cuif.1, converte o arquivo Cuif.1 em BMP, e calcula o PSNR
        cuif1 = Cuif(img, 1, matriculas)
        cuif1.printHeader()
        cuif1.show()
        cuif1.save(arquivo + '1.cuif')
        cuif1.saveBMP(arquivo + '1.bmp')
        img1 = Image.open(arquivo + '1.bmp')
        print(f'PSNR do CUIF.1 ({arquivo}): {PSNR(img, img1, 8)})\n')

        cuif2 = Cuif(img, 2, matriculas)
        cuif2.printHeader()
        cuif2.show()
        cuif2.save(arquivo + '2.cuif')
        cuif2.saveBMP(arquivo + '2.bmp')
        img2 = Image.open(arquivo + '2.bmp')
        print(f'PSNR do CUIF.2 ({arquivo}): {PSNR(img, img2, 8)})\n')


        cuif3 = Cuif(img, 3, matriculas)
        cuif3.printHeader()
        cuif3.show()
        cuif3.save(arquivo + '3.cuif')
        cuif3.saveBMP(arquivo + '3.bmp')
        img3 = Image.open(arquivo + '3.bmp')
        print(f'PSNR do CUIF.3 ({arquivo}): {PSNR(img, img3, 8)})\n')

        cuif4 = Cuif(img, 4, matriculas)
        cuif4.printHeader()
        cuif4.show()
        cuif4.save(arquivo + '4.cuif')
        cuif4.saveBMP(arquivo + '4.bmp')
        img4 = Image.open(arquivo + '4.bmp')
        print(f'PSNR do CUIF.4 ({arquivo}): {PSNR(img, img4, 8)})\n')

    print("THE END")
