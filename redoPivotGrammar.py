"""
Fixes the spacing issue in the es-cs-pivot grammar
"""

import gzip



def main():
    """
    instream = gzip.open('es-pivot-grammar.txt.gz', 'rb')
    temp_dest = gzip.open('temp', 'wb')
    
    for line in instream:
	line = line.split('|||')
	
	end = len(line) -1
	line[end] = " " + line[end]
	
	line = '|||'.join(line).strip('\n')
	temp_dest.write(line + '\n')

    instream.close()
    temp_dest.close()
    """ 
    instream = gzip.open('temp', 'rb')
    outfile = gzip.open('es-pivot-grammar.txt.gz', 'wb')
    for line in instream:
	line = line.strip()
	line = line + '\n'
	outfile.write(line)
	
    instream.close()
    outfile.close()


main()
