from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

img = Image.open('huella2.png')

imageToMatrice = np.asarray(img)

plt.imshow(imageToMatrice)
plt.show()

imagen_eg = np.zeros((imageToMatrice.shape[0],imageToMatrice.shape[1]))

for i in range(imagen_eg.shape[0]):
    for j in range(imagen_eg.shape[1]):
        imagen_eg[i, j] = np.mean(imageToMatrice[i, j])/255


plt.imshow(imagen_eg, cmap='gray')
plt.show()

#BINARIZADO
imagenBN = np.zeros((imagen_eg.shape[0], imagen_eg.shape[1]))
for i in range(imagen_eg.shape[0]):
    for j in range(imagen_eg.shape[1]):
        #print(np.mean(imagen_eg[i][j]))
        if np.mean(imagen_eg[i][j]) < 0.72:
          imagenBN[i][j] = 1
        else:
          imagenBN[i][j] = 0

plt.imshow(imagenBN)
plt.show()

#Si se desea visualizar la imagen sin la tonalidad violeta-amarilla hay que indicarlo
plt.imshow(imagenBN, cmap='gray')
plt.show()

def intarray(binstring):
    '''Change a 2D matrix of 01 chars into a list of lists of ints'''
    return [[1 if ch == '1' else 0 for ch in line]
            for line in binstring.strip().split()]

def chararray(intmatrix):
    '''Change a 2d list of lists of 1/0 ints into lines of 1/0 chars'''
    return '\n'.join(''.join(str(p) for p in row) for row in intmatrix)

def toTxt(intmatrix):
    '''Change a 2d list of lists of 1/0 ints into lines of '#' and '.' chars'''
    return '\n'.join(''.join(('#' if p else '.') for p in row) for row in intmatrix)

def neighbours(x, y, image):
    '''Return 8-neighbours of point p1 of picture, in order'''
    i = image
    x1, y1, x_1, y_1 = x+1, y-1, x-1, y+1
    #print ((x,y))
    return [i[y1][x],  i[y1][x1],   i[y][x1],  i[y_1][x1],  # P2,P3,P4,P5
            i[y_1][x], i[y_1][x_1], i[y][x_1], i[y1][x_1]]  # P6,P7,P8,P9

def transitions(neighbours):
    n = neighbours + neighbours[0:1]    # P2, ... P9, P2
    return sum((n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]))

def zhangSuen(image):
    changing1 = changing2 = [(-1, -1)]
    while changing1 or changing2:
        # Step 1
        changing1 = []
        for y in range(1, len(image) - 1):
            for x in range(1, len(image[0]) - 1):
                P2,P3,P4,P5,P6,P7,P8,P9 = n = neighbours(x, y, image)
                if (image[y][x] == 1 and    # (Condition 0)
                    P4 * P6 * P8 == 0 and   # Condition 4
                    P2 * P4 * P6 == 0 and   # Condition 3
                    transitions(n) == 1 and # Condition 2
                    2 <= sum(n) <= 6):      # Condition 1
                    changing1.append((x,y))
        for x, y in changing1: image[y][x] = 0
        # Step 2
        changing2 = []
        for y in range(1, len(image) - 1):
            for x in range(1, len(image[0]) - 1):
                P2,P3,P4,P5,P6,P7,P8,P9 = n = neighbours(x, y, image)
                if (image[y][x] == 1 and    # (Condition 0)
                    P2 * P6 * P8 == 0 and   # Condition 4
                    P2 * P4 * P8 == 0 and   # Condition 3
                    transitions(n) == 1 and # Condition 2
                    2 <= sum(n) <= 6):      # Condition 1
                    changing2.append((x,y))
        for x, y in changing2: image[y][x] = 0
        #print changing1
        #print changing2
    return image

imagen_delgada = zhangSuen(imagenBN)

#Si se desea visualizar la imagen sin la tonalidad violeta-amarilla hay que indicarlo
plt.imshow(imagen_delgada, cmap='gray')
plt.show()

def terminacion(imagen_copia):
  for x in range(5,imagen_copia.shape[0]-5):
    for y in range(5,imagen_copia.shape[1]-5):
      if imagen_copia[x, y] == 1:
        if es_vecino(x, y, imagen_copia)==1:
          pintar_minutas(x, y, imagen_copia)
  return imagen_copia

def es_vecino(x, y, imagen_copia):
  vecinos = [imagen_copia[x-1, y-1],
             imagen_copia[x-1, y],
             imagen_copia[x-1, y+1],
             imagen_copia[x, y-1],
             imagen_copia[x, y+1],
             imagen_copia[x+1, y-1],
             imagen_copia[x+1, y],
             imagen_copia[x+1, y+1] ]
  return sum(vecinos)

def pintar_minutas(x, y, imagen_copia):
  for i in range(x - 5, x + 6):
          # Pinta el borde superior e inferior
          imagen_copia[i, y - 5] = 1
          imagen_copia[i, y + 5] = 1
  for j in range(y - 5, y + 6):
          imagen_copia[x - 5, j] = 1
          imagen_copia[x + 5, j] = 1

imagen_copia = np.copy(imagen_delgada)
imagen_con_minutas = terminacion(imagen_copia)

plt.imshow(imagen_con_minutas, cmap='gray')
plt.show()