import scipy.io.wavfile as sciWav
import scipy.signal as sciSig
import matplotlib.pyplot as matp
import numpy

# Funcion: Conforma un grafico con los elementos de entrada, el cual muestra al final de proceso
# Entradas: Datos del eje x e y, titulo del grafico, label's de ambos ejes.
# Salida:   Gráfico standard.
def graph(datax, datay, title, ylabel, xlabel):
    matp.plot(datax, datay)
    matp.title(title)
    matp.ylabel(ylabel)
    matp.xlabel(xlabel)
    matp.show()

# Funcion: Conforma el espectrograma de una señal
# Entradas: rate sampling de una señal y amplitudes de la señal·
# Salida: Espectrograma
def graphSpectro(rate, audio, subtitle):
	f, t, Sxx = sciSig.spectrogram(audio, rate)
	matp.pcolormesh(t, f, numpy.log10(Sxx))
	matp.ylabel('Frequency [Hz]')
	matp.xlabel('Time [s]')
	matp.colorbar()
	matp.title("Espectrograma frecuencia vs tiempo: " + subtitle)
	matp.show()

# Funcion: Se genera una señal filtro en el dominio del tiempo
# Entradas: rate sampling del audio original, cantidad de puntos discretos del filtro, frecuencia mínima, frecuencia máxima
# Salida: Señal filtro pasabanda de lowFreq a highFreq
def createFilterPassBand(rate,numtaps,lowFreq,highFreq):
	#Numero de coeficientes del filtro, mas abrupto el corte del audio a medida que numtaps aumente
	filter = sciSig.firwin(numtaps, [lowFreq,highFreq], pass_zero=False, fs=rate)
	return filter

# Funcion: Se filtra la señal original convolucionando la señal original con la señal filtro
# Entradas: Información de la señal original (rate y amplitudes), señal filtro
# Salida: Señal convolucionada (filtrada), dejando las frecuencias relevantes.
def getFilteredAudio(data,filter):
	rate = data[0]
	audio = data[1]
	convolve = sciSig.convolve(audio,filter, mode='same')
	return convolve

# Funcion: Genera el gráfico de la señal original (Pasado por la transformada de Fourier) en el dominio de la amplitud vs la frecuencia
# Entradas: Amplitudes discretizadas de la señal en el dominio del tiempo, subtitulo del gráfico, sample rate de una señal
# Salida: Gráfico de la señal original en función de la Amplitud y frecuencia [Hz]
def showFourier(audio,labbel, rate):
	fourierFreq = numpy.fft.fftfreq(len(audio), 1/rate)
	fourier = numpy.fft.fft(audio)
	graph(fourierFreq,numpy.abs(fourier.real),"Gráfico amplitud vs frecuencia: T. Fourier "+labbel, "Amplitud", "Frecuencia [Hz]")

# Funcion: Genera el gráfico del filtro en el dominio del tiempo.
# Entradas: Señal del filtro discretizada
# Salida: Gráfico del filtro amplitud vs tiempo
def showFilter(filter):
	matp.plot(filter)
	matp.title("Gráfico amplitud vs tiempo: Filtro")
	matp.ylabel("Amplitud")
	matp.xlabel("Tiempo [s]")
	matp.show()

# Funcion: Genera el gráfico del filtro (Pasado por la transformada de Fourier) en el dominio de la amplitud vs la frecuencia
# Entradas: Amplitudes discretizadas de la señal en el dominio del tiempo, subtitulo del gráfico, sample rate de una señal
# Salida: Gráfico del filtro en función de la Amplitud y frecuencia [Hz]
def showFilterFourier(audio,labbel, rate):
	fourierFreq = numpy.fft.fftfreq(len(audio), 1/rate)
	fourier = numpy.fft.fft(audio)
	graph(fourierFreq,numpy.abs(fourier.real),"Gráfico amplitud vs frecuencia: T. Fourier "+labbel, "Amplitud", "Frecuencia [Hz]")


# Funcion: Genera el gráfico de la señal inversa a la transformada de Fourier, en el dominio de la amplitud vs el tiempo.
# Entradas: Amplitudes discretizadas de la señal en el dominio de la frecuencia, sample rate de la señal original, subtitulo del gráfico
# Salida: Gráfico de la señal original en función de la Amplitud y el tiempo [s] , y archivo .wav del audio pasado por la transformada inversa
def showFourierInv(audio,rate,labbel):
	fourier = numpy.fft.fft(audio)
	fourierInv = numpy.fft.ifft(fourier)
	time = numpy.linspace(0,len(audio)/rate, num=len(audio))
	graph(time, fourierInv.real,"Gráfico amplitud vs tiempo: Transformado "+labbel, "Amplitud", "Tiempo [s]")
	sciWav.write("handel"+labbel+".wav", rate, numpy.int16(fourierInv.real))

# Cuerpo principal del laboratorio donde se llaman todas las funciones necesarias para el correcto funcionamiento de la experiencia.
if __name__ == '__main__':

	# -------------------------------------------------------- PUNTO 1 --------------------------------------------------------
	data = sciWav.read('handel.wav')
	rate = data[0]
	originalAudio = data[1]


	# -------------------------------------------------------- PUNTO 2 --------------------------------------------------------
	# Se genera el Espectrograma de la función original
	graphSpectro(rate, originalAudio, "Audio original")

	# -------------------------------------------------------- PUNTO 3 --------------------------------------------------------
	# Se genera un filtro pasabanda de 500 a 1300
	filter = createFilterPassBand(rate,60,500,1300)

	#Filtro con numstap = 1 (El peor, no hace nada)
	#filter = createFilterPassBand(rate,3,500,1300)

	#Filtro con numstap = largo del arreglo de audio original ("El mejor")
	#filter = createFilterPassBand(rate,len(data[1]),500,1300)

	# Se genera un gráfico del filtro en el dominio del tiempo
	showFilter(numpy.abs(filter))
	# Se genera un gráfico del filtro en el dominio de la frecuencia
	showFilterFourier(filter, "Filtro", rate)

	# Se filtra audio original
	filteredAudio = getFilteredAudio(data,filter)

	# Se genera un gráfico de la señal original en el dominio de la frecuencia
	showFourier(originalAudio,"Original", rate)
	# Se genera un gráfico de la señal filtrada en el dominio de la frecuencia
	showFourier(filteredAudio,"Filtrada", rate)

	# Se genera el Espectrograma de la función filtrada
	graphSpectro(rate, filteredAudio, "Audio filtrado")

	# -------------------------------------------------------- PUNTO 4 --------------------------------------------------------

	# Se genera un gráfico de la señal original en el dominio del tiempo (Haciendo la inversa de Fourier) y un archivo .wav
	showFourierInv(originalAudio,rate,"Original")
	# Se genera un gráfico de la señal filtrada en el dominio del tiempo (Haciendo la inversa de Fourier) y un archivo .wav
	showFourierInv(filteredAudio,rate,"Filtrada")

