from PIL import Image
from Cuif import Cuif
import math

def PSNR(original,decodificada,b): #### Está correto de acordo com a fórmula, não houve alteração.
    try:
        mse = MSE(original,decodificada) 
        psnr = 10*math.log10(((2**b-1)**2)/mse)
        return psnr
    except ZeroDivisionError:
        return "Infinito"

def MSE(ori, dec): #Completo - Questão 3 do relatorio.
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
                    #Completo - Questão 3 do relatorio.

if __name__ == "__main__":
    # filepath = '/content/drive/MyDrive/PraticaIII/lena.bmp'
    filepath = 'peixe.bmp'
    img = Image.open(filepath)
    matriculas = [22100621, 23250860, 22200378]
    
    # instancia objeto Cuif, convertendo imagem em CUIF.1
    #cuif = Cuif(img,1,matriculas)

    # instancia objeto Cuif, convertendo imagem em CUIF.2
    cuif = Cuif(img,2,matriculas)
    
    # imprime cabeçalho Cuif
    cuif.printHeader()
    
    # mostra imagem Cuif
    cuif.show()
    
    #gera o arquivo Cuif.1
    #cuif.save('peixe1.cuif')
    #filepathdec = 'peixe1.cuif'
    cuif.save('peixe2.cuif')
    filepathdec = 'peixe2.cuif'

    #Abre um arquivo Cuif e gera o objeto Cuif.1
    #cuif1 = Cuif.openCUIF('peixe1.cuif')

    #Abre um arquivo Cuif e gera o objeto Cuif.2
    cuif2 = Cuif.openCUIF('peixe2.cuif')
    
    # Converte arquivo Cuif.1 em BMP e mostra
    #cuif1.saveBMP("peixe1.bmp")
    #cuif1.show()
    #filepathdec = 'peixe1.bmp'

    # Converte arquivo Cuif.2 em BMP e mostra
    cuif2.saveBMP("peixe2.bmp")
    cuif2.show()
    filepathdec = 'peixe2.bmp'
    
    img1 = Image.open(filepathdec)

    psnr = PSNR(img, img1, 8)
    print(f'Cálculo do PSNR: {psnr}')
