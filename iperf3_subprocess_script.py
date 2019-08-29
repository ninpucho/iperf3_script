#!/usr/bin/env python

import subprocess
import os
from datetime import datetime

VERSION = "1.0"
TITLE = "Tier II iPerf3 Python Script"
SCRIPT_PATH = os.path.abspath("./")
SCRIPT_LOG_PATH = os.path.join(SCRIPT_PATH, "iperf_logs")

if not os.path.exists(SCRIPT_LOG_PATH):
    os.mkdir(SCRIPT_LOG_PATH)

# Global Settings
GLOBAL_SETTINGS = {
    "_order_": [
        "--client",
        "--port",
        "--reverse",
        "--bandwidth",
        "--omit",
        "--no-delay",
        "--time",
        "--parallel",
        "--interval",
        "--window",
        "--udp",
        "--verbose",
        "--logfile"
    ],
    "--client": "resfiosspeed1.west.verizon.net",
    "--time": 20,
    "--port": 5201,
    "--udp": False,
    "--reverse": True,
    "--parallel": 20,
    "--interval": 0,
    "--bandwidth": "0M",
    "--omit": 2,
    "--window": "0M",
    "--no-delay": True,
    "--verbose": False,
    "--logfile": ""
}
# COMMAND = "iperf3 -client {SERVER_HOSTNAME} --parallel=20 --time=20 -p 5201 -i 0 -b 0M -R -O 2 -w 0M -N"

SERVER_LIST = [
    "resfiosspeed1.west.verizon.net",
    "nyfiosspeed1.west.verizon.net",
]


def print_menu(menu_object):
    # Print Header
    print("=" * 70)
    print(TITLE)
    print("Version: {0}".format(VERSION))
    print("-" * 70)
    print("=" * 70)
    i = 0
    for x in menu_object["_order_"]:
        print("{0}: {1}: {2}".format(i, x, menu_object[x])) 
        i += 1
    print("=" * 70)
    print("Options: [Q]uit | [R]un")
    print("-" * 70)
    selection = raw_input("Please make a selection: ")
    return selection
    
def main():
    GLOBAL_SETTINGS["--logfile"] = os.path.join(SCRIPT_LOG_PATH, mk_file_name("iperf_{0}.txt"))
    menu_index = [None] * len(GLOBAL_SETTINGS)

    os.system('cls' if os.name == 'nt' else 'clear')
    while True:

        selection = print_menu(GLOBAL_SETTINGS)
        if selection.isdigit():
            selection = int(selection)
            if len(menu_index) > selection >= 0:
                index = GLOBAL_SETTINGS["_order_"][selection]
                if index == "--client":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    i = 0
                    # Loops thru the default server list and displays options.
                    for x in SERVER_LIST:
                        print ("{0}: {1}".format(i, x))
                        i += 1
                    print("-" * 70)
                    print("Please select a client or enter a new client")
                    option = raw_input("--client [{0}]:".format(GLOBAL_SETTINGS[index]))
                    if option.isdigit():
                        option = int(option)
                        if len(SERVER_LIST) > option >= 0:
                            GLOBAL_SETTINGS[index] = SERVER_LIST[option]
                    elif option.strip() == "":
                        pass
                    else:
                        # Adds unlisted server and also appends to option list
                        # Adds are not persistent on script close.
                        GLOBAL_SETTINGS[index] = option
                        SERVER_LIST.append(option)
                else:
                    option = raw_input("Please enter '{0}' [{1}]: ".format(index, GLOBAL_SETTINGS[index]))
                    if option.isdigit():
                        GLOBAL_SETTINGS[index] = int(option)
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


            # Build Command
            command = "iperf3 " \
                      "--client {--client} " \
                      "--port {--port} " \
                      "--parallel {--parallel} " \
                      "--time {--time} " \
                      "--omit {--omit} " \
                      "--window {--window} " \
                      "--interval {--interval} " \
                      "--bandwidth {--bandwidth} " \
                      .format(**GLOBAL_SETTINGS)

            # Lets add boolean settings...
            for x in GLOBAL_SETTINGS:
                if isinstance(GLOBAL_SETTINGS, list):
                    pass
                elif str(GLOBAL_SETTINGS[x]).isdigit():
                    pass
                elif str(GLOBAL_SETTINGS[x]).lower() == "true":
                    command += " {0}".format(x)
            if GLOBAL_SETTINGS["--logfile"]:
                command += " --logfile {0}".format(GLOBAL_SETTINGS["--logfile"])

            result = run_iperf3(command)

            # If error we do not try to print anything to screen or log.
            if result["error"]:
                print("ERROR: {0}".format(result["error"]))
            else:
                print("=" * 70)
                result["text"]
                print("=" * 70)
                print("full log file located at {0}".format(GLOBAL_SETTINGS["--logfile"]))
                print("-" * 70)

            GLOBAL_SETTINGS["--logfile"] = os.path.join(SCRIPT_LOG_PATH, mk_file_name("iperf_{0}.txt"))
            selection = input("Press enter to continue or (Q)uit...")
            if selection.lower() == "quit" or selection.lower() == "q":
                # Breaks out of while loop and closes script.
                break
            os.system('cls' if os.name == 'nt' else 'clear')


def run_iperf3(command):
    print("Sending {0}".format(command))
    command = command.split()
    out = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    stdout, stderr = out.communicate()
    return {"error": stderr, "text": stdout}


def mk_file_name(name_format):
    # name_format i.e. iperf_{0}.txt
    dt = datetime.now()

    # Date Time tag...
    date_time_tag = str(dt.year).zfill(2) + str(dt.month).zfill(2) + str(dt.day).zfill(2) + "_" + \
        str(dt.hour).zfill(2) + str(dt.minute).zfill(2) + str(dt.second).zfill(2)
    return name_format.format(date_time_tag)

if __name__ == "__main__":
    main()
