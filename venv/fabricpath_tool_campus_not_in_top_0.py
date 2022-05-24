import os
import re
import subprocess
from datetime import time

from netmiko import ConnectHandler

from py import nodes, secrets

# FQDN name and a "common" name for each switch. the "common" name helps shorten output,
# whereas the FQDN name is needed for the connection

switches = nodes.alldevices

# This is the "temporary" script that I have to create dynamically
new_file = file('temp_script.py', 'w')

i = 0

percent = float(100)/float(len(switches))

z = 0

# iterate through the switches to get the arrays built
for switch in switches:
    z = z + percent
    print('progress: %f' % z)

    # Just initiates the connection to the switch
    device = ConnectHandler(device_type='cisco_nxos', ip=switches[i][0], username=secrets.nx_uid, password=secrets.nx_pass)
    # runs the command to the switch, stores in temp variable
    vlans_in_topo = device.send_command_expect("show fabricpath isis topology 0 vlan-range")

    # because VNI is not consistent, have to sense if this line exists, then adjust the parsing accordingly
    if "No VNI configured." in vlans_in_topo:
        # drops output to shell and iterates through via piping, not my favorite process but it works
        vlan2 = subprocess.Popen(["echo", vlans_in_topo], stdout=subprocess.PIPE)
        vlan3 = subprocess.Popen(["sed", "1,3d"], stdin=vlan2.stdout, stdout=subprocess.PIPE)
        vlan4 = subprocess.Popen(["sed", "$d"], stdin=vlan3.stdout, stdout=subprocess.PIPE)
        vlan5 = subprocess.Popen(["sed", "$d"], stdin=vlan4.stdout, stdout=subprocess.PIPE)
        # regex to recognize the commas
        pattern = re.compile("^\s+|\s*,\s*|\s+$")
        # creates an array where the output above gets split into array elements, including ranges
        # (i.e., 7-9 could exist)

        vlans = [x for x in pattern.split(vlan5.communicate()[0]) if x]

    else:
        # does same as above but with one less line removed from end
        vlan2 = subprocess.Popen(["echo", vlans_in_topo], stdout=subprocess.PIPE)
        vlan3 = subprocess.Popen(["sed", "1,3d"], stdin=vlan2.stdout, stdout=subprocess.PIPE)
        vlan4 = subprocess.Popen(["sed", "$d"], stdin=vlan3.stdout, stdout=subprocess.PIPE)
        pattern = re.compile("^\s+|\s*,\s*|\s+$")
        vlans = [x for x in pattern.split(vlan4.communicate()[0]) if x]
    # empty array where we will put individaul numbers into, breaking up ranges (i.e., splits up 7-9 into 7, 8, 9)
    array = []
    # iterates through the elements in the array vlan and adds individual numbers into the empty array
    for ele in vlans:
        if "-" in ele:
            l, r = ele.split("-")
            array.append(int(l))
            p = int(l) + 1
            while p < int(r):
                array.append(int(p))
                p = p + 1
            array.append(int(r))
        else:
            array.append(int(ele))

    array = str(array)

    new_file.write(switches[i][1] + ' = ' + array + '\n')
    new_file.write(switches[i][1] + '_set = set(' + switches[i][1] + ')' + '\n')

    i = i + 1

new_file.write("logfile = file('fabricpath_missing_from.txt', 'w')" + '\n')
new_file.write('i = 0' + '\n')

new_file.write('while i < 4096:' + '\n')
new_file.write('    i = i + 1' + '\n')
i = i - 1

new_file.write('    if i ')
j = 0
while j < i:
    new_file.write('not in ' + switches[j][1] + "_set and i ")
    j = j + 1
new_file.write('not in ' + switches[j][1] + '_set:' + '\n')
new_file.write('        logfile.write("no switches contain VLAN %i in topology 0 " % i)' + '\n')

new_file.write('    elif i ')
k = 0
while k < i:
    new_file.write('in ' + switches[k][1] + "_set and i ")
    k = k + 1
new_file.write('in ' + switches[k][1] + '_set:' + '\n')
new_file.write('        logfile.write("ALL SWITCHES CONTAIN VLAN %i IN TOPOLOGY 0 " % i)' + '\n')

new_file.write('    else:' + '\n')
new_file.write('        logfile.write("VLAN %i is in topology 0 missing from switches: " % i)' + '\n')
m = 0
while m < i:
    new_file.write('        if i not in ' + switches[m][1] + '_set:' + '\n')
    new_file.write('            logfile.write("' + switches[m][1] + ' ")' + '\n')
    m = m + 1
new_file.write('        if i not in ' + switches[m][1] + '_set:' + '\n')
new_file.write('            logfile.write("' + switches[m][1] + ' ")' + '\n')

new_file.write('    logfile.write("\\n")')

new_file.close()

os.system('python temp_script.py')

while True:
    try:
        os.remove('temp_script.py')
        break
    except:
        time.sleep(0.5)
