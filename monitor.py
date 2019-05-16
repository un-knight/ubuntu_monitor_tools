# -*- coding: UTF-8 -*-
import os
import datetime
import time
import multiprocessing
import datetime

import pandas as pd

from comm.config import DATA_TITLE
from performance.cpuProfiler import CpuProfiler
from performance.memProfiler import MemProfiler
from performance.IOProfiler import IOProfiler
from performance.gpuProfiler import GpuProfiler
from comm.utils import draw_lines, draw_box


class ProcessMonitor(object):
    
    @staticmethod
    def set_intervals(signal_frequence):
        # Reference: https://zhuanlan.zhihu.com/p/22480177
        SAMPLING_RATE = 2.56
        intervals = round(1.0 / (SAMPLING_RATE * signal_frequence), 3)
        return intervals

    def __init__(self, args, signal_frequence=1.6, log_name='log.csv'):
        super().__init__()
        self.cond = multiprocessing.Condition()
        self.alive = multiprocessing.Value('b', 1)
        self.profiler_num = 4
        
        # initialize profiler to collect data
        self.queue = multiprocessing.Queue(self.profiler_num)
        self.cpu_profiler = CpuProfiler(condition=self.cond, alive=self.alive, queue=self.queue)
        self.mem_profiler = MemProfiler(condition=self.cond, alive=self.alive, queue=self.queue)
        self.io_profiler = IOProfiler(condition=self.cond, alive=self.alive, queue=self.queue)
        self.gpu_profiler = GpuProfiler(args.target_gpu, condition=self.cond, alive=self.alive, queue=self.queue)

        self.log_name = log_name
        self.output_path = args.output_path
        self.running = True
        self.duration = args.duration
        self.intervals = ProcessMonitor.set_intervals(signal_frequence) 
#         self.intervals = 1.0
        print('intervals: {}'.format(self.intervals))
        self.count = 0
        self.timestamp_list = []

    def write_file(self):
        if os.path.exists(self.output_path) is False:
            os.makedirs(self.output_path)

        # get profiler subprocess list
        profiler_list = [attr for attr in dir(self) if attr.endswith('_profiler')]
        
        # to start profiler subprocesses
        for profiler in profiler_list:
            profiler = getattr(self, profiler)
            profiler.start()
        
        # waitting for all subprocesses to start
        time.sleep(1)
        
        starttime = time.time()
        errorTimes = 0
        while self.running:
            nowtime = time.time()
            # need to be changed
            if self.duration != 0 and ((nowtime - starttime) - self.intervals - 1) >= self.duration:
                self.running = False
                break
                
            str_now_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(time.time()))
            self.timestamp_list.append(str_now_time)

            with self.cond:
                # norify all subprocesses
                self.count += 1
                print(self.count)
                self.cond.notify_all()

            time.sleep(self.intervals)
            
            collection_time = time.time() - nowtime
            print('collection time: {}s'.format(collection_time))
            print('-'*30)
        
        with self.cond:
            # to stop profiler subprocess
            self.alive.value = 0
            self.cond.notify_all()
        
        # get result from queue
        result_dict = {}
        for i in range(self.profiler_num):
            output_dict = self.queue.get()
            # merge dict
            # only supported by >= python3.5
            result_dict = {**result_dict, **output_dict}
            
        self.result_dict = result_dict
        self.save_logfile()


    def pic(self):
        cpu_util_list = self.result_dict['cpu_util']
        rss_list = self.result_dict['rss']
        read_speed_list = self.result_dict['io_read']
        write_speed_list = self.result_dict['io_write']
        gpu_mean_list = self.result_dict['gpu_util_mean']
        
        suffix = ProcessMonitor.get_time()

        time_list = [x * self.intervals for x in range(len(cpu_util_list))]
        x_label = 'times(s)'
        draw_lines(time_list, cpu_util_list, x_label, 'cpu utils (%)', self.output_path, suffix=suffix)

        draw_lines(time_list, rss_list, x_label, 'memory (GB)', self.output_path, suffix=suffix)

        draw_lines(time_list, read_speed_list, x_label, 'io read (MB/s)', self.output_path, suffix=suffix)
        draw_lines(time_list, write_speed_list, x_label, 'io write (MB/s)', self.output_path, suffix=suffix)

        draw_lines(time_list, gpu_mean_list, x_label, 'gpu utils (%)', self.output_path, suffix=suffix)

        draw_box(filename='box_cpu_util-{}.png'.format(suffix), output_path=self.output_path, cpu_util=cpu_util_list)

        draw_box(filename='box_memory-{}.png'.format(suffix), output_path=self.output_path, rss=rss_list)

        draw_box(filename='box_io-{}.png'.format(suffix), output_path=self.output_path, io_read=read_speed_list, io_write=write_speed_list)

        draw_box(filename='box_gpu_util-{}.png'.format(suffix), output_path=self.output_path, gpu_util=gpu_mean_list)
        print('visualization done!')

    def run(self):
        self.write_file()
        self.pic()
        
    def save_logfile(self):
#         print(self.count)

        # to make all list equal length
        len_list = []
        for key, value in self.result_dict.items():
            len_list.append(len(value))
        min_len = min(len_list)
        for key, value in self.result_dict.items():
            value = value[:min_len]
            self.result_dict[key] = value
#             print(key, len(value))
        
        df = pd.DataFrame(self.result_dict)
        df.to_csv(os.path.join(self.output_path, self.log_name), header=True)
        
    @staticmethod
    def get_time():
        return (str(datetime.datetime.now() - datetime.timedelta(hours=8))[:-10]).replace(' ', '_').replace(':', '-')
    