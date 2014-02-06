#! /bin/sh

for f in SENTIMENT_test/*.txt
do
    cat $f | tr '\n\r' ' '
    echo
done > sentiment_test.txt