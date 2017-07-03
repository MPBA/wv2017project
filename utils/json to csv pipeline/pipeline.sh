for dir in */; do
	python jsonsloth_to_csv.py "$dir"conv/ "$dir"annotation.json "$dir"annotations.csv;
	python join_csvs.py "$dir"conv/ "$dir"annotations.csv;
	echo done $dir
done;

