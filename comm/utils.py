# -*- coding: UTF-8 -*-
import os
import subprocess

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import style
from scipy.interpolate import spline
import numpy as np

# style.use('fivethirtyeight')

def get_pid(proc_name, monitor_filename):
    '''get pid according to proc_name
    basic command: ps -ef | grep "name" | grep -v grep | awk '{print $2}'
    '''
    grep_name = 'grep "{}"'.format(proc_name)
    part1 = """ps -ef | {grep_name} """.format(grep_name=grep_name)
    # 'grep -v python' to get rid of python command 
    part2 = """| grep -v grep | grep -v "python {}" """.format(monitor_filename)
    part3 = """| awk '{print $2}'"""
    get_pid_command = part1 + part2
    # print(get_pid_command)

    try:
        outputs = subprocess.check_output(get_pid_command, shell=True).decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        outputs = None
        return outputs
    
    # dict format: {pid: ppid}
    pid_dict = {}
    for line in outputs.split('\n'):
        element = line.split()
        pid = int(element[1])
        ppid = int(element[2])
        pid_dict[pid] = ppid
    
    # subprocess's ppid == main process pid
    # main process's ppid == bash pid
    # since pid_dict.keys() got all pid which have the same process name
    # so only main porcess's ppid is not in pid_dict.keys()
    pids = list(pid_dict.keys())
    pids.sort()
    for pid in pids:
        ppid = pid_dict[pid]
        if ppid not in pid_dict.keys():
            break
    
    print('target process pid: {}'.format(pid))
    return pid


def draw_lines(x, y, x_label, y_label, output_path, suffix):

    def min_y(data_list):
        return round(min(data_list)*0.8, 2)

    def max_y(data_list):
        return round(max(data_list)*1.2, 2)
    
    plt.figure(figsize=(17, 6))
    # draw raw data
    plt.plot(x, y, 'dodgerblue', linewidth=1, label=y_label)
    
    # draw smooth data if number of examples > 500
#     if len(x) >= 500:
#         x_new = np.linspace(min(x), max(x), len(x)/10)
#         y_new = spline(x, y, x_new)
#         plt.plot(x_new, y_new, 'r', linewidth=1)
    
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.ylim(min_y(y), max_y(y))
    plt.grid(False)
    plt.legend()

    filename = '{}-{}.png'.format('_'.join(y_label.split()[:-1]), suffix)
    file_dir = 'log_visualization'
    output_path = os.path.join(output_path, file_dir)
    if os.path.exists(output_path) is False:
        os.makedirs(output_path)
    
    plt.savefig(os.path.join(output_path, filename), dpi=400, quality=100)
    plt.clf()
    

def draw_box(filename, output_path, **data_dict):
    keys = list(data_dict.keys())
    keys.sort()
    values = []
    for key in keys:
        values.append(data_dict[key])

    fig = plt.figure()
    ax = plt.subplot()
    ax.boxplot(values, notch=False)
    ax.set_xticks(list(range(1, len(keys)+1)))
    ax.set_xticklabels(keys)
    plt.grid(axis='y')

    file_dir = 'log_visualization'
    output_path = os.path.join(output_path, file_dir)
    if os.path.exists(output_path) is False:
        os.makedirs(output_path)
    
    plt.savefig(os.path.join(output_path, filename), dpi=400, quality=100)
    plt.clf()


# for unit testing
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--proc-name', type=str)
    args = parser.parse_args()

    get_pid(args.proc_name)