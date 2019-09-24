import scipy.io.wavfile as sci
import matplotlib.pyplot as matp
import numpy


# -------------------------------------------------------- PUNTO 1 --------------------------------------------------------

# Se lee el archivo de audio de entrada con la funcion read de scipy.
# el cual entrega el valor del rate, ademas de un arreglo de las respectivas amplitudes del audio junto con su dtype.
data = sci.read('handel.wav')
rate = data[0]
audio = data[1]

