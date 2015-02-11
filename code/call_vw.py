"""
Launch VW and retrieve the error
"""

import subprocess

def call_vw_inline(command):
	results = subprocess.check_output(command.split(' '), shell=True, stderr=subprocess.STDOUT) # run command
	results = results.decode("utf-8")
	#print(results)
	results = results.split('\r\n')[-4] # average loss = 
	results = results.split('= ')[1]
	results = float(results)
	return results
	
def call_vw(vw_command, x):
	new_command = vw_command.replace('%', str(x))
	return call_vw_inline(new_command)
	
if __name__ == '__main__':
	import sys
	
	if len(sys.argv) >= 2:
		print(call_vw(sys.argv[1]))
