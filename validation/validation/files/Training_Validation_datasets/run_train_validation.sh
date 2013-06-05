#!/bin/bash

./get_text.sh training
cut -d' ' -f1,3- training.txt | sort -R > temp.txt
rm training.txt
mv temp.txt training.txt

./get_text.sh validation
cut -d' ' -f1,3- validation.txt | sort -R > temp.txt
rm validation.txt
mv temp.txt validation.txt

