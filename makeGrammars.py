"""
This file extracts grammars with which to evaluate the dev and test set

NOTE: MUST BE SUBMITTED AS A JOB
"""

# Import
import os
import sys
import subprocess

src = 'es'
piv = 'en'
tar = 'cs'

devmode  = "dev"
testmode = "test"

CPU = 16

# ------------------------------------------------------- #

def main():
    makeGrammar(src, tar, devmode), makeGrammar(src, tar, testmode)
    makeGrammar(src, piv, devmode), makeGrammar(src, piv, testmode)
    makeGrammar(piv, tar, devmode), makeGrammar(piv, tar, testmode)

# ------------------------------------------------------- #

def makeGrammar(src_lang, tar_lang, mode):
    grammar_name = src_lang + '-' + tar_lang + '-' + mode + '.grammar'
    data_name    = src_lang + '-' + tar_lang + '-' + mode
    extract_name = src_lang + '-' + tar_lang + '-extract_sa.ini'
    destination  = src_lang + '-' + tar_lang + '-' + mode + '.sgm'

    if fileExists(grammar_name) and fileExists(destination):
	print "Grammar " + grammar_name + " already exists. And ",
	print destination + " already exists. Exiting"
	return
    if not fileExists(data_name):
	print "Data file " + data_name + " not found. Exiting"
	exit()
    if not fileExists(extract_name):
	print "Extractiong info file " + extract_name + " not found. Exiting"
	exit()

    command = "~/cdec/extractor/extract -c " + extract_name + " -g " + \
		grammar_name + " -t " + str(CPU) + " -z < " + data_name + \
		" > " + destination
    
    print "Extracting grammar " + grammar_name,
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
