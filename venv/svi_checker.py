from datetime import datetime
from netmiko import ConnectHandler
from py import nodes, secrets

vlans = [
    409
]

switches = nodes.alldevices

i = 0

percent = float(100)/float(len(switches))
percentage = percent/float(len(vlans))
y = 0

start_time = datetime.now()

total_parts = len(switches) * len(vlans)
completed_parts = 0

logfile = open('SVI_LOCATION.txt', 'w')

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

    for vlan in vlans:
        output = device.send_command("sho ip int brief vrf all | i 'Vlan%s '" % vlan)

        if "Vlan" in output:

            logfile.write("VLAN %s \n" % vlan)
            logfile.write("%s - " % switches[i][1])
            logfile.write("%s \n" % output)
            print("%s \n" % output)

        else:
            logfile.write("%s \n" % switches[i][1])
            logfile.write("SVI not found \n")
            print("SVI not found")

        logfile.write("******************* \n")

        y = y + percentage
        print('progress: %f' % y)
        # ---------------------------------------------------------------------------------------
        # time to completion script
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
        # ---------------------------------------------------------------------------------------

    i += 1

logfile.close()
