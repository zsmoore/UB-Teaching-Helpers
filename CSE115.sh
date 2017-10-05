#!/bin/bash

if (ps ax | grep -v grep | grep eclipse > /dev/null)
then
	echo "Please close eclipse."
        while (ps ax | grep -v grep | grep eclipse > /dev/null)
        do
		sleep .5
        done
fi

python3 /projects/CSE115/Repositories/Fall2017/UB-Teaching-Helpers/import_projects.py

eclipse &

exit
