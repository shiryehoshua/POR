#!/bin/bash

# wrapper function for the POR compiler
if [ "$#" -eq 1 ]; then
	# $1 is the directory of the thread files
	python compiler.py -d $1 | python
fi
