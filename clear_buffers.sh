# /bin/bash
# running in root mode

sync # (move data, modified through FS -> HDD cache) + flush HDD cache
echo 3 > /proc/sys/vm/drop_caches # (slab + pagecache) -> HDD (https://www.kernel.org/doc/Documentation/sysctl/vm.txt)
blockdev --flushbufs /dev/sda

echo "clear buffers done!"