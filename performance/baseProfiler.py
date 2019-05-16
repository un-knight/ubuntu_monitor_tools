# -*- coding: UTF-8 -*-
import multiprocessing

class BaseProfiler(multiprocessing.Process):

    def __init__(self, pid=-1, **args):
        super().__init__()
        # named target_pid to avoid pid conflict with multiprocessing.Process
        self.target_pid = pid
        self.cond = args['condition']
        self.alive = args['alive']
        self.queue = args['queue']
        self._TO_KB = 1024
        self._TO_MB = 1024*self._TO_KB
        self._TO_GB = 1024*self._TO_MB
        
    def profile(self):
        pass
    
    def run(self):
        pass
