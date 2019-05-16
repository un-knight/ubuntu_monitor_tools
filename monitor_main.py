# -*- coding: UTF-8 -*-
import _init_path
import sys
from comm.utils import get_pid
from monitor import ProcessMonitor

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--duration', type=int, default=60, help='time to monitor(default:60s)')
parser.add_argument('--target-gpu', nargs='*', type=int, default=[0,], help='target gpu to monitor(default:[0,])')
parser.add_argument('--output-path', type=str, default='./', help='log output path(default: ./)')
parser.add_argument('--signal-frequence', type=float, default=1.6, help='signal frequence(default: 1.6Hz)')
args = parser.parse_args()


def main():
    global args
    
    p = ProcessMonitor(args, args.signal_frequence)
    p.run()

if __name__ == "__main__":
    main()