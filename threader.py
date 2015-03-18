#! /usr/bin/python

import threading
import os
import subprocess

## This script threads out the shell calls in file threadme.txt
threads = 4    ## Specify total number of threads here

lock = threading.Lock()
def threader():
	while os.stat('threadme.txt').st_size >0:
		## Run 1st call from threadme.txt, then delete that line
		with lock:
			f = open('threadme.txt','rb')
			call = f.readline()
			subprocess.call("tail -n +2 threadme.txt > smaller.tmp",shell=True)
			os.rename("smaller.tmp","threadme.txt")
			f.close()
		subprocess.call(call,shell=True)
		if call != "":
			print(threading.current_thread().name + " did call: " + call)
	print(threading.current_thread().name + " terminated")
		
for t in range(threads):
	threading.Thread(target = threader).start()
	print("Thread-" + str(t+1) + " spawned")