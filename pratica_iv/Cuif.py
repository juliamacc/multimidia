import struct
import numpy as np
from PIL import Image
import ColorSpace
import RLE

''' 
Esta classe suporta os métodos necessários a codificação e decodificação de imagens CUIF 
nas versões definidas na aula Prática IV
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
                               bytes("CUIF",'ascii'), # Assinatura do arquivo
                               version, # versão do CUIF adotada
                               self.number_of_students) # número de alunos
        self.file_stream= self.file_stream + struct.pack('<II',img.size[0],img.size[1]) 
        for i in range(self.number_of_students):
            self.file_stream= self.file_stream + struct.pack('<I',ids[i]) # grava matrículas

        # Na sequência, em file_stream são incluídos os dados da imagem, conforme a versão CUIF 
        # os métodos abaixo retornam a imagem decodificada a partir da codificação fui utilizada                      
        if (version==1):
            self.image = self.generateCUIF1(img)  # Descompactado em formato RGB
        elif (version==2):
            self.image = self.generateCUIF2(img)
        elif (version==3):
             self.image = self.generateCUIF3(img)
        elif (version==4):
             self.image = self.generateCUIF4(img)
        else:
            raise ValueError('Invalid CUIF version')
            
    # Recebe a imagem e a codifica aem CUIF.1. Ou seja, armazenando primeiro os componentes R, depois G e finalmente B
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


    # Recebe a imagem e a codifica em CUIF.3. Ou seja, armazenando primeiro os componentes y, depois cb e finalmente cr
    # Retorna a mesma imagem decodificada a partir dos componentes Y,Cb,Cr.
    def generateCUIF3(self,img):
        (Y,Cb,Cr) = ColorSpace.convertToYCbCr(img)
        self.file_stream +=struct.pack('%sB'%Y.size,*Y.flatten('F'))
        self.file_stream +=struct.pack('%sB'%Y.size,*Cb.flatten('F'))
        self.file_stream +=struct.pack('%sB'%Y.size,*Cr.flatten('F'))
        return ColorSpace.convertToRGB(Y,Cb,Cr)

    # Recebe a imagem e a codifica em CUIF.4. Ou seja, converte a imagem em Y,Cb,Cr e depois compacta com RLE
    # Retorna a imagem decodificada depois de descompactada RLE e convertida para RGB
    def generateCUIF4(self,img):
        (Y,Cb,Cr) = ColorSpace.convertToYCbCr(img)
        compressed = RLE.compress(Y,Cb,Cr)
        self.file_stream +=struct.pack('%sB'%len(compressed),*compressed)
        
        # Etapas para descompactar e codificar a imagem em RGB
        data = RLE.decompress(compressed) 
        width = img.size[0]
        height = img.size[1]
        (Y,Cb,Cr) = ColorSpace.array2YCbCr(data,width,height)
        return ColorSpace.convertToRGB(Y,Cb,Cr)
    

    # Método estático que criar uma imagem CUIF na memória a partir de um arquivo CUIF
    @staticmethod
    def openCUIF(filename):
        bmp = open(filename, 'rb')

        if (bmp.read(4).decode()!='CUIF'):
            raise ValueError('Invalid CUIF file')

        version = struct.unpack('B', bmp.read(1))[0]
        number_of_students = struct.unpack('B', bmp.read(1))[0]
        ids = []
        width =  struct.unpack('I', bmp.read(4))[0]
        height =  struct.unpack('I', bmp.read(4))[0]
        for i in range(number_of_students):
            ids.append(struct.unpack('I', bmp.read(4))[0])
        if (version==1):
            img = Cuif.readCUIF1(bmp,width,height)
        elif (version==2):
            img = Cuif.readCUIF2(bmp,width,height)
        elif(version==3):
            img = Cuif.readCUIF3(bmp,width,height)
        elif(version==4):
            img = Cuif.readCUIF4(bmp,width,height)
        else:
            raise ValueError('Invalid CUIF version')
        return Cuif(img,version,ids)
            

    # Método estático que lê o raster (bitmap) para o formato CUIF.1
    @staticmethod
    def readCUIF1(bmp,width,height):
        r = Image.new( "L", (width,height))
        g = Image.new( "L", (width,height))
        b = Image.new( "L", (width,height))
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


    # Método estático que lê o raster (bitmap) para o formato CUIF.3
    @staticmethod
    def readCUIF3(bmp,width,height):
        Y = np.zeros([height,width], dtype=np.uint8)
        Cb = np.zeros([height,width], dtype=np.uint8)
        Cr = np.zeros([height,width], dtype=np.uint8)
        for i in range(width):
            for j in range(height):
                Y[j][i] =  struct.unpack('B', bmp.read(1))[0]
        for i in range(width):
            for j in range(height):
                Cb[j][i] = struct.unpack('B', bmp.read(1))[0]

        for i in range(width):
            for j in range(height):
                Cr[j][i] = struct.unpack('B', bmp.read(1))[0]

        img=ColorSpace.convertToRGB(Y,Cb,Cr)
        return img
    
    # Método estático que lê o raster (bitmap) para o formato CUIF.4
    @staticmethod
    def readCUIF4(bmp,width,height):
        Y = np.zeros([height,width], dtype=np.uint8)
        Cb = np.zeros([height,width], dtype=np.uint8)
        Cr = np.zeros([height,width], dtype=np.uint8)
        compressed=[]
        while True:
            data = bmp.read(1)
            if (data):
                compressed.append(int.from_bytes(data,byteorder='little'))
            else:
                break
        data = RLE.decompress(compressed) 
        (Y,Cb,Cr) = ColorSpace.array2YCbCr(data,width,height)
        img=ColorSpace.convertToRGB(Y,Cb,Cr)
        return img


    # Método que salva a imagem CUIF em arquivo                
    def save(self,filename):
        f = open(filename, "wb")
        f.write(self.file_stream)
        f.close()
        
    # Método que mostra a imagem CUIF
    def show(self):
        self.image.show()
       
    
    # Método que imprime o cabeçalho CUIF
    def printHeader(self):
        print('Version: %s' % self.version)
        print('Number of Students: %s' % self.number_of_students)
        print('Students: %s' % self.ids)
        print('Width: %s' % self.width)
        print('Height: %s' % self.height)
 
    # Método que salva a imagem CUIF no formato BMP
    def saveBMP(self,filename):
        self.image.save(filename)