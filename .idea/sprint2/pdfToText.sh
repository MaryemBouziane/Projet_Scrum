#!/bin/bash

	if [ ! -d "dossierText" ] 
		then
			$(mkdir dossierText/)
	fi
	for fich in $(ls dossierText)
	do
		rm dossierText/$fich
	done
	for fich in $(find -name "*.pdf")
	do
		$(pdftotext -raw -enc ASCII7 $fich)
	done
	for fich in $(find $1 -name "*.txt" | grep -oP '(?<=/)[^ ]*')
	do 
		mv $1/$fich dossierText	
	done
