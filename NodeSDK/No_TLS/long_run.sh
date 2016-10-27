#!/bin/bash
c=1
while [ $c -le 47 ]
do
    echo "Executing run $c"
    node invoke_query.js
	(( c++ ))
done
