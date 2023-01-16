from datetime import datetime
from netmiko import ConnectHandler
from py import nodes, secrets

i = 0

# Next three lines are for "time remaining" messages printed to screen as program runs
start_time = datetime.now()
total_parts = len(nodes.datacenterdevices)
completed_parts = 0

#

all_interfaces_down = 0
all_total_interfaces = 0
logfile = open('datacenter_interface_usage.csv', 'w')

logfile.write("Switch name,Interfaces in Use,Total Interfaces,Fill rate\n")

for switch in nodes.datacenterdevices:

    print("******************************")
    print("Starting switch %s." % nodes.datacenterdevices[i][1])

    logfile.write("%s," % nodes.datacenterdevices[i][1])
    # netmiko connection line
    device = ConnectHandler(
        device_type='cisco_nxos',
        ip=nodes.datacenterdevices[i][0],
        username=secrets.nx_uid,
        password=secrets.nx_pass
    )

    interfaces_down = device.send_command("show interface status down | grep Eth | count ")
    total_interfaces = device.send_command("show interface status | grep Eth | count ")
    all_interfaces_down = int(all_interfaces_down) + int(interfaces_down)
    all_total_interfaces = int(all_total_interfaces) + int(total_interfaces)
    interfaces_up = int(total_interfaces) - int(interfaces_down)
    interface_usage_percent_switch = float(100) - (float(100) * (float(interfaces_down) / float(total_interfaces)))
    print("******************************")
    logfile.write("%i,%s,%i%%\n" % (interfaces_up, total_interfaces, interface_usage_percent_switch))

    # ----------------------------------------------------------------------------------
    # Next block is for "time remaining" messages printed to screen as program runs
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
    # ----------------------------------------------------------------------------------

    i += 1

    # close logfile before opening next logfile

interface_usage_percent_all_switch = (
    float(100) - (float(100) * (float(all_interfaces_down) / float(all_total_interfaces)))
)
logfile.write("===================================================\n")
logfile.write("Interface Usage for all devices is %s%%\n" % interface_usage_percent_all_switch)
logfile.write("Total Interfaces in datacenter is %s" % all_total_interfaces)

logfile.close()
