#!/bin/bash

for i in `ls` ; do
	pushd $i
	python ../../test_files/verify_json.py
	for d in `cat files_with_invalid_json.txt` ; do
		rm $d
	done
	popd
done

