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


def graphSpectro(rate, audio):
	f, t, Sxx = sciSig.spectrogram(audio, rate)
	matp.pcolormesh(t, f, numpy.log10(Sxx))
	matp.ylabel('Frequency [Hz]')
	matp.xlabel('Time [sec]')
	matp.colorbar()
	matp.show()


def createFilterPassBrand(rate,numtaps,lowFreq,highFreq):
	#Numero de coeficientes del filtro, mas abrupto el corte del audio a medida que numtaps aumente
	filter = sciSig.firwin(numtaps, [lowFreq,highFreq], pass_zero=False, fs=rate)
	return filter

def getFilteredAudio(data,filter):
	rate = data[0]
	audio = data[1]
	convolve = sciSig.convolve(audio,filter, mode='same')
	return convolve

def showFourier(audio,labbel):
	fourierFreq = numpy.fft.fftfreq(len(audio), 1/rate)
	fourier = numpy.fft.fft(audio)
	graph(fourierFreq,numpy.abs(fourier),"Gráfico amplitud vs frecuencia: Transformada de Fourier "+labbel, "Amplitud", "Frecuencia (Hz)")

def showFourierInv(audio,rate,labbel):
	fourier = numpy.fft.fft(audio)
	fourierInv = numpy.fft.ifft(fourier)
	time = numpy.linspace(0,len(audio)/rate, num=len(audio))
	graph(time, fourierInv,"Gráfico amplitud vs tiempo: Transformado "+labbel, "Amplitud", "Tiempo (s)")
	sciWav.write("handel"+labbel+".wav", rate, numpy.int16(fourierInv))


data = sciWav.read('handel.wav')
rate = data[0]
filter = createFilterPassBrand(rate,60,500,1300)

originalAudio = data[1]
filteredAudio = getFilteredAudio(data,filter)

showFourier(originalAudio,"Original")
showFourier(filteredAudio,"Filtrada")

showFourierInv(originalAudio,rate,"Original")
showFourierInv(filteredAudio,rate,"Filtrada")

graphSpectro(rate, originalAudio)
graphSpectro(rate, filteredAudio)



