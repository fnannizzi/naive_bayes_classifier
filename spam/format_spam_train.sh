#! /bin/sh

for f in SPAM_training/HAM.*.txt
do
    echo -n "HAM "
    cat $f | tr '\n\r' ' '
    echo
done > allHAM.txt

for f in SPAM_training/SPAM.*.txt
do
    echo -n "SPAM "
    cat $f | tr '\n\r' ' '
    echo
done > allSPAM.txt