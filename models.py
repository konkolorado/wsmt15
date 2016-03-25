"""
This file combines the phrase tables into a new one.
Direct phrase table, pivot phrase table, combined phrase table
"""

# Imports
import cPickle as pickle
import gzip
import sys
import os
 
src = "es"
piv = "en"
tar = "cs"

# ------------------------------------------------------- #

def main():
    direct = loadData(src, tar) 
    first_piv = loadData(src, piv)
    second_piv = loadData(piv, tar)
    
    vocab = loadVocab(src, direct, first_piv) 
    
    doDirect(direct, vocab)
    doPivot(first_piv, second_piv, vocab)
    doCombined(direct, first_piv, second_piv, vocab)    

# ------------------------------------------------------- #

def doDirect(direct, vocab):
    """
    Get the extractions directly from es-cs data
    """
    filename = src + '-direct-grammar.txt.gz'
    if fileExists(filename):
	print "Direct extractions file %s found. Exiting" % (filename)
	return
    
    print "Extracting the direct grammer...",
    outstream = gzip.open(filename, 'wb')
    
    miss = 0
    for word in vocab:
	word = word.strip('\n')
	
	if word in direct:
	    all_translations = direct[word].keys()
	    for trans in all_translations:
		features = direct[word][trans]
		outstream.write(features)
	else:
	    miss += 1	

    outstream.close()
    print "Done"

# ------------------------------------------------------- #

def doPivot(first_piv, second_piv, vocab):
    """
    Get the extractions only from the pivot technique
    """
    filename = src + '-pivot-grammar.txt.gz'
    if fileExists(filename):
	print "Pivot extractions file %s found. Exiting" % (filename)
	return

    print "Extracting the pivot grammar...",
    outstream = gzip.open(filename, 'wb')

    miss = 0
    for word in vocab:
	word = word.strip('\n')
    
	# Lookup in first half of pivot table
	if word in first_piv:
	    first_piv_trans = first_piv[word].keys()
	    for trans in first_piv_trans:
		first_features = first_piv[word][trans]
		
		# Lookup in second half of pivot table
		if trans in second_piv:
		    second_piv_trans = second_piv[trans].keys()
		    for sec_trans in second_piv_trans:
			second_features = second_piv[trans][sec_trans]
			    
		        combo = combineFeatures(first_features, second_features)
			outstream.write(" " + combo + '\n')

		else:
		    miss += 1		
	else:
	    miss += 1

    outstream.close()
    print "Done"


# ------------------------------------------------------- #

def doCombined(direct, first_piv, second_piv, vocab):
    """
    Some combination of phrase table
    """
    filename = src + '-combined-grammar.txt.gz'
    if fileExists(filename):
	print "Combined extractions file %s found. Exiting" % (filename)
	return
    
    print "Extracting combined grammars..."
    outstream = gzip.open(filename, 'wb')
    
    miss = 0 
    for word in vocab:
	word = word.strip('\n')

	# Lookup in direct extractions
	if word in direct:
	    all_translations = direct[word].keys()
	    for trans in all_translations:
		features = direct[word][trans]
		outstream.write(features)
	
	# Lookup in pivot extractions 
	if word in first_piv:
	    first_piv_trans = first_piv[word].keys()
	    for trans in first_piv_trans:
		first_features = first_piv[word][trans]
		
		# Lookup in second half of pivot table
		if trans in second_piv:
		    second_piv_trans = second_piv[trans].keys()
		    for sec_trans in second_piv_trans:
			second_features = second_piv[trans][sec_trans]
			    
		        combo = combineFeatures(first_features, second_features)
			outstream.write(combo + '\n')

		else:
		    miss += 1		
	else:
	    miss += 1    

    outstream.close()
    print "Done"

# ------------------------------------------------------- #

