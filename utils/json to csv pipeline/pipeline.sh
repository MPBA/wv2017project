#!/bin/bash
for dir in */; do
	for file in "$dir"*.json; do
		python jsonsloth_to_csv.py "$dir"conv/ "$file" "${file/json/csv}";
		python join_csvs.py "$dir"conv/ "${file/json/csv}";
	done;
	echo "done" $dir
done;

