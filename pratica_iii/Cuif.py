import struct
import numpy as np
from PIL import Image
# import ColorSpace
# import RLE

''' 
Esta classe suporta os métodos necessários a codificação e decodificação de imagens CUIF.1 
nas versões definidas na aula Prática III
'''

class Cuif:
    
    # Construtor que criar uma imagem CUIF na memória. Os parâmetros são a imagem, a versão CUIF e ids (matrículas dos alunos)
    def __init__(self,img,version,ids):
        
        # Implementação suporta apenas imagens RGB não compactadas como entrada, se for diferente, faz a conversão
        if (img.mode!='RGB'):
            print('Image is not RGB, and will be converted to RGB')
            img=img.convert('RGB')
            
        # Atributos são os elementos do cabeçalho CUIF
        self.version = version
        self.number_of_students = len(ids)
        self.ids = ids
        self.width = img.size[0]
        self.height = img.size[1]

        # file_stream contém o stream de bytes que será salvo em arquivo no formato CUIF
        # Esta parte monta o cabeçalho do arquivo CUIF
        self.file_stream= struct.pack('4sBB', 
                               bytes('CUIF','ascii'), # Assinatura do arquivo
                               version, # versão do CUIF adotada
                               self.number_of_students) # número de alunos
        self.file_stream= self.file_stream + struct.pack('II',img.size[0],img.size[1]) 
        for i in range(self.number_of_students):
            self.file_stream= self.file_stream + struct.pack('I',ids[i]) # grava matrículas

        # Na sequência, em file_stream são incluídos os dados da imagem, conforme a versão CUIF 
        # os métodos abaixo retornam a imagem decodificada a partir da codificação fui utilizada                      
        if (version==1):
            self.image = self.generateCUIF1(img)  # Descompactado em formato RGB
        elif (version==2):
            self.image = self.generateCUIF2(img)
        else:
            raise ValueError('Invalid CUIF version')
            
    # Recebe a imagem e a codifica em CUIF.1. Ou seja, armazenando primeiro os componentes R, depois G e finalmente B
    # Retorna a mesma imagem, pois não há alteração de dados.
    def generateCUIF1(self,img):
        imRGB = Image.Image.split(img) 
        r = np.array(imRGB[0])
        g = np.array(imRGB[1])
        b = np.array(imRGB[2])
        self.file_stream +=struct.pack('%sB'%r.size,*r.flatten('F'))
        self.file_stream +=struct.pack('%sB'%g.size,*g.flatten('F'))
        self.file_stream +=struct.pack('%sB'%b.size,*b.flatten('F'))
        return img

     # Método que transforma raster CUIF.2 em Imagem
    def imgCUIF2(self,arrayr,gb):
      arrayg = gb&0xF0
      arrayb = (gb<<4)&0xFF
      r = Image.fromarray(arrayr.astype(np.uint8))
      g = Image.fromarray(arrayg.astype(np.uint8))
      b = Image.fromarray(arrayb.astype(np.uint8))  
      return Image.merge('RGB', (r, g, b))

   # Recebe a imagem e a codifica em CUIF.1. Ou seja, armazenando primeiro os componentes R, depois G e finalmente B
    # Retorna a mesma imagem, pois não há alteração de dados.
    def generateCUIF2(self,img):
        imRGB = Image.Image.split(img) 
        r = np.array(imRGB[0])
        g = np.array(imRGB[1])
        b = np.array(imRGB[2])
        gb = (b>>4) + (g&0xF0)
        self.file_stream +=struct.pack('%sB'%r.size,*r.flatten('F'))
        self.file_stream +=struct.pack('%sB'%gb.size,*gb.flatten('F'))
        return self.imgCUIF2(r,gb)

    # Método estático que criar uma imagem CUIF na memória a partir de um arquivo CUIF
    @staticmethod
    def openCUIF(filename):
        file = open(filename, 'rb')

        if (file.read(4).decode()!='CUIF'):
            raise ValueError('Invalid CUIF file')

        version = struct.unpack('B', file.read(1))[0]
        number_of_students = struct.unpack('B', file.read(1))[0]
        ids = []
        width =  struct.unpack('I', file.read(4))[0]
        height =  struct.unpack('I', file.read(4))[0]
        for i in range(number_of_students):
            ids.append(struct.unpack('I', file.read(4))[0])
        if (version==1):
            img = Cuif.readCUIF1(file,width,height)
        elif (version==2):
            img = Cuif.readCUIF2(file,width,height)
        else:
            raise ValueError('Invalid CUIF version')
        return Cuif(img,version,ids)
            

    # Método estático que lê o raster (bitmap) para o formato CUIF.1
    @staticmethod
    def readCUIF1(bmp,width,height):
        r = Image.new( "L", (width,height))
        g = Image.new( "L", (width,height))
        b = Image.new("L", (width,height))
        rasterR = r.load()
        rasterG = g.load()
        rasterB = b.load()
        for i in range(width):
            for j in range(height):
                rasterR[i,j] =  struct.unpack('B', bmp.read(1))[0]
        for i in range(width):
            for j in range(height):
                rasterG[i,j] = struct.unpack('B', bmp.read(1))[0]

        for i in range(width):
            for j in range(height):
                rasterB[i,j] = struct.unpack('B', bmp.read(1))[0]

        return Image.merge('RGB', (r, g, b))

    # Método estático que lê o raster (bitmap) para o formato CUIF.2
    @staticmethod
    def readCUIF2(file,width,height):
        r = Image.new( "L", (width,height))
        g = Image.new( "L", (width,height))
        b = Image.new( "L", (width,height))
        rasterR = r.load()
        rasterG = g.load()
        rasterB = b.load()
        for i in range(width):
            for j in range(height):
                rasterR[i,j] =  struct.unpack('B', file.read(1))[0]
        for i in range(width):
            for j in range(height):
                gbval = struct.unpack('B', file.read(1))[0]
                rasterG[i,j] = gbval&0xF0
                rasterB[i,j] = (gbval<<4)&0xFF
        return Image.merge('RGB', (r, g, b))

    # Método que salva a imagem CUIF em arquivo                
    def save(self,filename):
        f = open(filename, 'wb')
        f.write(self.file_stream)
        f.close()
        
    # Método que mostra a imagem CUIF
    def show(self):
        self.image.show()
    
    # Método que imprime o cabeçalho CUIF
    def printHeader(self):
        print('Version %s' % self.version)
        print('Number of Students %s' % self.number_of_students)
        print('Students %s' % self.ids)
        print('Width %s' % self.width)
        print('Height %s' % self.height)
 
    # Método que salva a imagem CUIF no formato BMP
    def saveBMP(self,filename):
        self.image.save(filename)