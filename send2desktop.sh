#! /usr/bin/bash
echo "enter filename"
read file
filepath=/mnt/c/Users/willi/oneDrive/Desktop/FromLinux
echo copying $file to $filepath
cp $file $filepath
