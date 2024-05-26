# Generate noisy FM data from audio

# Author: 30hours

from pydub import AudioSegment
import numpy as np
import scipy.signal as signal
from scipy.io.wavfile import write
from scipy.signal import resample
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import yaml

def get_wav_samples(mp3_file_path):

    """
    @brief Extracts audio samples from an MP3 file.
    @param mp3_file_path (str): Path to the MP3 file.
    @return tuple: The audio samples as a numpy array and the sample rate.
    """

    audio = AudioSegment.from_mp3(mp3_file_path)
    samples = np.array(audio.get_array_of_samples())
    
    # convert to mono
    if audio.channels == 2:
        samples = samples[::2]

    return samples, audio.frame_rate

def add_noise(x, fs, noise_level, fc):

    """
    @brief Adds band-limited noise to an input signal.
    @param x (np.array): Input signal.
    @param fs (int): Sampling rate of the input signal.
    @param noise_level (float): Desired noise level.
    @param fc (float): Cutoff frequency for the high-pass filter.
    @return np.array: The noisy signal, normalized and scaled to 16-bit integer range.
    """

    # generate white noise
    noise = np.random.normal(0, 1, len(x))

    # normalise signal and noise
    max_val = np.max(np.abs(x))
    if max_val > 0:
      noise = noise/max_val
    if max_val > 0:
      x = x/max_val

    # apply FIR highpass filter
    numtaps = 2001
    b = signal.firwin(numtaps, fc/(fs/2), pass_zero=False, window='blackmanharris')
    band_limited_noise = signal.lfilter(b, 1, noise)

    # scale band-limited noise to the desired noise level
    band_limited_noise = noise_level * band_limited_noise

    # plot noise
    plot_frequency(band_limited_noise, fs, "frequency_noise")

    # add noise to the signal
    noisy_samples = x + band_limited_noise

    # normalise to [-1, 1] and scale to 16-bit range
    max_val = np.max(np.abs(noisy_samples))
    if max_val > 0:
        noisy_samples = noisy_samples / max_val
    noisy_samples = np.int16(noisy_samples * 32767)

    return noisy_samples

def fm_modulate(x, fs, fd):

    """
    @brief FM modulate an input signal at baseband into IQ data.
    @param x (np.array): Input signal (real-valued).
    @param fs (int): Sampling rate of the input signal.
    @param fd (int): Maximum deviation of the frequency from the carrier in Hz.
    @return np.array: The complex-valued IQ data representing the FM modulated signal.
    """

    # normalise input signal
    x = np.array(x)
    if np.max(np.abs(x)) > 1.0:
        x = x / np.max(np.abs(x))

    phase_deviation = 2 * np.pi * fd * np.cumsum(x) / fs

    I = np.cos(phase_deviation)
    Q = np.sin(phase_deviation)

    return I + 1j * Q

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

    # create a time array
    t = np.arange(len(x)) / fs
    
    # plot and save
    plt.figure(figsize=(10, 6))
    plt.plot(t, x)
    plt.title("Time Domain")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.savefig(filename)
    plt.close()

np.random.seed(0)

# load samples and add noise
samples, fs = get_wav_samples("audio.mp3")
noisy_samples = add_noise(samples, fs, 1000000, 5000)

# resample to 200 kHz
fs_iq = 200000
num_samples = int(len(noisy_samples)*fs_iq/fs)
noisy_samples_resample = resample(noisy_samples, num_samples)

# FM modulate
iq_data = fm_modulate(noisy_samples_resample, fs_iq, 75000)

# save IQ to file
interleaved_data = np.column_stack((iq_data.real, iq_data.imag)).ravel()
interleaved_data.tofile('/app/challenge/002_noisy_fm/data/iq_data.bin')

# write IQ header
header = {'file': 'iq_data.bin', 'nChannels': 1, 'fs': fs_iq, 'fc': 'baseband'}
header_file = '/app/challenge/002_noisy_fm/data/iq_data_header.yml'
with open(header_file, 'w') as yaml_file:
    yaml.dump(header, yaml_file, default_flow_style=False, sort_keys=False)

# save the noisy samples to a WAV file
write("noisy_audio.wav", fs, noisy_samples)

# generate plots
plot_time(samples, fs, "time_samples")
plot_time(noisy_samples, fs, "time_noisy_samples")
plot_frequency(samples, fs, "frequency_samples")
plot_frequency(noisy_samples, fs, "frequency_noisy_samples")
