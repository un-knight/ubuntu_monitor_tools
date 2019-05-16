from performance.baseProfiler import BaseProfiler
# import subprocess
import psutil
import time


class IOProfiler(BaseProfiler):

    def __init__(self, **args):
        super().__init__(**args)
        self.r_list = []
        self.w_list = []
        
        # get initialization value
        self.t1 = time.time()
        self.disk_before = psutil.disk_io_counters()
        

    def run(self):
        while True:
            with self.cond:
                self.cond.wait()
                
                if self.alive.value:
                    t1 = time.time()
                    self.t2 = time.time()
                    self.disk_after = psutil.disk_io_counters()

                    time_delta = self.t2 - self.t1

                    disk_read_per_sec = (self.disk_after.read_bytes - self.disk_before.read_bytes) / time_delta
                    disk_write_per_sec = (self.disk_after.write_bytes - self.disk_before.write_bytes) / time_delta

                    self.disk_before = self.disk_after
                    self.t1 = self.t2

                    self.r_list.append(disk_read_per_sec / self._TO_MB)
                    self.w_list.append(disk_write_per_sec / self._TO_MB)
                    print('io time: {:.5f}s'.format(time.time()-t1))
                else:
                    print('io process out')
                    self.queue.put({
                        'io_read': self.r_list,
                        'io_write': self.w_list
                    })
                    break