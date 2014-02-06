#! /bin/sh

for f in SPAM_test/*.txt
do
    cat $f | tr '\n\r' ' '
    echo
done > spam_test.txt