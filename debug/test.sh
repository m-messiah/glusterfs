#!/bin/bash

algos=( LRU MRU FIFO LFU )
CLIENTS=1
THREADS=1 
for CLIENT in `seq 1 $CLIENTS`
do
    ALGO=${algos[$((CLIENT - 1))]}
    rm -rf ./result/$ALGO
    mkdir -p ./result/$ALGO

    TRIES=1000
    FILES=$(( TRIES / 20))
    
    for SIZE in 10 100 200
    do
    	for i in `seq 1 $FILES`
    	do
    		dd if=/dev/urandom of=/d${CLIENT}/$i.test bs=${SIZE}k count=1 2> /dev/null
    	done
    	
    	for j in `seq 1 $TRIES`
    	do
    		starttime=`date +%s.%N`
    		cat "/d${CLIENT}/$(( RANDOM % FILES + 1 )).test" > testfile.test
    		echo "$(date +%s.%N) - $starttime" | bc >> result/${ALGO}/rand$THREADS*$TRIES*${SIZE}k.txt
    	done
    
    	for i in `seq 1 $FILES`
    	do
    		dd if=/dev/urandom of=/d${CLIENT}/$i.test bs=${SIZE}k count=1 2> /dev/null
    	done
    
    	for j in `seq 1 $TRIES`
    	do
    		starttime=`date +%s.%N`
    		cat "/d${CLIENT}/$(( j % FILES + 1 )).test" > testfile.test
    		echo "$(date +%s.%N) - $starttime" | bc >> result/${ALGO}/seq$THREADS*$TRIES*${SIZE}k.txt
    	done
    done
    
    for SIZE in 1 10 40
    do
    	for i in `seq 1 $FILES`
    	do
    		dd if=/dev/urandom of=/d${CLIENT}/$i.test bs=1M count=$SIZE 2> /dev/null
    	done
    	
    	for j in `seq 1 $TRIES`
    	do
    		starttime=`date +%s.%N`
    		cat "/d${CLIENT}/$(( RANDOM % FILES + 1 )).test" > testfile.test
    		echo "$(date +%s.%N) - $starttime" | bc >> result/${ALGO}/rand$THREADS*$TRIES*${SIZE}M.txt
    	done
    
    	for i in `seq 1 $FILES`
    	do
    		dd if=/dev/urandom of=/d${CLIENT}/$i.test bs=1M count=$SIZE 2> /dev/null
    	done
    
    	for j in `seq 1 $TRIES`
    	do
    		starttime=`date +%s.%N`
    		cat "/d${CLIENT}/$(( j % FILES + 1 )).test" > testfile.test
    		echo "$(date +%s.%N) - $starttime" | bc >> result/${ALGO}/seq$THREADS*$TRIES*${SIZE}M.txt
    	done
    done
done
