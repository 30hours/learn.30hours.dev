name: Noisy FM
category: audio
tag: fm, filter-design
value: 10

---

An FM radio signal is provided. Demodulate it and listen to the audio. It sounds a bit noisy though? Remove the noise to listen to the flag. Read the header file to get the IQ data sampling frequency. Plot the signal in the frequency domain to see the noise after demodulating.

The IQ data is in the SigMF format, which is interleaved float64 bit I and Q samples. Read the SigMF docs or use the following Python example:

```
import numpy as np

def load_iq_data(iq_file_path):
    interleaved_data = np.fromfile(iq_file_path, dtype=np.float64)
    I = interleaved_data[0::2]
    Q = interleaved_data[1::2]
    iq_data = I + 1j * Q
    return iq_data
```

