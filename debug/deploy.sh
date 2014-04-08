#!/bin/bash
cd ..
git reset --hard HEAD
git pull
./installation.sh
cd debug
if [ `hostname` -eq "test1" ]
then
    ./server
else
    ./client1 &
fi