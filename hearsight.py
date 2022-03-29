from PIL import Image
from matplotlib import image
import matplotlib.pyplot as plt
import cv2
import numpy as np



def im2array(filename):
    image = Image.open(filename)
    imarray = np.asarray(image)    
    return imarray

def imhist(imarray):
    n_bins = 256
    first_edge = -0.5
    last_edge = 255.5
    # bin_edges = np.linspace(start=first_edge, stop=last_edge,
    #                         num=n_bins+1, endpoint=True)
    Bhist, Bbin_edges = np.histogram(imarray[:,0], bins=n_bins, range=(0,256))
    Ghist, Gbin_edges = np.histogram(imarray[:,1], bins=n_bins, range=(0,256))
    Rhist, Rbin_edges = np.histogram(imarray[:,2], bins=n_bins, range=(0,256))
    return Bhist, Bbin_edges, Ghist, Gbin_edges, Rhist, Rbin_edges


# Main function
if __name__ == '__main__':
    imarray = im2array("rainbow-mountains-2.jpg")
    Bhist, Bbin_edges, Ghist, Gbin_edges, Rhist, Rbin_edges = imhist(imarray)
    
    plt.plot(Bhist, 'b')
    plt.title("Blue")
    plt.plot(Ghist, 'g')
    plt.title("Green")
    plt.plot(Rhist, 'r')
    plt.title("Red")
