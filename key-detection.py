import essentia
from essentia.streaming import *
from essentia import Pool
import os
from pylab import plot, show, figure, imshow
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split

def normalize(hpcp):
    m = max(hpcp)
    for i in range(len(hpcp)):
        hpcp[i] = hpcp[i] / m
    return hpcp

def extract_HPCP(_filename):
    
    # initialization
    HPCP_size=36
    pool = Pool()
    key = Key()
    loader = MonoLoader(filename = _filename)
    frameCutter = FrameCutter(frameSize = 4096, hopSize = 512)
    window = Windowing(type = 'blackmanharris62')
    spectrum = Spectrum()
    spectralPeaks= SpectralPeaks(orderBy="magnitude",
                              magnitudeThreshold=1e-05,
                              minFrequency=100.0,
                              maxFrequency=5000.0, 
                              maxPeaks=10000)
    hpcp = HPCP(size = HPCP_size,
                   bandPreset = False,
                   minFrequency = 100.0,
                   maxFrequency = 5000.0,
                   weightType = 'squaredCosine',
                   nonLinear = False,
                   sampleRate= 44100.0,
                   windowSize = 4.0/3.0)

    # audio-->frame cutter-->windowing-->spectrum-->spectral peaks-->HPCP 

    loader.audio >> frameCutter.signal
    frameCutter.frame >> window.frame >> spectrum.frame
    spectrum.spectrum >> spectralPeaks.spectrum
    spectralPeaks.magnitudes >> hpcp.magnitudes
    spectralPeaks.frequencies >> hpcp.frequencies
    hpcp.hpcp>> (pool, 'hpcp vector')
    essentia.run(loader)
    hpcpVector= pool['hpcp vector']
    globalHPCP=[]
    #taking mean value for each frame to get global HPCP 
    globalHPCP=hpcpVector.mean(axis=0) 
    #normalized global HPCP
    globalHPCP=normalize(globalHPCP)
    return globalHPCP

data=[]
labels=[]

for dirname, dirnames, filenames in os.walk('./mirex_key'):
    for filename in sorted(filenames):
        if dirname=='./mirex_key/audio':
            data.append(extract_HPCP(os.path.join(dirname, filename)))
        else:
            file = open(os.path.join(dirname, filename), 'r')
            labels.append(file.read())

# split 60% of data as train, 40% of data as test
dataTrain, dataTest, labelTrain, labelTest = train_test_split(data,labels, test_size=0.4, random_state=0)


predictions=OneVsRestClassifier(LinearSVC(random_state=0)).fit(dataTrain,labelTrain).predict(dataTest)
true=0.0
labelLen=len(labelTest)
for j in range(0,labelLen):
    if predictions[j] == labelTest[j]:
        true=true+1

accuracy=true/labelLen

print accuracy
print labelLen





