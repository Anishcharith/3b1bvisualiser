import os
import scipy.io.wavfile
from numpy import fft as fft
import sys
import matplotlib.pyplot as plt
import numpy as np


def d2xy(n, d):
    """
    take a d value in [0, n**2 - 1] and map it to
    an x, y value (e.g. c, r).
    """
    assert(d <= n**2 - 1)
    t = d
    x = y = 0
    s = 1
    while (s < n):
        rx = 1 & int(t / 2)
        ry = 1 & int(int(t) ^ rx)
        x, y = rot(s, x, y, rx, ry)
        x += s * rx
        y += s * ry
        t /= 4
        s *= 2
    return x, y

def rot(n, x, y, rx, ry):
    """
    rotate/flip a quadrant appropriately
    """
    if ry == 0:
        if rx == 1:
            x = n - 1 - x
            y = n - 1 - y
        return y, x
    return x, y

def HilbertMapping(x,y,level):
    maxi=0
    n = 1 << level
    m = np.zeros((n, n))
    maxi=max(x)
    for i in range(0, len(x)):
        c, r = d2xy(n, int(round((n**2 - 1) * x[i] /maxi)))
        m[r][c] += y[i]
    return m
    
def bins(x,y,level):
    n = 1<<level
    m=np.zeros(n*n)
    maxi=max(x)
    for i in range(0, len(x)):
        c=int(round((n**2-1)*x[i]/maxi))
        m[c]+=y[i]
    return m

def plotbars(data,filename):
    x=np.arange(len(data))
    plt.bar(x,data,color="black")
    plt.ylim(ymax=1)
    plt.tick_params(
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    left='off',
    right='off',
    labelbottom='off',
    labeltop='off',
    labelleft='off',
    labelright='off')
    plt.ticklabel_format(useOffset=False)
    plt.savefig(filename+'.jpg',format='jpg')
    plt.close()

def saveFig(data,filename):
    #plt.matshow(data,fignum=False,cmap='binary',vmin=0,vmax=1)
    plt.matshow(data,fignum=False,cmap='binary',vmin=0)
    #plt.axis('off')
    plt.tick_params(
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    left='off',
    right='off',
    labelbottom='off',
    labeltop='off',
    labelleft='off',
    labelright='off')

    plt.savefig(filename+'.jpg',format='jpg')
    plt.close()

def modFig(data,filename):

    fig = plt.figure(figsize=(8,8),tight_layout=False) # Notice the equal aspect ratio
    ax = [fig.add_subplot(2,2,i+1) for i in range(4)]
    
    ax[0].matshow([i[::-1] for i in data[::-1]],cmap='Blues',vmin=0)
    ax[1].matshow(data,cmap='Blues',origin='lower',vmin=0)
    ax[2].matshow([i[::-1] for i in data[::-1]],origin='lower',cmap='Blues',vmin=0)
    ax[3].matshow(data,cmap='Blues',vmin=0)
    for a in ax:
        a.set_xticklabels([])
        a.set_yticklabels([])
        a.set_aspect('auto')

        a.axis('off')
        a.tick_params(
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        left='off',
        right='off',
        labelbottom='off',
        labeltop='off',
        labelleft='off',
        labelright='off')

    fig.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(filename+'.jpg',format='jpg')
    plt.close()


audiofile=sys.argv[1]
audioname=audiofile.split('.')[0].split('/')[-1]
rate,aud_data=scipy.io.wavfile.read('audio_input/'+audiofile)
duration=len(aud_data)/rate
fouriers_per_second=24
fourier_width=1/fouriers_per_second
total_frames=int(round(duration*fouriers_per_second))
fig=plt.figure()
os.system('mkdir -p samples/'+audioname)
savesamples='samples/'+audioname
totenergy=sum(abs(aud_data))/(total_frames*4*4)
print(totenergy)
for offset in range(total_frames):
    start=int(round(offset*fourier_width*rate))
    end=int(round((offset*fourier_width+fourier_width)*rate))
    print("Processing sample %i of %i (%d seconds)" % (offset + 1, total_frames, end/float(rate)))
    print(start,end)
    sample_range=aud_data[start:end]
    fft_data=abs(fft.fft(sample_range))
    freqs = fft.fftfreq(len(fft_data))
    fft_data=fft_data[:int(len(fft_data)/4)]
    #fft_data=fft_data/totenergy
    freqs=freqs[:int(len(freqs)/4)]
    ###############         hilbertcurve
    m=HilbertMapping(freqs,fft_data,4)  # change order of hilbert curve here
    modFig(m,savesamples+'/frame_'+str(offset).zfill(5))
    #saveFig(m,savesamples+'/frame_'+str(offset).zfill(5))
    ###############
    """
    ###############         not hilbert
    m=bins(freqs,fft_data,4)
    plotbars(m,savesamples+'/frame_'+str(offset).zfill(5))
    ##############         
    """

print("done!")
