#! /bin/sh

for f in SPAM_dev/*.txt
do
    cat $f | tr '\n\r' ' '
    echo
done > spam_dev.txt