"""
This creates a language model between the source and target languages
for use in the cdec decoder
"""

# Imports
import os
import sys
import subprocess

src = "es"
piv = "en"
tar = "cs"

order = 3

# ------------------------------------------------------- #

def main():
    makeModel(src,tar)

# ------------------------------------------------------- #

def makeModel(source_lang, tar_lang):
    
    train_file = source_lang + '-' + tar_lang + '-train'
    lang_model_file = source_lang + '-' + tar_lang + '.lm'
    bin_lang_model = source_lang + '-' + tar_lang + '.klm'
     
    if fileExists(bin_lang_model):
	print "Language model file already exists. Exiting"
	sys.exit(-1)
    if not fileExists(train_file):
	print "Training file not found. Exiting"
	sys.exit(-1)

    command = "~/cdec/corpus/cut-corpus.pl 2 " + train_file + \
	      " | ~/cdec/klm/lm/builder/lmplz --order " + str(order) + \
	      " > " + lang_model_file

    print "Building language model file...",
    sys.stdout.flush()
    subprocess.call(command, shell=True)
    print "Done"

    print "Building binary language model file...",
    sys.stdout.flush()
    buildBinary(lang_model_file, bin_lang_model)
    print "Done"

# ------------------------------------------------------- #

def buildBinary(lang_model_file, bin_lang_model):
    command = "~/cdec/klm/lm/build_binary " + lang_model_file + " " + \
	      bin_lang_model
    subprocess.call(command, shell=True)
    os.remove(lang_model_file)

# ------------------------------------------------------- #

def fileExists(filename):
    if os.path.exists(filename):
	return True
    return False

# ------------------------------------------------------- #

main()
