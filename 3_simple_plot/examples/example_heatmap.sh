#!/bin/sh

conda activate cdpy7
../simple_plot.heatmap.py \
  -in cblb_rgs_h.gamd.rms_cter.txt.bz2 cblb_rgs_h.gamd.rms_loop.txt.bz2 \
  -cols 2 2 -out cblb_rgs_h.gamd.cter_loop_hist2d.png \
  -xlab rms_cter -ylab rms_loop -bin 25 \
  -tick 9 -xlim 0 10 \
  -t_step 2 \
  -fract .95 \
  -ver 2.5 5 7.5 \
  -hor 0.75 1.25 2. \
  -col black 
