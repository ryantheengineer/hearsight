from PIL import Image
from matplotlib import image
from matplotlib import pyplot



def openImage(filename):
    image = Image.open(filename)
    return image

def imageArray(filename):
    image = image.imread(filename)
    return image
