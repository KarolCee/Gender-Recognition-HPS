from numpy import *
from scipy import *
import numpy as np
import scipy.io.wavfile
from scipy import signal as sig
import warnings
import sys

warnings.filterwarnings("ignore")


def funkcja(nazwa_pliku):

    #czytamy plik i wyciagamy czestotliwosc probkowania
    w, signal = scipy.io.wavfile.read(nazwa_pliku)
    #jesli sa dwa kanaly to je usredniamy
    if len(signal.shape) == 2:
        signal = [(s[0] + s[1]) / 2 for s in signal]

    signal = np.array(signal)
    n = len(signal)

    # Spektrum
    furier = fft(signal)
    furier = abs(furier)
    # Wyliczenie czestotliwosci i amplitud dla spektrum
    freqs = []
    amps = []
    for i in range(n):
        freq = i * w / n
        freqs.append(freq)
    for i in range(n):
        if i == 0:
            amp = (furier[i] / 2) / (n / 2)
        else:
            amp = (furier[i]) / (n / 2)
        amps.append(amp)
    freqs = np.array(freqs)
    amps = np.array(amps)

    # Sprawdzamy pierwsza polowe spektrum - lustrzane odbicie pomijamy
    freqs = freqs[:len(freqs) // 2]
    amps = amps[:len(amps) // 2]

    # metoda HARMONIC PRODUCT SPECTRUM
    amps_HPS = amps[:]
    freqs_HPS = freqs[:]
    final_length = 0
    min_downsample = 2
    max_downsample = 5
    for downsample_factor in reversed(range(min_downsample,max_downsample+1)):
        downsampled = sig.decimate(amps, downsample_factor)
        if downsample_factor==max_downsample:
            final_length = len(downsampled)
        amps_HPS = amps_HPS[:final_length] * downsampled[:final_length]
        freqs_HPS = freqs_HPS[:final_length]

    maximum = 0
    indeks = 0
    for i, element in enumerate(amps_HPS):
        #nie interesuja nas maksima dla f < 80hz
        if freqs[i]>80:
            if element > maximum:
                maximum = element
                indeks = i

    #zakladamy ze mezczyzna ponizej 160 Hz
    if freqs[indeks] < 160:
        odp = "Man"
    else:
        odp = "Woman"
    return odp
try:
    odpowiedz = funkcja(sys.argv[1])
    print(odpowiedz)
except:
    print("Woman")

