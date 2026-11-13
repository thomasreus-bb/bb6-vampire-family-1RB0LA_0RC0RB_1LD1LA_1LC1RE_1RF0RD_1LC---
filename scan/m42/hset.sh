#!/bin/bash
# halting e values of M(2,e) for e in [$1,$2)
for ((e=$1;e<$2;e++)); do echo "M 2 $e"; done | ./ev42 | awk -v s=$1 '{print s+NR-1, $0}' > h_$1_$2.txt
