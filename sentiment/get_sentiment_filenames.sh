#! /bin/sh

for f in SENTIMENT_dev/*
do
    filename=${f##*/}
    filename=${filename%.*}
    echo ${filename%.*}
done > sentiment_filenames.txt