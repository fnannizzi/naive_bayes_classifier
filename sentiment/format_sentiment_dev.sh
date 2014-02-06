#! /bin/sh

for f in SENTIMENT_dev/*.txt
do
    cat $f | tr '\n\r' ' '
    echo
done > sentiment_dev.txt