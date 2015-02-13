"""
Code to parse the tsv file, create features and output the txt file for VW

Feel free to modify and improve directly in this file.
"""

# Default files to use if no command line arguments
tsv_file = './train.tsv' # Source file (TSV)
txt_file = './trainvw.txt' # File for VW (TXT)
csv_sam = './toaddfeatures.csv' # Csv from the script
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


with open(tsv_file,'r') as tsvin, open(csv_sam, 'r') as csvsam, open(txt_file,'w') as txtout:
	tsvin.readline() # Skip header
	tsvin = csv.reader(tsvin, delimiter='\t')
	csvsam = csv.reader(csvsam, delimiter=',')
	for row, row2 in zip(tsvin, csvsam):
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
		to_write += ' |i ' 
                for k in range(0,24):
			to_write += ' i' + str(k) +':'
			to_write += row2[k]
		txtout.write(to_write + '\n')
	
