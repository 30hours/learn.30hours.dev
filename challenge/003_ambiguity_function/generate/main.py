# Create a transmit and receive radar signal with 1 target.

# Author: 30hours

import numpy as np
from sigmf import SigMFFile
from sigmf.utils import get_data_type_str

np.random.seed(0)

# waveform params
fs = 1000000
fc = 300000000
T = 0.1
N = int(fs*T)
t = np.arange(N)/fs

# create transmit waveform as noise
xi = np.random.uniform(-1, 1, N)
xq = np.random.uniform(-1, 1, N)
x = xi + 1j * xq

# target params
delay = 63
doppler = 41

# create receive target waveform
yt = np.roll(x, delay)
yt = yt * np.exp(1j*2*np.pi*doppler*t)

# create receive noise waveform
yn = np.random.uniform(-1, 1, N)

# create receive waveform
y = yn + 0.1*yt

# save IQ to file
iq_data = np.stack((x.real, x.imag, y.real, y.imag), axis=1).ravel()
data_file = '/app/challenge/003_ambiguity_function/data/challenge.sigmf-data'
iq_data.tofile(data_file)

# write IQ header
header_file = '/app/challenge/003_ambiguity_function/data/challenge.sigmf-meta'
header = SigMFFile(
    data_file=data_file,
    global_info = {
        SigMFFile.DATATYPE_KEY: get_data_type_str(iq_data),
        SigMFFile.SAMPLE_RATE_KEY: fs,
        SigMFFile.NUM_CHANNELS_KEY: 2,
        SigMFFile.AUTHOR_KEY: 'nathan@30hours.dev',
        SigMFFile.DESCRIPTION_KEY: 'A radar transmit and receive waveform with 1 target.',
        SigMFFile.LICENSE_KEY: 'MIT',
        SigMFFile.VERSION_KEY: '1.0.0',
    }
)
header.add_capture(0, metadata={
    SigMFFile.FREQUENCY_KEY: fc,
})
header.tofile(header_file)
