#!/bin/bash

DATA_DIR=/Users/nickchen/Documents/ling/AudioData/*/*.wav
BIN_DIR=/Users/nickchen/Documents/ling/openSMILE-2.1.0/
openSMILE=$BIN_DIR/SMILExtract

for wave in $DATA_DIR
do
    wave_base=$(basename $wave)
    wave_dir=$(basename $(dirname $wave))
    wave_out="$wave_dir-$wave_base.csv"
    CMD="$openSMILE -C $BIN_DIR/config/prosodyAcf.conf -I $wave -O csv/$wave_out"
    echo $CMD
    `$CMD`
done
