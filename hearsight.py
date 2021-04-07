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

# Scale image data to range of values acceptible in chosen WAV format
def scaleToWAV(vector):
    for i in range(len(vector)):
        vector[i] -= 32768
    return vector

def vectorToWAV(vector,outputFileName):
    sps = 44100
    write(outputFileName, sps, vector)
    # Might want to add a function that plays the output file?

def vectorizeRGB(data, columns, direction):
    # Take the numpy array of image data and create three vectors with the rows
    # or columns of data (specified by columns string in args) and chosen
    # direction (specified by increase or decrease string for direction)

    rows = data.shape[0]
    cols = data.shape[1]
    channels = data.shape[2]

    R = np.empty(0)
    G = np.empty(0)
    B = np.empty(0)

    if columns == True:
        if direction == 'LRcolsUDrows':
            for color in range(channels):
                for j in range(cols):
                    for i in range(rows):
                        if color == 0:
                            R = np.append(R, data[i,j,color])
                        elif color == 1:
                            G = np.append(G, data[i,j,color])
                        elif color == 2:
                            B = np.append(B, data[i,j,color])
                        else:
                            print('ERROR')

        elif direction == 'RLcolsUDrows':
            for color in range(channels):
                for j in reversed(range(cols)):
                    for i in range(rows):
                        if color == 0:
                            R = np.append(R, data[i,j,color])
                        elif color == 1:
                            G = np.append(G, data[i,j,color])
                        elif color == 2:
                            B = np.append(B, data[i,j,color])
                        else:
                            print('ERROR')

        elif direction == 'LRcolsDUrows':
            for color in range(channels):
                for j in range(cols):
                    for i in reversed(range(rows)):
                        if color == 0:
                            R = np.append(R, data[i,j,color])
                        elif color == 1:
                            G = np.append(G, data[i,j,color])
                        elif color == 2:
                            B = np.append(B, data[i,j,color])
                        else:
                            print('ERROR')

        elif direction == 'RLcolsDUrows':
            for color in range(channels):
                for j in reversed(range(cols)):
                    for i in reversed(range(rows)):
                        if color == 0:
                            R = np.append(R, data[i,j,color])
                        elif color == 1:
                            G = np.append(G, data[i,j,color])
                        elif color == 2:
                            B = np.append(B, data[i,j,color])
                        else:
                            print('ERROR')


    elif columns == False:
        if direction == 'LRcolsUDrows':
            for color in range(channels):
                for i in range(rows):
                    for j in range(cols):
                        if color == 0:
                            R = np.append(R, data[i,j,color])
                        elif color == 1:
                            G = np.append(G, data[i,j,color])
                        elif color == 2:
                            B = np.append(B, data[i,j,color])
                        else:
                            print('ERROR')

        elif direction == 'RLcolsUDrows':
            for color in range(channels):
                for i in range(rows):
                    for j in reversed(range(cols)):
                        if color == 0:
                            R = np.append(R, data[i,j,color])
                        elif color == 1:
                            G = np.append(G, data[i,j,color])
                        elif color == 2:
                            B = np.append(B, data[i,j,color])
                        else:
                            print('ERROR')

        elif direction == 'LRcolsDUrows':
            for color in range(channels):
                for i in reversed(range(rows)):
                    for j in range(cols):
                        if color == 0:
                            R = np.append(R, data[i,j,color])
                        elif color == 1:
                            G = np.append(G, data[i,j,color])
                        elif color == 2:
                            B = np.append(B, data[i,j,color])
                        else:
                            print('ERROR')

        elif direction == 'RLcolsDUrows':
            for color in range(channels):
                for i in reversed(range(rows)):
                    for j in reversed(range(cols)):
                        if color == 0:
                            R = np.append(R, data[i,j,color])
                        elif color == 1:
                            G = np.append(G, data[i,j,color])
                        elif color == 2:
                            B = np.append(B, data[i,j,color])
                        else:
                            print('ERROR')