def combineFeatures(first, second):
    # Features are in the CDEC form
    first, second = ''.join(first), ''.join(second)
    first, second = first.split('|||'), second.split('|||')
    
    comb_feat = []
    comb_feat.append(first[0]), comb_feat.append(first[1])
    comb_feat.append(second[2])

    tempFirst, tempSecond = first[3:4], second[3:4]
    
    tempFirst  = ' '.join(tempFirst).strip()
    tempSecond = ' '.join(tempSecond).strip()

    tempFirst  = tempFirst.split('=')
    tempSecond = tempSecond.split('=')

    tempFirst  = ' '.join(tempFirst).split(' ')
    tempSecond = ' '.join(tempSecond).split(' ')

    EGFC1,  EGFC2  = tempFirst[1],  tempSecond[1]
    SCF1,   SCF2   = tempFirst[3],  tempSecond[3]
    CEF1,   CEF2   = tempFirst[5],  tempSecond[5]
    MLFGE1, MLFGE2 = tempFirst[7],  tempSecond[7]
    MLEGF1, MLEGF2 = tempFirst[9],  tempSecond[9]
    ISF1,   ISF2   = tempFirst[11], tempSecond[11]
    ISFE1,  ISFE2  = tempFirst[13], tempSecond[13]

    EGFC  = str( float(EGFC1)  + float(EGFC2)  )
    SCF   = str( float(SCF1)   + float(SCF2)   )
    CEF   = str( float(CEF1)   + float(CEF2)   )
    MLFGE = str( float(MLFGE1) + float(MLFGE2) )
    MLEGF = str( float(MLEGF1) + float(MLEGF2) )
    ISF   = str( float(ISF1)  and float(ISF2)  )
    ISFE  = str( float(ISFE1) and float(ISFE2) )
    new_values = " EgivenFCoherent=" + str(EGFC) + " SampleCountF=" + \
		 str(SCF) + " CountEF=" +str(CEF) + " MaxLexFGivenE=" + \
		 str(MLFGE) + " MaxLexEgivenF=" + str(MLEGF) + \
		 " IsSingletonF=" + str(ISF) + " IsSingletonFE=" + \
		 str(ISFE) + " "
    
    comb_feat.append(new_values)
    
    anded_alignments = andAlign(first[4], second[4]) 
    comb_feat.append(anded_alignments)

    return '|||'.join(comb_feat) # TODO make sure the features formatted right

# ------------------------------------------------------- #

def andAlign(first, second):
    first, second = first.split(), second.split()
    alignment = ""

    for f in first:
	for s in second:
	    tempF = f.split('-')
	    tempS = s.split('-')
	    if tempF[1] == tempS[0]:
		align = tempF[0] + '-' + tempS[1] + ' '
		alignment += align

    return alignment.strip()

# ------------------------------------------------------- #

def loadVocab(language, vocab_direct, vocab_piv):
    filename  = language + '-vocab.txt' 
    if not fileExists(filename):
	print "Vocab file %s not found. Making..." % (filename)
	makeVocab(filename, vocab_direct, vocab_piv)
        
    vocab = []
    instream = open(filename, 'r')
    for line in instream:
	vocab.append(line)	
        
    instream.close()
    return vocab

# ------------------------------------------------------- #

def makeVocab(filename, vocab_direct, vocab_piv):
    outstream = open(filename, 'w')
    for i in vocab_direct:
	outstream.write(i + '\n')
    for j in vocab_piv:
	outstream.write(j+ '\n')
    outstream.close()

# ------------------------------------------------------- #

def loadData(source, target):
    pickle_file = src + '-' + target + '-dev.grammars.pkl'
    if not fileExists(pickle_file):
	print pickle_file + " not found. Exiting"
	sys.exit(-1)
    
    print "Loading " + pickle_file + "...",
    sys.stdout.flush()    

    instream = open(pickle_file, 'rb')
    extractions = pickle.load(instream)
    instream.close()

    print "Done"
    return extractions

# ------------------------------------------------------- #

def fileExists(filename):
    if os.path.exists(filename):
	return True
    return False

# ------------------------------------------------------- #

main()
