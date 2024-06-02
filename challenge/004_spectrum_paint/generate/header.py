# Generate a SigMF header for spectrum_painter IQ data.

# Author: 30hours

import sigmf
from sigmf import SigMFFile

fs = 100000
fc = 0
datatype = 'cf32_le'

header_file = '/app/challenge/004_spectrum_paint/data/challenge_004.sigmf-meta'
header = SigMFFile(
    data_file='/app/challenge/004_spectrum_paint/data/challenge_004.sigmf-data',
    global_info = {
        SigMFFile.DATATYPE_KEY: datatype,
        SigMFFile.SAMPLE_RATE_KEY: fs,
        SigMFFile.NUM_CHANNELS_KEY: 1,
        SigMFFile.AUTHOR_KEY: 'nathan@30hours.dev',
        SigMFFile.DESCRIPTION_KEY: 'A signal with spectrum painting.',
        SigMFFile.LICENSE_KEY: 'MIT',
        SigMFFile.VERSION_KEY: sigmf.__specification__,
    }
)
header.add_capture(0, metadata={
    SigMFFile.FREQUENCY_KEY: fc,
})
header.tofile(header_file)
