import scipy.io.wavfile as sciWav
import scipy.signal as sciSig
import matplotlib.pyplot as matp
import numpy

# Funcion: Conforma un grafico con los elementos de entrada, el cual muestra al final de proceso
# Entradas: Datos del eje x e y, titulo del grafico, label's de ambos ejes.
# Salida:   N/A
def graph(datax, datay, title, ylabel, xlabel):
    matp.plot(datax, datay)
    matp.title(title)
    matp.ylabel(ylabel)
    matp.xlabel(xlabel)
    matp.show()


# -------------------------------------------------------- PUNTO 1 --------------------------------------------------------

# Se lee el archivo de audio de entrada con la funcion read de scipy.
# el cual entrega el valor del rate, ademas de un arreglo de las respectivas amplitudes del audio junto con su dtype.
data = sciWav.read('handel.wav')
rate = data[0]
audio = data[1]


f, t, Sxx = sciSig.spectrogram(audio, rate)
matp.pcolormesh(t, f, numpy.log10(Sxx))
matp.ylabel('Frequency [Hz]')
matp.xlabel('Time [sec]')
matp.colorbar()
matp.show()

# A razon de los valores obtenidos anteriormente, se conforma un arreglo de tiempos con ayuda de la funcion
# linspace de numpy, el cual toma como entrada: (valor del primer elemento, valor del ultimo elemento, total de elementos)
time = numpy.linspace(0,len(audio)/rate, num=len(audio))

#Filtro pasa banda, de la frecuencia 500 a 1300
filter = sciSig.firwin(60, [500, 1300], pass_zero=False, fs=rate)

convolve = sciSig.convolve(filter, audio, mode='valid')

# Se calcula la tranformada de fourier a partir de las amplitudes del audio, por medio de la funcion fft de numpy.
fourier = numpy.fft.fft(convolve)
# --DUDA--
# Se utiliza la funcion fftfreq para obtener un arreglo compuesto por el rango de frecuencias del audio.
fourierFreq = numpy.fft.fftfreq(len(convolve), 1/rate)

# Se obtiene la transformada de fourier inversa de lo obtenido en el punto anterior. Esto por medio de la funcion ifft de numpy.
fourierInv = numpy.fft.ifft(fourier)

graph(fourierFreq,numpy.abs(fourier),"Gráfico amplitud vs frecuencia: Transformada de Fourier", "Amplitud", "Frecuencia (Hz)")

graph(time, fourierInv,"Gráfico amplitud vs tiempo: Transformado", "Amplitud", "Tiempo (s)")

f, t, Sxx = sciSig.spectrogram(fourierInv, rate)
matp.pcolormesh(t, f, numpy.log10(Sxx))
matp.ylabel('Frequency [Hz]')
matp.xlabel('Time [sec]')
matp.colorbar()
matp.show()