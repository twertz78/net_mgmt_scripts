#! /bin/env python
# n7k_f3_proc_mem.py
# This script checks the output of `show system internal process memory` for all N7k LC installed
# and generates a syslog message if RSS is greater than rss_max which is by default set to 800,000
#
# Instructions
# Upload n7k_f3_proc_mem.py to the N7k and save it in the /scripts directory in bootflash: 
# N77-042# dir bootflash:/scripts | i n7k
#       1480    Nov 30 17:52:14 2017  n7k_f3_proc_mem.py
#
# The following will configure the scheduler to run the script every 2 mins
# and generate a syslog if RSS is greater than 100,000 (if omitted rss_max is 800,000)
# 
# N7706(config)# feature scheduler 
# N7706(config)# scheduler job name ipfib_mem_check
# N7706(config-job)# source n7k_f3_proc_mem.py 100,000 ! the argument can be omitted
# N7706(config-job)# exit
# N7706(config)# scheduler schedule name ipfib_mem_check
# N7706(config-schedule)# job name ipfib_mem_check
# N7706(config-schedule)# time start now repeat 0:0:2
# Schedule starts from Thu Nov 30 18:02:30 2017
# N7706(config-schedule)# end
# N7706#
#
# Written by: aeguiart@cisco.com
#  Nov 30th, 2017

import sys
import syslog
import re

if __name__ == "__main__":
    if len(sys.argv) > 1:
        rss_max = int(sys.argv[1])
    else:
        rss_max = 800000
    # print("rss_max=".format(rss_max))
    sh_module = cli('show module | grep "\-M\|\-F" | exc Fabric')
    module_data = []
    if sh_module:
        for line in sh_module.splitlines():
            mod_fnd = re.search("(\d+)\s+\d+\s+.*\s([N77|N7K].*)\s+", line)
            if mod_fnd:
                slot = mod_fnd.group(1)
                part_number = mod_fnd.group(2).strip()
                module_data.append({"slot": slot, "part_number": part_number})
        if module_data:
            for module in module_data:
                sh_system_proc_mem = cli(
                    "slot {} quoted 'show system internal process memory | inc PID|ipfib | ex egrep'".format(
                        module["slot"]))
                if sh_system_proc_mem:
                    for line in sh_system_proc_mem.splitlines():
                        if "/isan/bin/ipfib" in line:
                            pid, tty, stat, time, majflt, trs, rss, vsz, mem, cmd = line.split()
                            # print("PID: {} RSS:{}".format(pid, rss))
                            rss = int(rss)
                            if rss > rss_max:
                                msg = "Module {} in slot {} has ipfib process with PID {} showing high memory usage. RSS={}".format(
                                    module["part_number"], module["slot"], pid, rss)
                                syslog.syslog(1, msg)
