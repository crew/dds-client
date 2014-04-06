#!/bin/sh

echo "Running Script"
echo $1
echo $2

xvfb-run --server-args="-screen 0, 1280x1024x24" cutycapt --url=$1 --out=$2
echo "Done"
#fbi $2
