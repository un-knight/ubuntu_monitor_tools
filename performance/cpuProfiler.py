# -*- coding: UTF-8 -*-

# from baseProfiler import BaseProfiler
from performance.baseProfiler import BaseProfiler
# import datetime
# import re
# from functools import reduce
# import subprocess
# from multiprocessing import cpu_count
import psutil
import time


class CpuProfiler(BaseProfiler):

    def __init__(self, **args):
        super().__init__(**args)
        self.cpu_util_list = []

#     def profile(self):
#         """output of 'top -bc -n 1 | grep "python main.py" | grep -v grep'
#         23101 yejunxi+  20   0 16.112g 1.683g 120188 S 106.2 10.8   0:00.45 python main.py --epoch 1000
#         22914 yejunxi+  20   0 16.113g 1.985g 434960 S  31.2 12.8   0:12.82 python main.py --epoch 1000
#         """
#         part1 = 'top -bc -n 1 | grep "{}"'.format(self.process)
#         part2 = "| grep -v grep"
#         command = part1 + part2

#         try:
#             output = subprocess.check_output(command, shell=True).decode('utf-8').strip()
#         except subprocess.CalledProcessError as e:
#             print('cpu profiler error result will be set to 0, ', e)
#             output = None

#         cpu_util = 0.0
#         if output is not None:
#             for line in output.split('\n'):
#                 cpu_util += float(line.split()[8])

#         cpu_util /= self.cpu_core
    
    def run(self):
        while True:
            with self.cond:
                self.cond.wait()
                
                if self.alive.value:
                    t1 = time.time()
                    cpu_util = psutil.cpu_percent(interval=None)
                    self.cpu_util_list.append(cpu_util)
                    print('cpu time: {:.5f}s'.format(time.time()-t1))
                else:
                    print('cpu process out')
                    self.queue.put({'cpu_util': self.cpu_util_list})
                    break

# unit testing
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('pid', type=str)
    args = parser.parse_args()

    cpu_pro = CpuProfiler(args.pid)
    print(cpu_pro.profile())