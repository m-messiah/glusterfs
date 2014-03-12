#!/bin/bash

ALGO="MRU"
mkdir -p ./result/$ALGO

THREADS=1
TRIES=1000
FILES=$(( TRIES / 40))

for SIZE in 1k 10k 100k 1M
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

for SIZE in 10 40 80 100 1024
do
	for i in `seq 1 $FILES`
	do
		dd if=/dev/urandom of=/d/$i.test bs=1M count=$SIZE 2> /dev/null
	done
	
	for j in `seq 1 $TRIES`
	do
		starttime=`date +%s.%N`
		cat "/d/$(( RANDOM % FILES + 1 )).test" > testfile.test
		echo "$(date +%s.%N) - $starttime" | bc >> result/${ALGO}/$THREADS*$TRIES*${SIZE}M.txt
	done;
done
