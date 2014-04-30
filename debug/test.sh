#!/bin/bash

algos=( LRU MRU FIFO LFU )
CLIENTS=4

function testReadK() {
    CLIENT=$1
    SIZE=$2
    ALGO=$3
    TYPE=$4
    rm -rf /d${CLIENT}/*
    for i in `seq 1 $FILES`
    do
        dd if=/dev/urandom of=/d${CLIENT}_1/$i.test bs=${SIZE}k count=1 2> /dev/null || exit 1
    done
    
    for threads in 1 2 5 10 20
    do
        for j in $(seq 1 $TRIES)
        do
            if [[ $TYPE == rand ]]
                then
                    count=$RANDOM
                else
                    count=$j
            fi
            starttime=$(date +%s.%N)
            seq $threads | parallel -n0 cat "/d${CLIENT}_{#}/$(( count % FILES + 1 )).test" > testfile.test || exit 1
            echo "$(date +%s.%N) - $starttime" | bc >> result/$ALGO/$TYPE$threads*$TRIES*${SIZE}k.txt
        done
    done
}

function testReadM() {
    CLIENT=$1
    SIZE=$2
    ALGO=$3
    TYPE=$4
    rm -rf /d${CLIENT}/*
    for i in `seq 1 $FILES`
    do
        dd if=/dev/urandom of=/d${CLIENT}_1/$i.test bs=1M count=$SIZE 2> /dev/null || exit 1
    done
    
    for threads in 1 2 5 10 20
    do
        for j in $(seq 1 $TRIES)
        do
            if [[ $TYPE == rand ]]
                then
                    count=$RANDOM
                else
                    count=$j
            fi
            starttime=$(date +%s.%N)
            seq $threads | parallel -n0 cat "/d${CLIENT}_{#}/$(( count % FILES + 1 )).test" > testfile.test || exit 1
            echo "$(date +%s.%N) - $starttime" | bc >> result/$ALGO/$TYPE$threads*$TRIES*${SIZE}M.txt
        done
    done
}

for CLIENT in $(seq 1 $CLIENTS)
do
    ALGO=${algos[$((CLIENT - 1))]}
    rm -rf ./result/$ALGO
    mkdir -p ./result/$ALGO

    TRIES=1000
    FILES=$(( TRIES / 20))
    
    for SIZE in 10 100 200
    do
        testReadK $CLIENT $SIZE $ALGO rand
        testReadK $CLIENT $SIZE $ALGO seq
    done
    
    for SIZE in 1 10 40
    do
        testReadM $CLIENT $SIZE $ALGO rand
        testReadM $CLIENT $SIZE $ALGO seq
    done
done
