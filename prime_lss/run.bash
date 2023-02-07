#!/bin/bash

split -l 10000 mergedURLs.txt

mkdir splits json
mv x* splits/

for i in $(ls splits); do mkdir json/$i; done

for i in $(ls splits); do python resolver.py -i splits/$i -d json; done
