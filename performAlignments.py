"""
Contains the procedure with which to create alignments using cdec

This should only be done on the training set
"""

# Imports
import os
import sys
import subprocess

src = "es"
piv = "en"
tar = "cs"

home = "/export/ws15-mt-data2/umandujano/"
data = home + "pract/data/"
dest = home + "pract/alignments/"

symm_heuristic = "grow-diag-final-and"

# ------------------------------------------------------- #

def main():
    align(src, tar)
    align(src,piv), align(piv, tar)    

# ------------------------------------------------------- #

def align(source, target):
    newfile = source + '-' + target + '-train'
    datafile = data + newfile  
    
    if not fileExists(datafile):
	print "Training data not found: " + filename + "... Exiting"
	sys.exit(-1)   
    if fileExists(dest + source + '-' + target + '.gdfa'):
	print "Alignment between " + source + " and " + target + \
	      " already exists. Exiting."
	return
  
    print "Aligning on " + newfile

    forward_name = dest + newfile + '-forward'
    forwardAlign(datafile, forward_name)

    backward_name = dest + newfile + '-backward'
    backwardAlign(datafile, backward_name)

    symm_name = dest + source + '-' + target + '.gdfa'
    symmetrize(forward_name, backward_name, symm_name)

    os.remove(forward_name), os.remove(backward_name)
    
# ------------------------------------------------------- #

def forwardAlign(filename, destination):
    print filename, destination
    command = home + "cdec/word-aligner/fast_align -i " + \
	      filename + " -d -v -o > " + destination

    print "Forward aligning...",
    sys.stdout.flush()
    subprocess.call(command, shell=True)
    print "Done"    

# ------------------------------------------------------- #

def backwardAlign(filename, destination):
    command = home + "cdec/word-aligner/fast_align -i " + \
	      filename + " -d -v -o -r > " + destination

    print "Backward aligning...",
    sys.stdout.flush()
    subprocess.call(command, shell=True)
    print "Done"

# ------------------------------------------------------- #

def symmetrize(forwardfile, backwardfile, destination):
    command = home + "cdec/utils/atools -i " + forwardfile + \
	      " -j " + backwardfile + " -c " + symm_heuristic + \
	      "> " + destination
    
    print "Symmetrizing forward and backward alignments...",
    sys.stdout.flush()
    subprocess.call(command, shell=True)    
    print "Done"

# ------------------------------------------------------- #

def fileExists(filename):
    if os.path.exists(filename):
	return True
    return False

# ------------------------------------------------------- #

main()
