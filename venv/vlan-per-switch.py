from datetime import datetime
from netmiko import ConnectHandler
from py import nodes, secrets

switches = nodes.datacenterdevices

i = 0

percent = float(100)/float(len(switches))
y = 0

total_parts = len(switches)
completed_parts = 0
start_time = datetime.now()
for switch in switches:

    print("******************************")
    print("Starting switch %s." % switches[i][1])
    print("******************************")

    nxos_config = {
        'device_type': 'cisco_nxos',
        'ip': switches[i][0],
        'username': secrets.nx_uid,
        'password': secrets.nx_pass,
        'global_delay_factor': 0.25,
    }

    device = ConnectHandler(**nxos_config)

    logfile = file('%s.txt' % switches[i][1], 'w')

    output = device.send_command("sho vlan brief | inc active | cut -c -37")  #
    logfile.write("%s" % output)

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

    logfile.close()
