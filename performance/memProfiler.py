# -*- coding: UTF-8 -*-
from performance.baseProfiler import BaseProfiler
# import re
# import subprocess
import psutil
import time


class MemProfiler(BaseProfiler):
    """
    get real time physical memory usage.
    """

    def __init__(self, **args):
        super().__init__(**args)
        self.rss_list = []

    def run(self):
        """
        vmrss's basic unit is MB
        """
        # output = self.adb.cmd("dumpsys", "meminfo", self.appPid).communicate()[0].decode("utf-8").strip()
        while True:
            with self.cond:
                self.cond.wait()
                
                if self.alive.value:
                    t1 = time.time()
                    mem = psutil.virtual_memory()
                    self.rss_list.append(round(mem.used/self._TO_GB, 2))
                    print('memory time: {:.5f}s'.format(time.time()-t1))
                else:
                    print('mem process out')
                    self.queue.put({'rss': self.rss_list})
                    break


# unit testing
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('pid', type=str)
    args = parser.parse_args()

    mem_pro = MemProfiler(args.pid)
    print(mem_pro.profile())

