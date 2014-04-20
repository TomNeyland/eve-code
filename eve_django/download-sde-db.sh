#!/bin/bash
FILE_URL=$1
OUT_FILE=$2
: ${FILE_URL:="https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2"}
: ${OUT_FILE:="eve.db"}
echo "Downloading $FILE_URL to $OUT_FILE with command:"
echo "wget -q $FILE_URL -O - | bzip2 -cd > $OUT_FILE"
wget -q $FILE_URL -O - | bzip2 -cd > $OUT_FILE
