#!/bin/bash
for number in $@
do
  let sum=$sum+$number
done
echo "mean $@ => $(($sum/$#))"