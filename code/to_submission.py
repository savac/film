"""
Convert to the CSV format for submission
Feel free to modify if there is mistakes.
"""

txt_file = '../data/predictions.txt' # File from VW (TXT)

import sys

if len(sys.argv) >= 2:
	txt_file = sys.argv[1]
	
txt_file = open(txt_file,'r')
submission_file = open('../data/submission.csv','w')

submission_file.write('PhraseId,Sentiment\n') # Write header

for line in txt_file:
	new_line = ''
	field = line[:-1].split(' ')
	new_line = field[1]
	cl = int(max(min(round(float(line[0]))-1,4),0))
	new_line += ','+str(cl)
	submission_file.write(new_line + '\n')
	
