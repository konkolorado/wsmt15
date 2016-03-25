"""
Extract grammars between the language pairs. Also extracts a vocabulary.

! This should only be called on grammars in the dev set
! Takes lots of memory - submit a job on it
"""

# Imports
import os
import sys
import gzip
import pickle

src = 'es'
piv = 'en'
tar = 'cs'

train = 'train'
dev   = 'dev'
test  = 'test'

# ------------------------------------------------------- #
def main():

    vocab_dir = getGrammars(src, tar, dev)
    vocab_piv = getGrammars(src, piv, dev)
    getGrammars(piv, tar, dev)

    makeVocab(vocab_dir, vocab_piv)

# ------------------------------------------------------- #

def getGrammars(source_lang, tar_lang, mode):
    filelocation = source_lang + '-' + tar_lang + '-' + mode + '.grammar'
    if not fileExists(filelocation):
	print "Grammar file " + filelocation + " does not exists. Exiting."
	return
    filedump = filelocation + 's.pkl'
    if fileExists(filedump):
	print "Grammar dump file " + filedump + " already exists. Exiting"
	return 

    print "Extracting data from: " + filelocation
    extractions = extract(filelocation) 
    print "Done"

    print "Dumping data...",
    sys.stdout.flush()
    dumpData(extractions, filedump)
    print "Done"

    return extractions.keys()

# ------------------------------------------------------- #

def extract(filelocation):
    files = os.listdir(filelocation)    
    files.sort()
    extractions = {}
    
    for f in files:
	if not f.endswith('.gz'):
	    continue
	
	print "Opening " + f
	instream = gzip.open(filelocation + '/' + str(f), 'rb')
	
	for line in instream:
	    features = line[:]
	    
	    line = line.strip().split('|||')
	    source, target = line[1], line[2]

	    if source not in extractions:
		extractions[source] = {}
	    if target not in extractions[source]:
		extractions[source][target] = features
	instream.close()

    return extractions

# ------------------------------------------------------- #

def dumpData(extractions, filename):
    outstream = open(filename, 'wb')
    pickle.dump(extractions, outstream)
    outstream.close()
    
# ------------------------------------------------------- #

def makeVocab(vocab_dir, vocab_piv):
    # NOT WORKING -- Possibly due to a timing mismatch with the 
    #		     pickle dump
    vocab = src + "-vocab.txt"
    if fileExists(vocab):
	print "Vocab file " + vocab + " already exists. Exiting"
	return  
    
    outstream = open(vocab, 'w')
    
    print "Making " + src + " vocab...",
    for i in vocab_dir:
	outstream.write(i + '\n')
    for i in vocab_piv:
	outstream.write(i + '\n')
    
    print "Done"
    outstream.close()    

# ------------------------------------------------------- #

def fileExists(filename):
    if os.path.exists(filename):
	return True
    return False
        
# ------------------------------------------------------- #

main()
