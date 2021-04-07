from PIL import Image
from matplotlib import image
from matplotlib import pyplot
import numpy as np
from scipy.io.wavfile import write


def openImage(filename):
    image = Image.open(filename)
    return image

def imageArray(filename):
    image = image.imread(filename)
    return image

def imageToArray(image):
    data = np.asarray(image)
    print(type(data))
    print(data.shape)
    return data

# Scale image data to range of values acceptible in chosen WAV format (this
# needs to be adjusted to account for image format-- JPEG won't work with this
# math)
def scaleToWAV(vector):
    for i in range(len(vector)):
        vector[i] -= 32768
    return vector

def vectorToWAV(vector,outputFileName):
    sps = 44100
    write(outputFileName, sps, vector)
    # Might want to add a function that plays the output file?

## CONSIDER USING THIS FUNCTION TO SHORTEN VECTORIZERGB FUNCTION BELOW
# def fillVector(vindex,R,G,B,data,i,j,color):
#     if color == 0:
#         R[vindex] = data[i,j,color]
#     elif color == 1:
#         G[vindex] = data[i,j,color]
#     elif color == 2:
#         B[vindex] = data[i,j,color]
#     else:
#         print('ERROR')

def vectorizeRGB(data, columns, direction):
    # Take the numpy array of image data and create three vectors with the rows
    # or columns of data (specified by columns string in args) and chosen
    # direction (specified by increase or decrease string for direction)

    rows = data.shape[0]
    cols = data.shape[1]
    channels = data.shape[2]

    vlength = rows*cols

    R = np.zeros(vlength)
    G = np.zeros(vlength)
    B = np.zeros(vlength)

    vindex = 0

    if columns == True:
        if direction == 'LRcolsUDrows':
            for j in range(cols):
                for i in range(rows):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = data[i,j,color]
                        elif color == 1:
                            G[vindex] = data[i,j,color]
                        elif color == 2:
                            B[vindex] = data[i,j,color]
                        else:
                            print('ERROR')

                    vindex += 1


        elif direction == 'RLcolsUDrows':
            for j in reversed(range(cols)):
                for i in range(rows):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = data[i,j,color]
                        elif color == 1:
                            G[vindex] = data[i,j,color]
                        elif color == 2:
                            B[vindex] = data[i,j,color]
                        else:
                            print('ERROR')

                    vindex += 1

        elif direction == 'LRcolsDUrows':
            for j in range(cols):
                for i in reversed(range(rows)):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = data[i,j,color]
                        elif color == 1:
                            G[vindex] = data[i,j,color]
                        elif color == 2:
                            B[vindex] = data[i,j,color]
                        else:
                            print('ERROR')

                    vindex += 1

        elif direction == 'RLcolsDUrows':
            for j in reversed(range(cols)):
                for i in reversed(range(rows)):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = data[i,j,color]
                        elif color == 1:
                            G[vindex] = data[i,j,color]
                        elif color == 2:
                            B[vindex] = data[i,j,color]
                        else:
                            print('ERROR')

                    vindex += 1



    elif columns == False:
        if direction == 'LRcolsUDrows':
            for i in range(rows):
                for j in range(cols):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = data[i,j,color]
                        elif color == 1:
                            G[vindex] = data[i,j,color]
                        elif color == 2:
                            B[vindex] = data[i,j,color]
                        else:
                            print('ERROR')

                    vindex += 1


        elif direction == 'RLcolsUDrows':
            for i in range(rows):
                for j in reversed(range(cols)):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = data[i,j,color]
                        elif color == 1:
                            G[vindex] = data[i,j,color]
                        elif color == 2:
                            B[vindex] = data[i,j,color]
                        else:
                            print('ERROR')

                    vindex += 1

        elif direction == 'LRcolsDUrows':
            for i in reversed(range(rows)):
                for j in range(cols):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = data[i,j,color]
                        elif color == 1:
                            G[vindex] = data[i,j,color]
                        elif color == 2:
                            B[vindex] = data[i,j,color]
                        else:
                            print('ERROR')

                    vindex += 1

        elif direction == 'RLcolsDUrows':
            for i in reversed(range(rows)):
                for j in reversed(range(cols)):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = data[i,j,color]
                        elif color == 1:
                            G[vindex] = data[i,j,color]
                        elif color == 2:
                            B[vindex] = data[i,j,color]
                        else:
                            print('ERROR')

                    vindex += 1

    return [R, G, B]
