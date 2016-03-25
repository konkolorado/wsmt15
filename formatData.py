"""
Align sentences in the EuroParl data, tokenizes, and filters lengths.
Necessary for alignments.
"""

# Imports
import os
import sys
import gzip
import codecs
import subprocess

sys.path.append('/export/ws15-mt-data2/umandujano/prefix/lib/python2.7/site-packages')
import nltk.data

location = "/export/ws15-mt-data2/umandujano/pract/"
data = "/export/ws15-mt-data/data/europarl/txt/"
src  = "es"
tar  = "cs"
piv  = "en"

num_train = 1000
num_dev   = 75
num_test  = 75

trainmode = "train"
devmode   = "dev"
testmode  = "test"

# ------------------------------------------------------- #

def main():
    assert fileExists(data+src), fileExists(data+tar)
    
    createData(src, tar, trainmode)
    createData(src, piv, trainmode)
    createData(piv, tar, trainmode)
    
    createData(src, tar, devmode)
    createData(src, piv, devmode)
    createData(piv, tar, devmode)

    createData(src, tar, testmode)
    createData(src, piv, testmode)
    createData(piv, tar, testmode)

# ------------------------------------------------------- #

def createData(source_data, target_data, curr_mode):
    """
    Retrieves filenames necessary to perform the direct triangulation
    """
    train, dev, test = getFiles(source_data, target_data)

    datafile = location + "data/" + source_data + "-" + target_data + "-" + curr_mode
    
    if not fileExists(datafile):
	print "No pre-existing data file found: " + datafile
	if curr_mode == "train":
	    makeData(train, datafile, source_data, target_data)
	elif curr_mode == "test":
	    makeData(test, datafile, source_data, target_data)
	elif curr_mode == "dev":
	    makeData(dev, datafile, source_data, target_data)
	else:
	    print "Mode not found. Must be {train, dev, test}"
    else:
	print "Nothing to do. " + datafile + " already exists." 


# ------------------------------------------------------- #

def makeData(files, datafile, source, target):
    """# {{{
    Gets files in list 'files' and puts them into proper cdec format in datafile
    """
    print "Creating data file...", 
    sys.stdout.flush()    

    temp  = "temp"
    temp2 = "temp2"
    all_data = codecs.open(temp, 'w', encoding='utf8')

    sent_detector = nltk.data.load('/export/ws15-mt-data2/umandujano/nltk_data/tokenizers/punkt/english.pickle')	
    
    
    for filename in files:
	file1 = open(data + source + '/' + filename, 'r')
	file2 = open(data + target + '/' + filename, 'r')
	
	for src_sent, tar_sent in zip(file1, file2):
	    if src_sent[0] != '<' and tar_sent[0] != '<':
		if src_sent.strip() != "" and tar_sent.strip() != "":
				    
		    src_sents_aligned = \
			sent_detector.tokenize(src_sent.strip().decode('utf8'))
		    tar_sents_aligned = \
			sent_detector.tokenize(tar_sent.strip().decode('utf8'))
		    
		    if len(src_sents_aligned) == len(tar_sents_aligned):	
			for s in range(len(src_sents_aligned)):
			    exam = src_sents_aligned[s] + " ||| " + \
				   tar_sents_aligned[s] + '\n'
		    	    all_data.write(exam)
		    else:
			all_data.write(''.join(src_sents_aligned) + " ||| " + \
				       ''.join(tar_sents_aligned) + "\n")
	
	file1.close, file2.close()
    
    print "Done"
    all_data.close()
    
    print "Tokenizing...",
    sys.stdout.flush()
    tokenize(temp, temp2)
    print "Done"
    
    print "Filtering length...", 
    sys.stdout.flush()
    filterLength(temp2, datafile)
    print "Done"
    
    os.remove(temp), os.remove(temp2)
    #}}}

# ------------------------------------------------------- #

def tokenize(datafilename, final_data_name):
    """#{{{
    Tokenizes the data if it has not already been tokenized
    """

    command = "/export/ws15-mt-data2/umandujano/cdec/corpus/tokenize-anything.sh < " + datafilename + \
	      " | ~/cdec/corpus/lowercase.pl > " + final_data_name
    subprocess.call(command, shell=True)#}}}

# ------------------------------------------------------- #

def filterLength(tempFile, resultFile):
    length = 80
    command = "/export/ws15-mt-data2/umandujano/cdec/corpus/filter-length.pl -" + str(length) + " " + tempFile + \
	      " > " + resultFile
    subprocess.call(command, shell=True)

# ------------------------------------------------------- #

def getFiles(langA, langB):
    """#{{{
    Retrieves filenames between language A and language B and divides it 
    into the training set, dev set, test set. Returns the sets
    """
    src_files = os.listdir(data+langA)
    tar_files = os.listdir(data+langB)
    all_files = list(set(src_files).intersection(tar_files))
    
    train = all_files[ 0 : num_train ]
    dev   = all_files[ num_train : num_train + num_dev]
    test  = all_files[ num_train + num_dev: num_train + num_dev + num_test ]
 
    assert len(train) == num_train, "not enough training data available"
    assert len(dev)   == num_dev,   "not enough dev data available"
    assert len(test)  == num_test,  "not enough test data available"

    return train, dev, test
    #}}}

# ------------------------------------------------------- #

def fileExists(filename):
    if os.path.exists(filename):
	return True
    return  False

# ------------------------------------------------------- #

main()
