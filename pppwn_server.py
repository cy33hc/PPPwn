#!/usr/bin/env python3
#
# Copyright (C) 2024 Andy Nguyen
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import os
import subprocess
import threading
import config
from argparse import ArgumentParser
from sys import exit

def run_exploit():
    while True:
        print("Starting exploit process")
        if os.path.isfile(os.getcwd() + "/pppwn.py"):
            exploit_process = subprocess.Popen(["python3", os.getcwd() + "/pppwn.py", "--interface", config.interface, "--fw", config.firmware, "--stage1", config.stage1, "--stage2", config.stage2], stdout=subprocess.PIPE, universal_newlines=True)
        elif os.path.isfile(os.getcwd() + "/pppwn.exe"):
            exploit_process = subprocess.Popen([os.getcwd() + "/pppwn.exe", "--interface", config.interface, "--fw", config.firmware, "--stage1", config.stage1, "--stage2", config.stage2], stdout=subprocess.PIPE, universal_newlines=True)
        else:
            exploit_process = subprocess.Popen([os.getcwd() + "/pppwn", "--interface", config.interface, "--fw", config.firmware, "--stage1", config.stage1, "--stage2", config.stage2], stdout=subprocess.PIPE, universal_newlines=True)
        
        for stdout_line in iter(exploit_process.stdout.readline, ""):
            print(stdout_line)
        exploit_process.stdout.close()
        return_code = exploit_process.wait()

def main():
    parser = ArgumentParser('PPPwn Server')
    parser.add_argument('--interface', required=True, help="The network interface used for executing the exploit on")
    parser.add_argument('--fw',
                        choices=[
                            '800', '801', '803', '850', '852',
                            '900', '903', '904', '950', '951', '960',
                            '1000', '1001', '1050', '1070', '1071',
                            '1100'
                        ],
                        default='1100', help="Firmware version of the PS4. Defaults to 1100 if not specified")
    parser.add_argument('--stage1', default='stage1/stage1.bin', help="The stage1 exploit payload. Defaults to \"stage1/stage1.bin\"")
    parser.add_argument('--stage2', default='stage2/stage2.bin', help="The stage2 exploit payload. Defaults to \"stage2/stage2.bin\"")
    args = parser.parse_args()

    config.interface = args.interface
    config.firmware = args.fw
    config.stage1 = args.stage1
    config.stage2 = args.stage2
    
    exploit_thread = threading.Thread(target=run_exploit)
    exploit_thread.start()
    exploit_thread.join()

    return 0


if __name__ == '__main__':
    exit(main())
