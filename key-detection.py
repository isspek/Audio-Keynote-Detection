'''
    File name: key-detection.py
    Author: isspek
    Date created: 22/05/2016
    Date last modified: 
    Python Version: 2.7.6
'''
import os
import numpy
import scipy.io.wavfile as wav



"""
Reading the audio files as .wav format, and storing their rate and data in an array.
"""

class Audio:
    def __init__(self, rate, data):
        self.rate=rate
        self.data=data

def create_audio_objs(path):
    rate, data= wav.read(path,0)
    return Audio(rate,data)

audioArray=[]

for dirname, dirnames, filenames in os.walk('./mirex_key/audio'):
    for filename in sorted(filenames):
        audioArray.append(create_audio_objs(os.path.join(dirname, filename)));

for i in range(len(audioArray)):
    print audioArray[i].data
