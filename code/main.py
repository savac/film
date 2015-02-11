"""
main script to coordinate all the tasks
"""

# Parameters fo VW
alpha = 0.180859
beta = 0.007839
l1 = 0.003497
l2 = 0.002761
vw_options = '-c -b 28 --ngram 3'
vw_options_training = '--passes 1 --ect 5'

tsv_file = '../data/train.tsv'
txt_file = '../data/train.txt'
tsv_test_file = '../data/test.tsv'
txt_test_file = '../data/test.txt'
txt_predictions_file = '../data/predictions.txt'

optim_hyperparam = False

import os
from myhypersearch import score

# Convert to VW
print('Converting the training set...')
os.system('python to_vw.py ' + tsv_file + ' ' + txt_file)

# Train with VW
print('Training...')
if optim_hyperparam:
	print('\tOptimising l1')
	vw_command = 'vw -f model.vw --ftrl --ftrl_alpha '+str(alpha)+' --ftrl_beta '+str(beta)+' --l1 % --l2 ' + str(l2) + ' --data ' + txt_file + ' ' + vw_options + ' ' +  vw_options_training
	l1 = score(vw_command, 1e-3, l1, 1e3)
	print('\tOptimising l2')
	vw_command = 'vw -f model.vw --ftrl --ftrl_alpha '+str(alpha)+' --ftrl_beta '+str(beta)+' --l1 '+str(l1)+' --l2 % --data ' + txt_file + ' ' + vw_options + ' ' +  vw_options_training
	l2 = score(vw_command, 1e-3, l2, 1e3)
	print('\tOptimising alpha')
	vw_command = 'vw -f model.vw --ftrl --ftrl_alpha % --ftrl_beta ' + str(beta) + ' --l1 ' + str(l1) + ' --l2 ' + str(l2) + ' --data ' + txt_file + ' ' + vw_options + ' ' +  vw_options_training
	alpha = score(vw_command,1e-3, alpha, 1e3)
	print('\tOptimising beta');
	vw_command = 'vw -f model.vw --ftrl --ftrl_alpha '+str(alpha)+' --ftrl_beta % --l1 ' + str(l1) + ' --l2 ' + str(l2) + ' --data ' + txt_file + ' ' + vw_options + ' ' +  vw_options_training
	beta = score(vw_command, 1e-3, beta, 1e3)

os.system('vw -f model.vw --ftrl --ftrl_alpha ' + str(alpha) + ' --ftrl_beta ' + str(beta) + ' --l1 ' + str(l1) + ' --l2 ' + str(l2) + ' --data ' + txt_file + ' ' + vw_options + ' ' +  vw_options_training)

# Convert test set to VW
print('Converting the test set...')
os.system('python to_vw.py ' + tsv_test_file + ' ' + txt_test_file + ' test')

# Predict the test set
print('Predicting...')
os.system('vw -p ' + txt_predictions_file + ' --data ' + txt_test_file + ' -t -i model.vw ' + vw_options)

# Convert predictions to submission format
print('Converting the predictions...')
os.system('python to_submission.py')
