#!/usr/bin/env python

import iperf3
import os
# from os import system as clear
# from os import path, mkdir
from datetime import datetime
from pprint import pprint

VERSION = "1.0"
TITLE = "Tier II iPerf3 Python Script"

# Global Settings
GLOBAL_SETTINGS = {
	"server_hostname": "ping.online.net",
	"duration": 20,
	"port": 5203,
	"protocol": "tcp",
	"reverse": True,
	"num_streams": 20,
	"blksize": 1024,
}

SERVER_LIST = [
	"ping.online.net",
	"iperf.he.net",
	"speedtest.serverius.net"
]

SCRIPT_PATH = os.path.abspath("./")
SCRIPT_LOG_PATH = os.path.join(SCRIPT_PATH, "iperf_logs")

if not os.path.exists(SCRIPT_LOG_PATH):
	os.mkdir(SCRIPT_LOG_PATH)

IPERF_TEST_RESULTS = {
	"tcp":[
		"tcp_mss_default",
		"retransmits",
		"sent_bytes",
		"sent_bps",
		"sent_kbps",
		"sent_Mbps",
		"sent_kB_s",
		"sent_MB_s",
		"received_bytes",
		"received_bps",
		"received_kbps",
		"received_Mbps",
		"received_kB_s",
		"received_MB_s",		
	],
	"udp":[
		"bytes",
		"bps",
		"jitter_ms",
		"kbps",
		"Mbps",
		"kB_s",
		"MB_s",
		"packets",
		"lost_packets",
		"lost_percent",
		"seconds",
	],
	"parameters":[
		"text",
		"json",
		"error",
		"time",
		"timesecs",
		"system_info",
		"version",
		"local_host",
		"local_port",
		"remote_host",
		"remote_port",
		"reverse",
		"protocol",
		"num_streams",
		"blksize",
		"omit",
		"duration",
		"local_cpu_total",
		"local_cpu_user",
		"local_cpu_system",
		"remote_cpu_total",
		"remote_cpu_user",
		"remote_cpu_system",
	]
}



