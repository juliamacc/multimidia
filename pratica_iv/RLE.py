import numpy as np

# Método que compacta matrizes Y, Cb e CR usando a codificação RLE apresentada na aula prática
def compress(Y,Cb,Cr):
    array = np.concatenate((Y.flatten('F'),Cb.flatten('F'),Cr.flatten('F')))
    data = np.right_shift(array,1)
    output =  []
    index = 0 
    while (index<len(data)-1):
        repetitions = 1
        i=index+1
        while (i<len(data)):
            if (data[index]==data[i]):
                repetitions=repetitions+1
                i+=1
            else:
                break
        if (repetitions==1):
            output.append(data[index])
            index +=1
        else:
            # com repetição
            if (repetitions<128):
                output.append(repetitions  | (1<<7))
                output.append(data[index])
            else:
                # repetição acima da capacidade de 7bit faz divisão
                output.append(255) # bit mais significativo setado e 127 repetições
                output.append(data[index])
                tmprepetitions = repetitions-127
                while (tmprepetitions!=0):
                    if (tmprepetitions<=127):
                        output.append(tmprepetitions | (1<<7))
                        output.append( data[index])
                        tmprepetitions=0
                    else:
                        output.append( 255)
                        output.append( data[index])
                        tmprepetitions -=127
            index +=repetitions
    if (index<len(data)):
        output.append(data[index])

    return output

# Método que descompacta o dado compactado com a codificação RLE apresentada na aula prática
def decompress(data):
    output = []
    i=0
    while (i<len(data)):
        if (data[i]&128==0):
            output.append(data[i]<<1)
        else:
            # Flag de repetição setado
            repetitions = data[i]&127
            for j in range(repetitions):
                output.append(data[i+1]<<1)
            i+=1
        i+=1
        
    return output
