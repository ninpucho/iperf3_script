#! /usr/bin/env python

import subprocess


# COMMAND = "iperf3 -c {SERVER_HOSTNAME} --parallel=20 --time=20 -p 5201 -i 0 -b 0M -R -O 2 -w 0M -N" 

COMMAND = raw_input("Please Enter Command: ")
COMMAND = COMMAND.split()

#iperf3 -c {SERVER_HOSTNAME} --parallel=20 --time=20 -p 5201 -i 0 -b 0M -R -O 2 -w 0M -N
out = subprocess.Popen(COMMAND,
	stdout=subprocess.PIPE,
	stderr=subprocess.STDOUT)

stdout,stderr = out.communicate()
print(stdout)
print(stderr)
