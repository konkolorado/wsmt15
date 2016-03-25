"""
This file creates a suffix array using processed data and it's symmetrized
aligments
"""

# Imports
import os
import sys
import subprocess

src = "es"
piv = "en"
tar = "cs"

symm_heuristic = "grow-diag-final-and"

# ------------------------------------------------------- #

def main():
    createArray(src, tar)    
    createArray(src, piv)
    createArray(piv, tar)    

# ------------------------------------------------------- #

def createArray(source_lang, target_lang):
    if symm_heuristic ==  "grow-diag-final-and":
	ext = ".gdfa"
    else:
	print "Unrecognized symmetrization metric. Exiting."
	exit()	

    train_file   = source_lang + '-' + target_lang + '-' + 'train'
    aligned_file = source_lang + '-' + target_lang + ext
    extract_file = source_lang + '-' + target_lang + '-' + 'extract_sa.ini'
    destination  = source_lang + '-' + target_lang + '.sa'
    
    if fileExists(destination):
	print "Suffix array " + destination + " already available. Exiting"
	return   
    if not fileExists(train_file):
	print "No training data found. Exiting"
	exit()
    if not fileExists(aligned_file):
	print "No alignment data was found. Exiting"
	exit()
    
    command = "~/cdec/extractor/sacompile -b " + train_file + " -a " + \
	      aligned_file + " -c " + extract_file + " -o " + destination
    
    print "Creating suffix array...",
    sys.stdout.flush()
    subprocess.call(command, shell=True)
    print "Done"

# ------------------------------------------------------- #

def fileExists(filename):
    if os.path.exists(filename):
	return True
    return False

# ------------------------------------------------------- #

def exit():
    sys.exit(-1)

# ------------------------------------------------------- #

main()
