#!/bin/bash

rootdir="/home/ross/Dropbox/work/intense_A"

pngdir=$rootdir"/png/"
outdir=$rootdir"/outputs/"
dirlist=$outdir"directory.txt"
ignlist=$outdir"web_ignore.txt"





for arg in $(comm -23 <(less $dirlist | sort) <(less $ignlist | sort)) 
do
    sav=${arg:0:-4}".png"
    python ./csv_utilities/plotter.py --data_0=$outdir$arg --output_png="./png_dir/"$sav  
done
