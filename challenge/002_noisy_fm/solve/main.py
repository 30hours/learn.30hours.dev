# Generate audio from noisy FM data.

# Author: 30hours

import numpy as np
import scipy.signal as signal
from scipy.io.wavfile import write
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

def load_iq_data(iq_file_path):

    """
    @brief Load interleaved IQ data from a binary file.
    @param iq_file_path (str): Path to the binary file containing interleaved IQ data.
    @return np.array: The complex-valued IQ data.
    """

    interleaved_data = np.fromfile(iq_file_path, dtype=np.float64)

    I = interleaved_data[0::2]
    Q = interleaved_data[1::2]
    iq_data = I + 1j * Q

    return iq_data

def fm_demodulate(iq_data, fs, fd):

    """
    @brief FM demodulate an IQ modulated signal back to baseband.
    @param iq_data (np.array): Complex-valued IQ data representing the FM modulated signal.
    @param fs (int): Sampling rate of the IQ data.
    @param fd (int): Maximum deviation of the frequency from the carrier in Hz.
    @return np.array: The demodulated baseband signal.
    """

    # calculate the phase of the IQ data
    phase = np.unwrap(np.angle(iq_data))
    
    # differentiate the phase to get the frequency
    frequency = np.diff(phase) * fs / (2 * np.pi)
    
    # get the original baseband signal
    baseband = frequency / fd
    baseband = np.pad(baseband, (1, 0), 'constant')

    return baseband

def plot_frequency(x, fs, filename):

    """
    @brief Plot the frequency spectrum of a signal and save it to a file.
    @param x (np.array): The input signal.
    @param fs (float): The sampling rate of the input signal in Hz.
    @param filename (str): The filename to save the plot.
    """

    # fft the signal
    yf = fft(x)
    xf = fftfreq(len(x), 1 / fs)
    
    # only keep the positive frequencies
    pos_indices = np.where(xf >= 0)
    xf = xf[pos_indices]
    yf = 10*np.log10(np.abs(yf[pos_indices]))

    # plot and save
    plt.figure(figsize=(10, 6))
    plt.plot(xf, yf)
    plt.title("Frequency Domain")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (dB)")
    plt.grid()
    plt.savefig(filename)
    plt.close()

def plot_time(x, fs, filename):

    """
    @brief Plot the time domain signal and save it to a file.
    @param x (np.array): The input signal.
    @param fs (float): The sampling rate of the input signal in Hz.
    @param filename (str): The filename to save the plot.
    """

    # Create a time array
    t = np.arange(len(x)) / fs
    
    # Plot and save
    plt.figure(figsize=(10, 6))
    plt.plot(t, x)
    plt.title("Time Domain")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.savefig(filename)
    plt.close()

def resample_signal(x, original_rate, target_rate):

    """
    @brief Resample the signal to the target sampling rate.
    @param x (np.array): The signal to resample.
    @param original_rate (int): Original sampling rate of the signal.
    @param target_rate (int): Target sampling rate.
    @return np.array: The resampled signal.
    """

    number_of_samples = int(len(x) * float(target_rate) / original_rate)
    y = signal.resample(x, number_of_samples)

    return y

def low_pass_filter(x, fs, fc, n):
   
    # normalise signal and noise
    max_val = np.max(np.abs(x))
    if max_val > 0:
      x = x/max_val
 
    # design a FIR filter
    b = signal.firwin(n, fc/(fs/2), window='blackmanharris')

    # apply filter to noise
    y = signal.lfilter(b, 1, x)

    # remove impulse
    y = y[1000:]

    # normalise to [-1, 1] and scale to 16-bit range
    max_val = np.max(np.abs(y))
    if max_val > 0:
      y = y/max_val
    y = np.int16(y * 32767)

    return y

iq_data = load_iq_data("/app/challenge/002_noisy_fm/data/iq_data.bin")

# demodulate FM
fs_iq = 200000
fd = 75000
demodulated_signal = fm_demodulate(iq_data, fs_iq, fd)

# resample to audio range
fs_target = 20000
resampled_signal = resample_signal(demodulated_signal, fs_iq, fs_target)

# filter out noise
resampled_signal_clean = low_pass_filter(resampled_signal, fs_target, 3500, 1001)

# save audio files
write("audio_pre_filter.wav", fs_target, resampled_signal)
write("audio_post_filter.wav", fs_target, resampled_signal_clean)

# generate plots
plot_frequency(resampled_signal, fs_target, "frequency_raw")
plot_frequency(resampled_signal_clean, fs_target, "frequency_filtered")
plot_time(resampled_signal, fs_target, "time_raw")
plot_time(resampled_signal_clean, fs_target, "time_filtered")
