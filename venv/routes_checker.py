from datetime import datetime

from netmiko import ConnectHandler

from py import secrets

switches = [
    ['m22dc1.tele.iastate.edu', 'M22DC1'],
    ['b06dc1.tele.iastate.edu', 'B06DC1'],
    ['b31nx1.tele.iastate.edu', 'b31nx1'],
    ['e63nx2.tele.iastate.edu', 'e63nx2'],
    ['b31nx2.tele.iastate.edu', 'b31nx2'],
    ['e63nx1.tele.iastate.edu', 'e63nx1'],
    ['b11nx2.tele.iastate.edu', 'b11nx2'],
    ['b11nx1.tele.iastate.edu', 'b11nx1'],
    ['c12nx2.tele.iastate.edu', 'c12nx2'],
    ['c12nx1.tele.iastate.edu', 'c12nx1'],
    ['e01nx2.tele.iastate.edu', 'e01nx2'],
    ['e01nx1.tele.iastate.edu', 'e01nx1'],
    ['m22nx2.tele.iastate.edu', 'm22nx2'],
    ['m22nx1.tele.iastate.edu', 'm22nx1'],
    ['h13nx1.tele.iastate.edu', 'h13nx1'],
    ['s07nx1.tele.iastate.edu', 's07nx1'],
    ['b31nx3.tele.iastate.edu', 'b31nx3'],
    ['e63nx3.tele.iastate.edu', 'e63nx3'],
    ['b31nx4.tele.iastate.edu', 'b31nx4'],
    ['b31nx5.tele.iastate.edu', 'b31nx5'],
    ['e63core.tele.iastate.edu', 'e63core'],
    ['b31core.tele.iastate.edu', 'b31core'],
    ['b31dmztest.tele.iastate.edu', 'b31dmztest'],
    ['e63dmztest.tele.iastate.edu', 'e63dmztest'],
    ['rtr-b31nx6-vdc1.tele.iastate.edu', 'b31nx6'],
    ['rtr-e63nx6-vdc1.tele.iastate.edu', 'e63nx6']

]

i = 0

start_time = datetime.now()

total_parts = len(switches)
completed_parts = 0

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

    logfile = open('%s.txt' % switches[i][1], 'w')

    show_run = device.send_command("show run all")
    # ip_routes = device.send_command("show ip route sum vrf all")
    # ipv6_routes = device.send_command("show ipv6 route sum vrf all")
    # ip_mroutes = device.send_command("show ip mroute sum vrf all")
    # ipv6_mroutes = device.send_command("show ipv6 mroute sum vrf all")
    # mac_address = device.send_command("show mac address-table count")
    # acl_sum = device.send_command("show access-lists summary")

    logfile.write("%s: \n\n\n" % switches[i][1])
    logfile.write("*****************************************")
    # logfile.write("\n\n\nshow ip route summary vrf all\n")
    # logfile.write("%s \n\n\n" % ip_routes)
    logfile.write("\n\n\nshow run all\n")
    logfile.write("%s \n\n\n" % show_run)
    # logfile.write("*****************************************")
    # logfile.write("\n\n\nshow ipv6 route summary vrf all\n")
    # logfile.write("%s \n\n\n" % ipv6_routes)
    # logfile.write("*****************************************")
    # logfile.write("\n\n\nshow ip mroute summary vrf all\n")
    # logfile.write("%s \n\n\n" % ip_mroutes)
    # logfile.write("*****************************************")
    # logfile.write("\n\n\nshow ipv6 mroute summary vrf all\n")
    # logfile.write("*****************************************")
    # logfile.write("\n\n\nshow mac address-table count\n")
    # logfile.write("%s \n\n\n" % mac_address)
    # logfile.write("*****************************************")
    # logfile.write("\n\n\nshow access-lists summary\n")
    # logfile.write("%s \n\n\n" % acl_sum)
    # logfile.write("*****************************************")
    # logfile.write("\n\n\n")

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
