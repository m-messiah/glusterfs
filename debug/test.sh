#!/bin/bash

ALGO="LRU"
mkdir -p ./result/$ALGO

THREADS=1
TRIES=10000
FILES=$(( TRIES / 50))

for SIZE in 1 10 100 1k 4k 10k 100k 1M 10M 100M 1G 10G
do
	for i in `seq 1 $FILES`
	do
		dd if=/dev/urandom of=/d/$i.test bs=$SIZE count=1 2> /dev/null
	done
	
	for j in `seq 1 $TRIES`
	do
		starttime=`date +%s.%N`
		cat "/d/$(( RANDOM % FILES + 1 )).test" > testfile.test
		echo "$(date +%s.%N) - $starttime" | bc >> result/${ALGO}/$THREADS*$TRIES*${SIZE}.txt
	done;
done
