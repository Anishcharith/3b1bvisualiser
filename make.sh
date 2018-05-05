#!/bin/bash

#if [ $# -lt 1 ]; then
#  echo "You must supply a mono-mixed wave file as the first argument."
#  exit 1
#fi

#[[ -w frame_*.png ]] && rm frame_*.png

#./plotvals.py $1

filename=$1
extension="${filename##*.}"
filename="${filename%.*}"
echo $filename
ffmpeg -framerate 24 -i samples/$filename/frame_%05d.jpg -i audio_input/$1 ${WAVFILE/wav/mp4} -vcodec mpeg4 video_output/$filename.mp4 
#rm -r frame_*
