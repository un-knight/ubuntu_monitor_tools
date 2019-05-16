## 环境依赖

- python版本：python 3.6 及以上
- python依赖库：
    - matplotlib
    - pandas
    - psutil
    - py3nvml
- 依赖系统工具：
    - iotop
    - nvidia-smi
    - top

## 权限说明
普通用户权限执行即可。

## 使用说明

### 清除缓存

```
./clear_buffers.sh
```

### 运行监控

```shell
usage: monitor_main.py [-h] [--duration DURATION]
                       [--target-gpu [TARGET_GPU [TARGET_GPU ...]]]
                       [--output-path OUTPUT_PATH]
                       [--signal-frequence SIGNAL_FREQUENCE]

optional arguments:
  -h, --help            show this help message and exit
  --duration DURATION   time to monitor(default:60s)
  --target-gpu [TARGET_GPU [TARGET_GPU ...]]
                        target gpu to monitor(default:[0,])
  --output-path OUTPUT_PATH
                        log output path(default: ./)
  --signal-frequence SIGNAL_FREQUENCE
                        signal frequence(default: 1.6Hz)
```

举例说明：

```shell
python monitor_main.py --duration 60 --target-gpu 0 1 2 3 4
```


## 结果查看
- log.txt  数据文件
- log_visualization/log.png  数据可视化

## 可视化效果图
![](log.png)