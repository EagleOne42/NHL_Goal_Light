#!/bin/bash

echo "This will delete files in the current folder that do not have valid json"
echo "This shouldn't be needed to run the script much longer - close to getting proper error detection"
echo "Will continue in 10 seconds"
sleep 10

for i in `ls` ; do
	pushd $i
	python ../../test_files/verify_json.py
	for d in `cat files_with_invalid_json.txt` ; do
		rm $d
	done
	popd
done

