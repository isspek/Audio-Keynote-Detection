import essentia
from essentia.streaming import *
from essentia import Pool
import os
from pylab import plot, show, figure, imshow


def extract_HPCP(_filename):
    
    # initialization

    pool = Pool()
    loader = MonoLoader(filename = _filename)
    frameCutter = FrameCutter(frameSize = 4096, hopSize = 512)
    window = Windowing(type = 'blackmanharris62')
    spectrum = Spectrum()
    spectralPeaks= SpectralPeaks(orderBy="magnitude",
                              magnitudeThreshold=1e-05,
                              minFrequency=100.0,
                              maxFrequency=5000.0, 
                              maxPeaks=10000)
    hpcp = HPCP(size = 36,
                   bandPreset = False,
                   minFrequency = 100.0,
                   maxFrequency = 5000.0,
                   weightType = 'squaredCosine',
                   nonLinear = False,
                   normalized=True,
                   sampleRate= 44100.0,
                   windowSize = 4.0/3.0)

    # audio-->frame cutter-->windowing-->spectrum-->spectral peaks-->HPCP 

    loader.audio >> frameCutter.signal
    frameCutter.frame >> window.frame >> spectrum.frame
    spectrum.spectrum >> spectralPeaks.spectrum
    spectralPeaks.magnitudes >> hpcp.magnitudes
    spectralPeaks.frequencies >> hpcp.frequencies
    hpcp.hpcp >> (pool, 'hpcp vector')
    # run streaming algorithms
    essentia.run(loader)
    return pool['hpcp vector']


ground_truth=[]
features=[]

for dirname, dirnames, filenames in os.walk('./mirex_key'):
    for filename in sorted(filenames):
        if dirname=='./mirex_key/audio':
            features.append(extract_HPCP(os.path.join(dirname, filename)))
        else:
            file = open(os.path.join(dirname, filename), 'r')
            ground_truth.append(file.read())











