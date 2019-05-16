# -*- coding: UTF-8 -*-
from performance.baseProfiler import BaseProfiler
# import re
# import subprocess
from py3nvml.py3nvml import *
import time


class GpuProfiler(BaseProfiler):

    def __init__(self, target_gpus=[0,], **args):
        super().__init__(**args)
        self.util_result = {}
        self.util_result['gpu_util_mean'] = []
        self.target_gpus = target_gpus
        for gpu in target_gpus:
            self.util_result[gpu] = []

        
    def run(self):
        # initialize nvml
        nvmlInit()
        
        while True:
            with self.cond:
                self.cond.wait()
                
                if self.alive.value:
                    t1 = time.time()
                    mean = 0.0

                    for gpu in self.target_gpus:
                        try:
                            handle = nvmlDeviceGetHandleByIndex(gpu)
                            gpu_util = nvmlDeviceGetUtilizationRates(handle).gpu
                        except NVMLError as err:
                            error, gpu_util = GpuProfiler.handleError(err)
                            print(error)

                        self.util_result[gpu].append(gpu_util)
                        mean += gpu_util

                    self.util_result['gpu_util_mean'].append(mean / len(self.target_gpus))
                    print('gpu time: {:.5f}s'.format(time.time()-t1))
                else:
                    print('gpu process out')
                    self.queue.put(self.util_result)
                    break
        
        nvmlShutdown()

    @staticmethod
    def handleError(err):
        if err.value == NVML_ERROR_NOT_SUPPORTED:
            return "N/A", 0
        else:
            return err.__str__(), 0
    

# unit testing
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--target-gpu', nargs='*', type=int)
    args = parser.parse_args()
    
    target_gpu = args.target_gpu if args.target_gpu is not None else [0,]
    gpu_pro = GpuProfiler(target_gpu)
    print(gpu_pro.get_gpu_info())
