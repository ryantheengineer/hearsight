from PIL import Image
from matplotlib import image
import matplotlib.pyplot as plt
import cv2
import numpy as np
import scipy
from scipy.io.wavfile import write


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


def hist_to_wave_equal_disperse(hist,lowfreq,highfreq,samplename):
    sample_time = 5.0
    samplerate = 44100
    t = np.linspace(0., sample_time, int(sample_time)*samplerate)
    output = np.zeros(len(t))
    
    # maxamp = np.max(hist)
    
    for i,val in enumerate(hist):
        frac = (i+1)/len(hist)
        fs = lowfreq + frac * (highfreq - lowfreq)
        data = val * np.sin(2. * np.pi * fs * t)
        output += data
        
    # Scale output to int16 min and max
    output_interp = np.interp(output, (output.min(), output.max()), (np.iinfo(np.int16).min, np.iinfo(np.int16).max))
        
    # Write output to mp3
    write(samplename, samplerate, output_interp.astype(np.int16))
    

# Main function
if __name__ == '__main__':
    imgname = "rainbow-mountains-2.jpg"
    imarray = im2array(imgname)
    Bhist, Bbin_edges, Ghist, Gbin_edges, Rhist, Rbin_edges = imhist(imarray)
    
    plt.plot(Bhist, 'b')
    plt.title("Blue")
    plt.plot(Ghist, 'g')
    plt.title("Green")
    plt.plot(Rhist, 'r')
    plt.title("Red")
    
    minfreq = 1000
    maxfreq = 20000
    hist_to_wave_equal_disperse(Bhist,minfreq,maxfreq,"Blue_{}_{}.wav".format(minfreq,maxfreq))
    hist_to_wave_equal_disperse(Ghist,minfreq,maxfreq,"Green_{}_{}.wav".format(minfreq,maxfreq))
    hist_to_wave_equal_disperse(Rhist,minfreq,maxfreq,"Red_{}_{}.wav".format(minfreq,maxfreq))
