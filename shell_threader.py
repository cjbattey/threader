#! /usr/bin/python

import threading
import os
import subprocess

## This script threads out the shell calls in file calls.list
threads = 4    ## Specify total number of threads here

lock = threading.Lock()
def threader():
	while os.stat('calls.list').st_size >0:
		## Run 1st call from calls.list, then delete that line
		with lock:
			f = open('calls.list','rb')
			call = f.readline()
			subprocess.call("tail -n +2 calls.list > smaller.tmp",shell=True)
			os.rename("smaller.tmp","calls.list")
		subprocess.call(call,shell=True)
		if call != "":
			print(threading.current_thread().name + " did call: " + call)
		f.close()
	print(threading.current_thread().name + " terminated")
		
for t in range(threads):
	threading.Thread(target = threader).start()
	print("Thread-" + str(t+1) + " spawned")