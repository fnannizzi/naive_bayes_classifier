#! /bin/sh

for f in SENTIMENT_training/NEG.*.txt
do
    echo -n "NEG "
    cat $f | tr '\n\r' ' '
    echo
done > allNEG.txt

for f in SENTIMENT_training/POS.*.txt
do
    echo -n "POS "
    cat $f | tr '\n\r' ' '
    echo
done > allPOS.txt