"""
Code to parse the tsv file, create features and output the txt file for VW

Feel free to modify and improve directly in this file.
"""

# Default files to use if no command line arguments
tsv_file = '../data/train.tsv' # Source file (TSV)
txt_file = '../data/train.txt' # File for VW (TXT)
test = False

from os.path import isfile
import sys
import csv
from myparser import parse # see parser.py
# Add other feature scripts here


# Read command line
if len(sys.argv) >= 3:
	tsv_file = sys.argv[1]
	txt_file = sys.argv[2]
if len(sys.argv) == 4:
	test = sys.argv[3] == 'test'

# If file already exists, exit the script. This can be remove to force the execution.
if isfile(txt_file):
	print('The txt file already exitst. Conversion skipped.')
	sys.exit(1);

with open(tsv_file,'r') as tsvin, open(txt_file,'w') as txtout:
	tsvin.readline() # Skip header
	tsvin = csv.reader(tsvin, delimiter='\t')
	
	for row in tsvin:
		to_write = ''
		phrase = parse(row[2]) # clean and store the phrase
		
		
		# Write label and tag
		to_write += str(int(row[3]) + 1) if test==False else '1'
		to_write += " '" + row[0]
		
		# Parse
		to_write += ' |phrase '
		to_write += phrase
		
		# Add features
		# I wrote one inline but we can of course make call to other scripts here
		to_write += ' |count word_count:'
		to_write += str(1+phrase.count(' '))
		
		txtout.write(to_write + '\n')
	
