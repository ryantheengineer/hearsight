from PIL import Image
from matplotlib import image
from matplotlib import pyplot
import numpy as np
from scipy.io.wavfile import write

######### DEV NOTES ##################
# 4/8/21: So far, the resulting output wav files are extremely noisy and very
# long, since they are using every single pixel value in a very large picture
# (3457 x 5194 pixels = 17955658 pixels total = nearly 7 minutes of audio when
# sampled at 44100 samples per second standard).

# One way to deal with both the noise and the audio length would be to sample
# at fewer points, but take an average of a range of pixels around the sample
# point. In this way, the values should be more closely related as they rise and
# fall. The "smoothness" might be controllable with the size of the sampling
# box. There would still need to be different paths to take to generate the
# waveform. It might be useful to implement a drawing function that lets the
# user choose the path of sampling, so they can choose more interesting parts of
# the photo. This might require OpenCV.

# 4/9/21: Merge function works okay, need a better way to handle large datasets
# without crashing (ex: when sample box is 3x3). Maybe with generators?

def genFromZero(maxval):
    num = 0
    while num < maxval:
        yield num
        num += 1

def genFromVal(startval,endval):
    if startval < endval:
        num = startval
        while num < endval:
            yield num
            num += 1
    else:
        print('ERROR: Starting value must be smaller than ending value')

def openImage(filename):
    image = Image.open(filename)
    return image

def imageArray(filename): # This function doesn't work correctly yet
    image = image.imread(filename)
    return image

def imageToArray(image):
    # image.show
    image.close
    data = np.asarray(image,dtype=np.int16)
    print(type(data))
    print(data.shape)
    return data

# Scale image data to range of values acceptible in chosen WAV format (this
# needs to be adjusted to account for image format-- JPEG won't work with this
# math)
def scaleToWAV(vector):
    maxval = max(vector)
    if maxval <= 255 and maxval >= 230:
        vector *= 257

    for i in range(len(vector)):
        vector[i] -= 32768 # Might need to add a range check
    return vector

def vectorToWAV(vector,outputFileName): # THE ENCODING DOESN'T CURRENTLY WORK
    sps = 44100
    write(outputFileName, sps, vector.astype(np.int16)) # GOT THIS TO WORK WHEN ASTYPE IS UINT8 FOR THE DATA I'M WORKING WITH
    # Might want to add a function that plays the output file?

def vectorizeMergeRGB(data, boxdim, columns, direction):
    # Create a new sampled array for each color channel, and then turn data into
    # a column vector as vectorizeRGB does, choosing the sampling paradigm
    # (sampling paradigm later might include a spiral path or something to
    # prevent regular abrupt changes found in using columns or rows)

    datarows = data.shape[0]
    datacols = data.shape[1]
    channels = data.shape[2]

    Rdata = np.asarray(data[:,:,0])
    Gdata = np.asarray(data[:,:,1])
    Bdata = np.asarray(data[:,:,2])

    samplerows = datarows - boxdim + 1
    samplecols = datacols - boxdim + 1

    Rsample = np.zeros([samplerows, samplecols])
    Gsample = np.zeros([samplerows, samplecols])
    Bsample = np.zeros([samplerows, samplecols])

    for i in range(samplerows):
        for j in range(samplecols):
            # Calculate the average pixel value for the appropriate channel
            Ravg = 0.
            Bavg = 0.
            Gavg = 0.

            rowsrange = range(i, i+boxdim)
            colsrange = range(j, j+boxdim)

            for m in rowsrange:
                for n in colsrange:
                    Ravg += Rdata[m,n]
                    Gavg += Gdata[m,n]
                    Bavg += Bdata[m,n]  # For now the channel splitting is happening early and explicitly to make it clear, but later this should be automated and the channel split should be at the very end for efficiency

            Ravg /= boxdim**2
            Gavg /= boxdim**2
            Bavg /= boxdim**2

            Rsample[i,j] = Ravg
            Gsample[i,j] = Gavg
            Bsample[i,j] = Bavg

    # Vectorize the RGB data THIS IS NOT FINISHED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    vlength = samplerows*samplecols

    R = np.zeros(vlength)
    G = np.zeros(vlength)
    B = np.zeros(vlength)

    vindex = 0

    if columns == True:
        if direction == 'LRcolsUDrows':
            for j in range(samplecols):
                for i in range(samplerows):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = Rsample[i,j]
                        elif color == 1:
                            G[vindex] = Gsample[i,j]
                        elif color == 2:
                            B[vindex] = Bsample[i,j]
                        else:
                            print('ERROR')

                    vindex += 1


        elif direction == 'RLcolsUDrows':
            for j in reversed(range(samplecols)):
                for i in range(samplerows):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = Rsample[i,j]
                        elif color == 1:
                            G[vindex] = Gsample[i,j]
                        elif color == 2:
                            B[vindex] = Bsample[i,j]
                        else:
                            print('ERROR')

                    vindex += 1

        elif direction == 'LRcolsDUrows':
            for j in range(samplecols):
                for i in reversed(range(samplerows)):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = Rsample[i,j]
                        elif color == 1:
                            G[vindex] = Gsample[i,j]
                        elif color == 2:
                            B[vindex] = Bsample[i,j]
                        else:
                            print('ERROR')

                    vindex += 1

        elif direction == 'RLcolsDUrows':
            for j in reversed(range(samplecols)):
                for i in reversed(range(samplerows)):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = Rsample[i,j]
                        elif color == 1:
                            G[vindex] = Gsample[i,j]
                        elif color == 2:
                            B[vindex] = Bsample[i,j]
                        else:
                            print('ERROR')

                    vindex += 1



    elif columns == False:
        if direction == 'LRcolsUDrows':
            for i in range(samplerows):
                for j in range(samplecols):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = Rsample[i,j]
                        elif color == 1:
                            G[vindex] = Gsample[i,j]
                        elif color == 2:
                            B[vindex] = Bsample[i,j]
                        else:
                            print('ERROR')

                    vindex += 1


        elif direction == 'RLcolsUDrows':
            for i in range(samplerows):
                for j in reversed(range(samplecols)):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = Rsample[i,j]
                        elif color == 1:
                            G[vindex] = Gsample[i,j]
                        elif color == 2:
                            B[vindex] = Bsample[i,j]
                        else:
                            print('ERROR')

                    vindex += 1

        elif direction == 'LRcolsDUrows':
            for i in reversed(range(samplerows)):
                for j in range(samplecols):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = Rsample[i,j]
                        elif color == 1:
                            G[vindex] = Gsample[i,j]
                        elif color == 2:
                            B[vindex] = Bsample[i,j]
                        else:
                            print('ERROR')

                    vindex += 1

        elif direction == 'RLcolsDUrows':
            for i in reversed(range(samplerows)):
                for j in reversed(range(samplecols)):
                    for color in range(channels):
                        if color == 0:
                            R[vindex] = Rsample[i,j]
                        elif color == 1:
                            G[vindex] = Gsample[i,j]
                        elif color == 2:
                            B[vindex] = Bsample[i,j]
                        else:
                            print('ERROR')

                    vindex += 1

    return [R,G,B]

## CONSIDER USING THIS FUNCTION TO SHORTEN VECTORIZERGB FUNCTION BELOW
# def fillVector(vindex, R, G, B, data, i, j, color):
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
