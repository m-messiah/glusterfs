#!/bin/bash

algos=( LRU MRU FIFO LFU )
CLIENTS=3
for CLIENT in `seq 3 $CLIENTS`
do
    ALGO=${algos[$((CLIENT - 1))]}
    rm -rf ./result/$ALGO
    mkdir -p ./result/$ALGO

    TRIES=1000
    FILES=$(( TRIES / 20))
    
    for SIZE in 10 100 200
    do
    	rm -rf /d${CLIENT}_1/*
        for i in `seq 1 $FILES`
        do
        	dd if=/dev/urandom of=/d${CLIENT}_1/$i.test bs=${SIZE}k count=1 2> /dev/null || exit 1
        done
        
        for threads in 1 2 5
        do
            for j in `seq 1 $TRIES`
            do
                count=$RANDOM
            	starttime=`date +%s.%N`
            	seq $threads | parallel -n0 cat "/d${CLIENT}_{#}/$(( count % FILES + 1 )).test" > testfile.test || exit 1
            	echo "$(date +%s.%N) - $starttime" | bc >> result/${ALGO}/rand$threads*$TRIES*${SIZE}k.txt
            done
        done
 
    	rm -rf /d${CLIENT}_1/*
        for i in `seq 1 $FILES`
        do
        	dd if=/dev/urandom of=/d${CLIENT}_1/$i.test bs=${SIZE}k count=1 2> /dev/null || exit 1
       	done
 

        for threads in 1 2 5
        do        
           	for j in `seq 1 $TRIES`
           	do
           		starttime=`date +%s.%N`
           		seq $threads | parallel -n0 cat "/d${CLIENT}_{#}/$(( j % FILES + 1 )).test" > testfile.test || exit 1
           		echo "$(date +%s.%N) - $starttime" | bc >> result/${ALGO}/seq$threads*$TRIES*${SIZE}k.txt
        	done
        done
    done
    
    for SIZE in 10
    do
	rm -rf /d${CLIENT}_1/*
    	for i in `seq 1 $FILES`
    	do
    		dd if=/dev/urandom of=/d${CLIENT}_1/$i.test bs=1M count=$SIZE 2> /dev/null || exit 1
    	done
 
        for threads in 1 2 5
        do
            for j in `seq 1 $TRIES`
            do
                count=$RANDOM
            	starttime=`date +%s.%N`
            	seq $threads | parallel -n0 cat "/d${CLIENT}_{#}/$(( count % FILES + 1 )).test" > testfile.test || exit 1
            	echo "$(date +%s.%N) - $starttime" | bc >> result/${ALGO}/rand$threads*$TRIES*${SIZE}M.txt
            done
        done
    
	rm -rf /d${CLIENT}_1/*
    	for i in `seq 1 $FILES`
    	do
    		dd if=/dev/urandom of=/d${CLIENT}_1/$i.test bs=1M count=$SIZE 2> /dev/null || exit 1
    	done
 
        for threads in 1 2 5
        do        
           	for j in `seq 1 $TRIES`
           	do
           		starttime=`date +%s.%N`
           		seq $threads | parallel -n0 cat "/d${CLIENT}_{#}/$(( j % FILES + 1 )).test" > testfile.test || exit 1
           		echo "$(date +%s.%N) - $starttime" | bc >> result/${ALGO}/seq$threads*$TRIES*${SIZE}M.txt
        	done
        done
   
    done
done
