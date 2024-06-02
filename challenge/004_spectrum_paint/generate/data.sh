#!/bin/sh

python3 -m spectrum_painter.img2iqstream -s 100000 -l 0.005 --format float \
-o /app/challenge/004_spectrum_paint/data/challenge_004.sigmf-data \
/app/challenge/004_spectrum_paint/generate/spectrum.png
