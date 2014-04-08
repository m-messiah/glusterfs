#!/bin/bash
cd ..
git reset --hard HEAD
git pull
./installation.sh
cd debug