def menu():
	menu_index = [None] * len(GLOBAL_SETTINGS)


	os.system('cls' if os.name == 'nt' else 'clear')

	while True:
		dt = datetime.now()
		log_file = os.path.join(
			SCRIPT_LOG_PATH, 
			str(dt.year).zfill(2) + str(dt.month).zfill(2) + str(dt.day).zfill(2) + "_" + \
			str(dt.hour).zfill(2) +	str(dt.minute).zfill(2) + str(dt.second).zfill(2) + ".json"
			)
		print("=" * 70)
		print(TITLE)
		print("Version: {0}".format(VERSION))
		print("-" * 70)		
		print("=" * 70)
		print("Global Settings")
		print("-" * 70)
		i = 0
		for x in GLOBAL_SETTINGS.keys():
			print("{2}: {0}: {1}".format(x, GLOBAL_SETTINGS[x], i + 1))
			menu_index[i] = x
			i += 1
		print("=" * 70)
		print("Options: [Q]uit | [R]un")
		print("-" * 70)
		# print("Select A Server")
		# print("-" * 70)
		# i = 0
		# for x in SERVER_LIST:
		# 	print ("{0}: {1}".format(i,x))
		# 	i += 1

		# print("=" * 70)
		selection = input("Please make a selection: ")
		if selection.isnumeric():
			selection = int(selection) - 1
			if selection < len(menu_index) and selection >= 0:
				index = menu_index[selection]
				if menu_index[selection] == "server_hostname":
					os.system('cls' if os.name == 'nt' else 'clear')
					i = 0
					# Loops thru the default server list and displays options.
					for x in SERVER_LIST:
						print ("{0}: {1}".format(i,x))
						i += 1
					print("Please select a server hostname or enter a new server hostname")
					option = input("server_hostname [{0}]:".format(GLOBAL_SETTINGS[menu_index[selection]]))
					if option.isnumeric():
						option = int(option)
						if option < len(SERVER_LIST) and option >= 0:
							GLOBAL_SETTINGS[index] = SERVER_LIST[option]
					elif option.strip() == "":
						pass
					else:
						# Adds unlisted server and also appends to option list
						# Adds are not persitent on script close.
						GLOBAL_SETTINGS[index] = option
						SERVER_LIST.append(option)
				else:
					option = input("Please enter '{0}' [{1}]: ".format(index, GLOBAL_SETTINGS[index]))
					if option.isnumeric():
						GLOBAL_SETTINGS[index] = int(option)
					elif index == "protocol":
						# Specify protocols this will limit options
						if option.lower() == "tcp":
							GLOBAL_SETTINGS[index] = option.lower()
						elif option.lower() == "udp":
							GLOBAL_SETTINGS[index] = option.lower()
					elif option.strip() == "":
						pass
					elif option.lower() == "true" or option.lower() == "false":
						GLOBAL_SETTINGS[index] = option.lower().capitalize()
					else:
						GLOBAL_SETTINGS[index] = option


		elif selection.lower() == "quit" or selection.lower() == "q":
			# Breaks out of while loop and closes script.
			break
		elif selection.lower() == "run" or selection.lower() == "r":
			os.system('cls' if os.name == 'nt' else 'clear')

			result = run_iperf3(GLOBAL_SETTINGS)

			if result["parameter"]["error"]:
				pass
			else:
				print("=" * 70)
				print("SETTINGS:")
				print("-" * 70)
				for i in result["parameter"].keys():
					if i == "json" or i == "text":
						pass
					else:
						print(i + ": " + str(result["parameter"][i]))

				print("=" * 70)
				print("SUMMARY:")
				print("-" * 70)
				for i in result["summary"].keys():
					print(i + ": " + str(result["summary"][i]))

				with open(log_file, "a") as log:
					log.write(("=" * 70) + "\n")
					log.write("COMPLETE LOG\n")									
					log.write(("-" * 70) + "\n")	

					log.write(str(result["parameter"]["text"]) + "\n")

					log.write(("=" * 70) + "\n")
					log.write("SETTINGS\n")									
					log.write(("-" * 70) + "\n")	

					for i in result["parameter"].keys():
						if i == "json" or i == "text":
							pass
						else:
							log.write(i + ": " + str(result["parameter"][i]) + "\n")

					log.write(("=" * 70) + "\n")
					log.write("SUMMARY\n")									
					log.write(("-" * 70) + "\n")		
					for i in result["summary"].keys():
						log.write(i + ": " + str(result["summary"][i]) + "\n")

				print("=" * 70)
				print("full log file located at {0}".format(log_file))
				print("-" * 70)

			input("Press enter to continue...")





		os.system('cls' if os.name == 'nt' else 'clear')


def run_iperf3(object):
	client = iperf3.Client()
	# Loop global settings
	# for x in GLOBAL_SETTINGS.keys():
	# 	if GLOBAL_SETTINGS[x].isnumeric():
	# 		eval("client.{0} = {1}".format(x, GLOBAL_SETTINGS[x]))
	# 	else:
	# 		eval("client.{0} = '{1}'".format(x, GLOBAL_SETTINGS[x]))

	client.duration = GLOBAL_SETTINGS["duration"]
	client.server_hostname = GLOBAL_SETTINGS["server_hostname"]
	client.port = GLOBAL_SETTINGS["port"]
	client.protocol = GLOBAL_SETTINGS["protocol"]
	client.reverse = GLOBAL_SETTINGS["reverse"]
	client.num_streams = GLOBAL_SETTINGS["num_streams"]
	client.blksize = GLOBAL_SETTINGS["blksize"]
	# client.json_output = GLOBAL_SETTINGS["json_output"]
	# client.verbose = True

	print("Connecting to {0}:{1}".format(client.server_hostname, client.port))
	output = {"parameter":{},"summary":{}}
	result = client.run()


	for x in IPERF_TEST_RESULTS["parameters"]:
		try:
			value = eval("result.{0}".format(x))
			# print ("{0}: {1}".format(x, value))
			output["parameter"][x] = value
		except:
			continue
	if result.error:
		print(result.error)
	else:

		for x in IPERF_TEST_RESULTS[GLOBAL_SETTINGS["protocol"]]:
			value = eval("result.{0}".format(x))
			# print ("{0}: {1}".format(x, value))
			output["summary"][GLOBAL_SETTINGS["protocol"] + ":" + x] = value

	return output

if __name__ == "__main__":
	menu()
