import sounddevice as sd
from scipy.io import wavfile
from scipy import fftpack, signal
import wave
import matplotlib.pyplot as plt
import numpy as np
import threading
import time
import datetime
import os

vol_threshold = 1000

class sound_detector(threading.Thread):
    def __init__(self, duration = 5, interval = 5):
        self.sample_rate = 44100
        self.duration = duration
        self.interval = interval #time bewteen recordings
        self.stop = False
        self.is_sound = None
        # inits the threading class
        threading.Thread.__init__(self)

    # Recording a sample
    def record_sample(self, title):
        print("Recording Sample...")
        recording = sd.rec(int(self.duration*self.sample_rate),samplerate = self.sample_rate, channels = 1, dtype='Int16')
        sd.wait()
        # if os.path.exists("recording.wav"):
        #     os.remove("recording.wav")
        # else:
        #     print("The file does not exist")
        # wavfile.write('%s.wav' %(title),self.sample_rate,recording)
        # print("Written to file: %s.wav" %(title))
        # rate,sound = wavfile.read("%s.wav" %(title),'r')
        recording = recording.flatten()
        self.wave_file = recording

    # Opening the sample as np array
    def open_sample(self, title, plot = False):
        """
        Opens a .wav file of specified title.
        Returns:
            0 - Silence
            1 - Voice
            2 - Music
        """
        
        # Opening file, applying FFT
        # print("for %s:" %title)
        # rate, sound = wavfile.read("%s.wav" %(title),'r')
        sound = self.wave_file
        rate = self.sample_rate
        amplitude = sound.shape[0]

        n = len(sound) # length of the signal
        k = np.arange(n)
        T = n/rate
        frq = k/T # two sides frequency range
        frq = frq[range(int(round(n/2)))] # one side frequency range

        Y = fftpack.fft(sound)/n # fft computing and normalization
        Y = Y[range(int(round(n/2)))]
        
        # Plotting
        if plot == True:
            f, ax = plt.subplots(2,1)
            ax[0].plot(np.arange(amplitude) / rate, sound)
            ax[0].set_xlabel('Time [s]')
            ax[0].set_ylabel('Amplitude [unknown]')
            ax[1].plot(frq,abs(Y),'r') # plotting the spectrum
            ax[1].set_xlabel('Freq (Hz)')
            ax[1].set_ylabel('|Y(freq)|')
            plt.xscale("log")
            plt.grid(True)
            ax[1].set_xlim(left = 20, right = 20000)
            plt.title(title)
            plt.show()
            
        # Amplitude Processing
        volume = abs(sound)
        a_peak, properties1 = signal.find_peaks(volume,threshold=7000,distance=500)
        a_peaks = len(a_peak)
        a_avges = []
        a_width = 200
        a_cut_width = 600
        a_no_peak_mean = np.mean(volume)
        # print(len(volume))
        # print(peaks)
        # a_no_peak_slice = volume[:]
        if np.mean(volume) <= vol_threshold:
            # print("Is Silent")
            return 0
        try:
            for i in np.nditer(a_peak):
                a_lower_thresh = int((i-a_width))
                a_upper_thresh = int((i+a_width))
                a_cut_lower_thresh = int((i-a_cut_width))
                a_cut_upper_thresh = int((i+a_cut_width))
                a_avg = np.mean(volume[a_lower_thresh:a_upper_thresh])
                a_cut_avg = np.mean(volume[a_cut_lower_thresh:a_cut_upper_thresh])
                a_avges.append(a_avg)
                a_no_peak_mean -= a_cut_avg*a_cut_width*2/len(volume)
                # if len(a_no_peak_slice)>60000:
                    # a_no_peak_slice = a_no_peak_slice[i-(len(volume)-len(a_no_peak_slice)):]
                # print(len(no_peak_slice))
            a_normalized=np.mean(a_avges)/a_no_peak_mean#np.mean(a_no_peak_slice)
            # print(len(a_avges))
            # print("a_normalized: %f" %(float(a_normalized)))
        except:
            a_normalized = 0
            # print("No peaks")
        # print("Amplitude Peaks: %i" %(a_peaks))
        # print(a_peaks)


        # Frequency Analysis
        freq_plot = abs(Y)
        slice_freq_plot = freq_plot[100*5:7000*5]
        peaks, properties2 = signal.find_peaks(slice_freq_plot,threshold=60,distance=100)
        peaks = peaks/5 +100
        avges = []
        width = 20
        # no_peak_slice = freq_plot[:]
        no_peak_mean = np.mean(freq_plot)
        # print(peaks)
        try:
            for i in np.nditer(peaks):
                lower_thresh = int((i-width)*5)
                upper_thresh = int((i+width)*5)
                avg = np.mean(freq_plot[lower_thresh:upper_thresh])
                avges.append(avg)
                no_peak_mean -= avg*width*2/len(freq_plot)
                # print(i*5-(len(freq_plot)-len(no_peak_slice)))
                # if len(no_peak_slice)>60000:
                    # no_peak_slice = no_peak_slice[int(i*5-(len(freq_plot)-len(no_peak_slice))):]
            # print(np.mean(freq_plot))
            # print(no_peak_mean)
            normalized=np.mean(avges)/no_peak_mean
            # print("normalized: %f" %(float(normalized)))
        except:
            normalized = 0
            # print("No peaks")

        # Weighing both amplitude and frequency
        weight = 0
        # Higher is less likely music
        if a_normalized >1:
            weight += 0.2
        elif a_normalized >= 0.95:
            weight += 0.3
        elif a_normalized >=0.9:
            weight += 0.4
        elif a_normalized >=0.85:
            weight += 0.5
        elif a_normalized >=0.8:
            weight += 0.6
        elif a_normalized >= 0.75:
            weight += 0.7
        else:
            weight += 0.8
        # Higher is less likely music
        if normalized<14:
            weight+= 0.7
        elif normalized <16:
            weight += 0.6
        elif normalized < 19:
            weight += 0.5
        elif normalized<=25:
            weight += 0.4
        elif normalized >25:
            weight += 0.3
        # print("Weight (Likelihood of music): %f" %(round(weight/2,3)))
        if weight >=1:
            # print("Likely Music")
            # print("\n")
            return 2
        else:
            # print("Likely Voice")
            # print("\n")
            return 1
        
    def stop_all(self):
        self.stop = True
    
    def run(self):
        """
        Will record a sample and analyse it every minute
        """
        f = open("log.txt", "a")
        int_log = np.array([]) #for internal logging, averaging over 5 samples
        while self.stop == False:
            self.record_sample("recording")
            # is_music = 0
            is_music = self.open_sample("recording" )
            #writing the logs
            np.append(int_log,is_music)
            f.write("{},{}\n".format(str(datetime.datetime.now()),is_music))
            if len(int_log)>10: #To keep the list at 10 values
                np.delete(int_log,0)
            self.is_sound = int(round(np.mean(is_music),0))
            
            time.sleep(self.interval)
        f.close()
            
# with statement


if __name__ == "__main__":
    sou = sound_detector()
    sou.record_sample("output")
    sou.open_sample("output")


# record_sample("voice")
# open_sample("voice1")
# open_sample("voice3")
# open_sample("fvoice")

# sou = sound_detector()

# sou.record_sample("output")
# sou.open_sample("output", plot=True)

# open_sample("music2")

# open_sample("music")
# open_sample("smusic")
# plt.show()