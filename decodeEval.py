"""
File decodes the test set and evaluates the results
"""

# Imports
import subprocess
import sys
import os

src = "es"
piv = "en"
tar = "cs"

direct = "direct"
pivot = "pivot"
combined = "combined"

# ------------------------------------------------------- #

def main():
    direct_decoded = decode(src, direct)
    #pivot_decoded = decode(src, pivot)
    #combined_decoded = decode(src, combined)
    
    evaluate(direct_decoded)
    #evaluate(pivot_decoded)
    #evaluate(combined_decoded)

# ------------------------------------------------------- #

def decode(source, method):
    filename = source + "-" + tar + "-test"
    if not fileExists(filename):
	print "Test file %s not found. Exiting" % (filename)
	return
    
    cdec_ini = source + "-" + method + ".ini"
    if not fileExists(cdec_ini):
	print "Ini file %s not found. Exiting" % (cdec_ini)
	return

    weights_final = source + "-" + method + "-mira/weights.final"
    if not fileExists(weights_final):
	print "Weights file %s not found. Exiting" % weights_final
	return    

    testset_decoded = source + "-" + method + ".decoded"
    if fileExists(testset_decoded):
	print "Decoded file %s already exists. Exiting" %(testset_decoded)  
	return  testset_decoded 

    print "Decoding test set...",
    sys.stdout.flush()
    command = "cat " + filename + " | /export/ws15-mt-data2/umandujano" + \
	      "/cdec/corpus/cut-corpus.pl 1 | " + \
	      "/export/ws15-mt-data2/umandujano/cdec/decoder/cdec -c " + \
	      cdec_ini + " -w " + weights_final + " > " + \
	      testset_decoded    

    subprocess.call(command, shell=True)
    print "Done"
    
    return testset_decoded

# ------------------------------------------------------- #

def evaluate(filename_decoded):
    filename = src + "-" + tar + "-test"
    makeRefs = "cat " + filename + " | /export/ws15-mt-data2/umandujano" + \
	       "/cdec/corpus/cut-corpus.pl 1 > " + \
	       "refs" 
    
    print "Making reference text",
    sys.stdout.flush()
    subprocess.call(makeRefs, shell=True)  
    print "Done"

    command = "/export/ws15-mt-data2/umandujano/multeval-0.5.1/multeval.sh eval " + \
	      "--refs refs --hyps-baseline " + \
	      filename_decoded + " --meteor.language cs"
    
    print command 
    print "Evaluating the decoded set...",
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
