import re
import subprocess
from datetime import datetime
from netmiko import ConnectHandler
from py import nodes, secrets

# FQDN name and a "common" name for each switch. the "common" name helps shorten output,
# whereas the FQDN name is needed for the connection

switches = nodes.datacenterdevices

vlans = [
    3103
]

i = 0

logfile = open('Topology-cleanup.txt', 'w')

percent = float(100)/float(len(switches))
percentage = percent/float(len(vlans))
y = 0

start_time = datetime.now()

total_parts = len(switches) * len(vlans)
completed_parts = 0

# iterate through the switches to get the arrays built with the
for switch in switches:

    print("******************************")
    print("Starting switch %s." % switches[i][1])
    print("******************************")

    # Just initiates the connection to the switch
    nxos_config = {
        'device_type': 'cisco_nxos',
        'ip': switches[i][0],
        'username': secrets.nx_uid,
        'password': secrets.nx_pass,
        'global_delay_factor': 0.25,
    }

    device = ConnectHandler(**nxos_config)

    logfile.write('------------------------------------------------------------------- \n')
    logfile.write('%s vlan\n' % (switches[i][1]))
    logfile.write('------------------------------------------------------------------- \n')

    for vlan in vlans:

        y = y + percentage
        print('progress: %f' % y)

        # runs the command to the switch, stores in temp variable
        port = device.send_command_expect("sho vlan id %i" % vlan, delay_factor=0.25)

        # drops output to shell and iterates through via piping, not my favorite process but it works
        port2 = subprocess.Popen(["echo", port], stdout=subprocess.PIPE)
        port3 = subprocess.Popen(["sed", "1,3d"], stdin=port2.stdout, stdout=subprocess.PIPE)
        port4 = subprocess.Popen(["cut", "-c", "49-80"], stdin=port3.stdout, stdout=subprocess.PIPE)
        port5 = subprocess.Popen(["sed", "$d"], stdin=port4.stdout, stdout=subprocess.PIPE)
        port6 = subprocess.Popen(["sed", "$d"], stdin=port5.stdout, stdout=subprocess.PIPE)
        port7 = subprocess.Popen(["sed", "$d"], stdin=port6.stdout, stdout=subprocess.PIPE)
        port8 = subprocess.Popen(["sed", "$d"], stdin=port7.stdout, stdout=subprocess.PIPE)
        port9 = subprocess.Popen(["sed", "$d"], stdin=port8.stdout, stdout=subprocess.PIPE)
        port10 = subprocess.Popen(["sed", "$d"], stdin=port9.stdout, stdout=subprocess.PIPE)
        port11 = subprocess.Popen(["sed", "$d"], stdin=port10.stdout, stdout=subprocess.PIPE)
        port12 = subprocess.Popen(["sed", "$d"], stdin=port11.stdout, stdout=subprocess.PIPE)
        port13 = subprocess.Popen(["sed", "$d"], stdin=port12.stdout, stdout=subprocess.PIPE)
        port14 = subprocess.Popen(["sed", "$d"], stdin=port13.stdout, stdout=subprocess.PIPE)

        pattern = re.compile("^\s+|\s*,\s*|\\n|\s+$")

        port_array = [x for x in pattern.split(port14.communicate()[0]) if x]

        fp_ports = []
        ce_ports = []

        for port in port_array:
            output = device.send_command_expect("show run interface %s" % port, delay_factor=0.25)
            if "mode fabricpath" in output:
                fp_ports.append(port)
            else:
                ce_ports.append(port)

        if not fp_ports:
            logfile.write("For VLAN %s on %s, no Fabricpath ports exist. \n" % (vlan, switches[i][1]))
        else:
            logfile.write("For VLAN %s on %s, Fabricpath ports exist on %s \n" % (vlan, switches[i][1], fp_ports))
        if not ce_ports:
            logfile.write("For VLAN %s on %s, no Classic Ethernet Ports \n" % (vlan, switches[i][1]))
        else:
            logfile.write("For VLAN %s on %s, Classic Ethernet ports exist on %s \n" % (vlan, switches[i][1], ce_ports))

        completed_parts += 1
        current_time = datetime.now()
        et = current_time - start_time
        elapsed_time = et.seconds
        estimated_time = elapsed_time * total_parts / completed_parts
        time_to_completion = estimated_time - elapsed_time
        hours = time_to_completion / 3600
        minutes = (time_to_completion % 3600) / 60
        seconds = (time_to_completion % 3600) % 60
        print("Time left %i hours, %i minutes, and %i seconds" % (hours, minutes, seconds))

    i += 1
