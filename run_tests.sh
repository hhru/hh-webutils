#!/bin/sh

python setup.py test

if [ "$?" -ne "0" ]
then
    echo "Tests failed!"
    exit 1
fi
