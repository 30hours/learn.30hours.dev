# Read SigMF file and plot a spectrogram.

# Author: 30hours

# Not sure why I can't get scipy spectrogram to give a 2 sided image.
# Implementation from first principles works fine.

import numpy as np
from numpy.fft import fftshift
from scipy import signal
from scipy.signal import ShortTimeFFT
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
import sigmf
from sigmf import sigmffile

# sigmf files
datapath = '/app/challenge/004_spectrum_paint/data/'
solvepath = '/app/challenge/004_spectrum_paint/solve/'
sigmf_file_path = datapath + 'challenge_004.sigmf-data'
sigmf_meta_path = datapath + 'challenge_004.sigmf-meta'

# load the sigmf metadata
handle = sigmf.sigmffile.fromfile(sigmf_meta_path)
global_info = handle.get_global_info()
fs = global_info['core:sample_rate']

# load the sigmf binary data
data = handle.read_samples()
I = data[0::2]
Q = data[1::2]
iq_data = I + 1j * Q

# generate the spectrogram with scipy
n = int(0.05 * fs)
f, t, Sxx = spectrogram(iq_data, fs=fs, nperseg=n, return_onesided=False, scaling='spectrum')
Sxx_dB = 10 * np.log10(Sxx)
max_value = np.max(Sxx_dB)

# plot spectrogram
plt.figure(figsize=(10, 6))
plt.pcolormesh(f, t, Sxx_dB.T, vmin=max_value-40, vmax=max_value, cmap='viridis')
plt.colorbar(label='Intensity (dB)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Time (s)')
plt.title('Spectrogram')
plt.savefig(solvepath + 'spectrogram_scipy.png')
plt.close()

# generate spectrogram manually
num_rows = len(iq_data) // n
iq_matrix = iq_data[:num_rows * n]
iq_matrix = iq_matrix.reshape((num_rows, n))
iq_matrix = np.fft.fft(iq_matrix, axis=1)
iq_matrix = np.fft.fftshift(iq_matrix, axes=1)
iq_matrix = np.flipud(iq_matrix)
iq_matrix_mag = 10*np.log10(np.abs(iq_matrix))

# plot spectrogram
plt.figure(figsize=(10, 6))
plt.imshow(iq_matrix_mag, aspect='auto', cmap='viridis', extent=[0, n, 0, num_rows])
plt.colorbar(label='Magnitude (dB)')
plt.xlabel('Frequency (bins)')
plt.ylabel('Time (bins)')
plt.title('Spectrogram')
plt.savefig(solvepath + 'spectrogram.png')
plt.close()
