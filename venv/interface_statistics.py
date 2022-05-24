from datetime import datetime
from netmiko import ConnectHandler
from py import nodes, secrets
import re
import time
import sys
import csv

# block for allowing simple entries as argument to get router pairs
# -------------------------------------------------------------------------------------
# devices to run commands against, first part is FQDN, second part is for a "common" name
topology = int(sys.argv[1])
if topology == 31:
    switches = nodes.b31e63
elif topology == 63:
    switches = nodes.e63b31
elif topology == 11:
    switches = nodes.b11c12
elif topology == 12:
    switches = nodes.c12b11
elif topology == 22:
    switches = nodes.m22e01
elif topology == 1:
    switches = nodes.e01m22
elif topology == 7:
    switches = nodes.s07h13
elif topology == 35:
    switches = nodes.b31nx3e63nx3
elif topology == 20:
    switches = nodes.b31nx5
elif topology == 29:
    switches = nodes.be
elif topology == 0:
    switches = nodes.core
elif topology == 6:
    switches = nodes.datacenterdevices
else:
    sys.exit(
        "Your topology selection was not valid, please use 0 for core or 31, 63, 11, 12, 22, 1, 7, 35, 20, 29, or 6"
    )
# -------------------------------------------------------------------------------------
i = 0
# iterate through each switch

for switch in switches:
    # create logfile
    # logfile = file('%s_interface_statistics.csv' % switches[i][1], 'w')
    # screen ouput
    print("******************************")
    print("Starting switch %s." % switches[i][1])
    print("******************************")
    # variable in order to log into switch
    nxos_config = {
        'device_type': 'cisco_nxos',
        'ip': switches[i][0],
        'username': secrets.nx_uid,
        'password': secrets.nx_pass,
        'global_delay_factor': 0.25,
    }
    # creates connection to device
    device = ConnectHandler(**nxos_config)

    # Gather the first interface statistics
    # -------------------------------------------------------------------------------------
    array_t_1 = []
    output_1 = device.send_command("show interface")
    output_array_1 = []
    timestamp_1 = datetime.now()
    for line in iter(output_1.splitlines()):
        output_array_1.append(line)
    n = 0
    m = 0
    for line in output_array_1:
        if re.search('^(Ethernet[0-9]/[0-9]|port-channel[0-9])', line):
            array_t_1.append([])
            array_t_1[m].append(line)
        elif re.search('RX', line):
            words = []
            nextline = output_array_1[n + 1]
            for word in iter(nextline.split()):
                words.append(word)
            array_t_1[m].append(words[0])
            array_t_1[m].append(words[3])
            array_t_1[m].append(words[6])
            m += 1
        n += 1
    # -------------------------------------------------------------------------------------

    # wait 30 seconds (may change later to make variable)
    time.sleep(30)

    # Gather the second interface statistics
    # -------------------------------------------------------------------------------------
    array_t_2 = []
    output_2 = device.send_command("show interface")
    output_array_2 = []
    timestamp_2 = datetime.now()
    for line in iter(output_2.splitlines()):
        output_array_2.append(line)
    n = 0
    m = 0
    for line in output_array_2:
        if re.search('^(Ethernet[0-9]/[0-9]|port-channel[0-9])', line):
            array_t_2.append([])
            array_t_2[m].append(line)
        elif re.search('RX', line):
            words = []
            nextline = output_array_2[n + 1]
            for word in iter(nextline.split()):
                words.append(word)
            array_t_2[m].append(words[0])
            array_t_2[m].append(words[3])
            array_t_2[m].append(words[6])
            m += 1
        n += 1
    # -------------------------------------------------------------------------------------

    # This block generates the output
    # -------------------------------------------------------------------------------------
    p = 0
    time_interval = timestamp_2 - timestamp_1
    seconds_interval = time_interval.seconds
    print("%i seconds measured interval" % seconds_interval)
    logfile = open('%s_interface_statistics.csv' % switches[i][1], 'w')
    logfile.write("%s in %i seconds,Unicast,Multicast,Broadcast\n" % (switches[i][1], seconds_interval))
    for element in array_t_1:
        print array_t_1[p][0]
        unicast_per_second = ((int(array_t_2[p][1]) - int(array_t_1[p][1])) / seconds_interval)
        multicast_per_second = ((int(array_t_2[p][2]) - int(array_t_1[p][2])) / seconds_interval)
        broadcast_per_second = ((int(array_t_2[p][3]) - int(array_t_1[p][3])) / seconds_interval)
        print("%i unicast packets per second " % unicast_per_second)
        print("%i multicast packets per second" % multicast_per_second)
        print("%i broadcast packets per second" % broadcast_per_second)

        # writes each line to the CSV
        with open('%s_interface_statistics.csv' % switches[i][1], 'a') as logfile:
            headers = [
                'Interface',
                'Unicast',
                'Multicast',
                'Broadcast'
            ]
            writer = csv.DictWriter(logfile, fieldnames=headers, lineterminator='\n')
            writer.writerow(
                {
                    'Interface': array_t_1[p][0],
                    'Unicast': unicast_per_second,
                    'Multicast': multicast_per_second,
                    'Broadcast': broadcast_per_second
                }
            )
        p += 1
    # -------------------------------------------------------------------------------------

    i += 1
