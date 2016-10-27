#!/bin/bash
c=1
while [ $c -le 5000 ]
do
    echo "Executing run $c"
    node invoke3_query2.js
	(( c++ ))
done