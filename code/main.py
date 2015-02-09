"""
main script to coordinate all the tasks
"""

# Parameters fo VW
l = 0.1
l1 = 0.1
l2 = 0.1

tsv_file = '../data/train.tsv'
txt_file = '../data/train.txt'

vw_options = ''

import os

# Convert to VW
os.system('python to_vw.py ' + tsv_file + ' ' + txt_file)

# Launch VW
os.system('vw -l ' + str(l) + ' --l1 ' + str(l1) + ' --l2 ' + str(l2) + ' --data ' + txt_file + ' ' + vw_options)
