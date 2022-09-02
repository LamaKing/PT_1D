#!/bin/bash
for i in 0.03 0.05 0.1 0.5; do echo $i ; ./loop_k.py $i 1 30 params-start.json; done
