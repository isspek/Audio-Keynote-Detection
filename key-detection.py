'''
    File name: key-detection.py
    Author: Ipek B.
    Date created: 22/05/2016
    Date last modified: 
    Python Version: 2.7.6
'''
import os
import numpy
import scipy.io.wavfile as wav



"""
Reading the audio files as .wav format, and storing in an array.
"""

audioFiles=[]


def read_wave(path):
    wav.read(path,0)
    

for dirname, dirnames, filenames in os.walk('./mirex_key/audio'):
    for filename in sorted(filenames):
        audioFiles.append(read_wave(os.path.join(dirname, filename)));


