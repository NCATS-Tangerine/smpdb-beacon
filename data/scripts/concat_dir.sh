#!/bin/bash

# The command sed -e '$a\' $filename adds a newline at the end of the file

if [ "$3" = "header" ]; then
  echo "Using header"

  head -1 `(find "$1" -type f | head -1)` > "$2"

  for filename in "$1"/*
  do
    # 1d means delete first line, $a\ means add a new line at the end
    sed -e '1d; $a\' $filename >> "$2"
  done

elif [ "$3" = "noheader" ]; then
  echo "Concatenating full files"
  echo '' > "$2"
  for filename in "$1"/*
  do
    sed -e '$a\' $filename >> "$2"
  done

else
  echo "usage: directory_path output_path [header|noheader]"
  exit
fi
