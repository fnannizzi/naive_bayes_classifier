#! /bin/sh

for f in SPAM_dev/*
do
    filename=${f##*/}
    filename=${filename%.*}
    echo ${filename%.*}
done > filenames.txt