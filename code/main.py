"""
main script to coordinate all the tasks
"""

# Parameters fo VW
alpha = 0.295059
beta = 1.51332
l1 = 3.6036
l2 = 1.53323
vw_options = '-c -b 24 --ngram 5'
vw_options_training = '--passes 10 --noconstant'

tsv_file = '../data/train.tsv'
txt_file = '../data/train.txt'
tsv_test_file = '../data/test.tsv'
txt_test_file = '../data/test.txt'
txt_predictions_file = '../data/predictions.txt'



import os

# Convert to VW
print('Converting the training set...')
os.system('python to_vw.py ' + tsv_file + ' ' + txt_file)

# Train with VW
print('Training...')
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
