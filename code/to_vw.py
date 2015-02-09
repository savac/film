"""
Code to parse the tsv file, create features and output the txt file for VW

Feel free to modify and improve directly in this file.
"""

tsv_file = '../data/train.tsv' # Source file (TSV)
txt_file = '../data/train.txt' # File for VW (TXT)
test = False

from os.path import isfile
from sys import exit
import csv
from myparser import parse # see parser.py
# Add other feature scripts here



# If file already exists, exit the script. This can be remove to force the execution.
if isfile(txt_file):
	print('The txt file already exitst. Task skipped.')
	exit(1);

with open(tsv_file,'r') as tsvin, open(txt_file,'w') as txtout:
	tsvin.readline() # Skip header
	tsvin = csv.reader(tsvin, delimiter='\t')
	
	for row in tsvin:
		to_write = ''
		phrase = parse(row[2]) # clean and store the phrase
		
		
		# Write label and tag
		to_write += row[3] if test==False else '1'
		to_write += " '" + row[0]
		
		# Parse
		to_write += ' |phrase '
		to_write += phrase
		
		# Add features
		# I wrote one inline but we can of course make call to other scripts here
		to_write += ' |count word_count:'
		to_write += str(1+phrase.count(' '))
		
		txtout.write(to_write + '\n')
	
