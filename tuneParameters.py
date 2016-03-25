"""
Program to remove .sgm file annotations, create reference .ini files,
tune MIRA parameters, and performs some decoding

With the new grammar, sgm files don't need grammar annotations. But 
the .ini files do need a grammar location. .sgm files can simply be
replaced with the tokenized, parallel  dev and test data
"""

# Imports
import subprocess
import sys
import os

src = 'es'
piv = 'en'
tar = 'cs'

CPUS = 8

direct = 'direct'
pivot = 'pivot'
combined = 'combined'

# ------------------------------------------------------- #

def main():
    #testAndTune(src, direct)
    
    # TODO Uncomment and tune methods below
    testAndTune(src, pivot)
    #testAndTune(src, combined)
    
# ------------------------------------------------------- #

def testAndTune(source, mode):
    ini_filename = checkIni(source, mode)

    sgm_tune_filename = source + '-' + tar + '-dev'
    sgm_test_filename = source + '-' + tar + '-test'
    command = '/export/ws15-mt-data2/umandujano/' + \
	      'cdec/training/mira/mira.py -d ' + sgm_tune_filename + \
	      ' -t '+ sgm_test_filename + ' -c ' + ini_filename + \
	      ' -j ' + str(CPUS) + " -o " + source + "-" + mode + "-mira"
    
    print "Tuning parameters and testing for %s mode..." % (mode),
    sys.stdout.flush() 
    subprocess.call(command, shell=True)
    print "Done"    

# ------------------------------------------------------- #

def checkIni(source, mode):
    filename = source + '-' + mode + '.ini'
    if fileExists(filename):
	return filename
    
    print "File %s not found... Making" % (filename), 
    outstream = open(filename, 'w')
    outstream.write('formalism=scfg' + '\n')
    outstream.write('add_pass_through_rules=true' + '\n')
    outstream.write('feature_function=WordPenalty' + '\n')
    outstream.write('feature_function=KLanguageModel ') # No newline 
    outstream.write('/export/ws15-mt-data2/umandujano/base/es-cs.klm' + '\n')
    outstream.write('grammar=/export/ws15-mt-data2/umandujano/base/')
    outstream.write(source + '-' + mode + '-grammar.txt.gz')
    outstream.close()
    
    print "Made" 
    return filename    

# ------------------------------------------------------- #

def fileExists(filename):
    if os.path.exists(filename):
	return True
    return False

# ------------------------------------------------------- #
main()
