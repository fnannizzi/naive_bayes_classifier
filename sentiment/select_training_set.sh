#! /bin/sh

for f in SENTIMENT_training/* 
do
  val=$RANDOM
  if test $val -gt 3276; then
    mv "$f" ./SENTIMENT_dev
  fi
done