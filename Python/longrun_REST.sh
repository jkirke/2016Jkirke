#!/bin/bash
c=1
while [ $c -le 1000 ]
do
    echo "Executing run $c"
    python3 longrun.py
        (( c++ ))
done