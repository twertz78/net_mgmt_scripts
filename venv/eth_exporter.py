from netmiko import ConnectHandler
from datetime import datetime
from py import secrets

switches = [
    ['b31nx0.tele.iastate.edu', 'b31nx0'],
    ['e63nx0.tele.iastate.edu', 'e63nx0'],
    ['b11nx0.tele.iastate.edu', 'b11nx0'],
    ['c12nx0.tele.iastate.edu', 'c12nx0'],
    ['e01nx0.tele.iastate.edu', 'e01nx0'],
    ['m22nx0.tele.iastate.edu', 'm22nx0'],
    ['h13nx1.tele.iastate.edu', 'h13nx1'],
    ['s07nx1.tele.iastate.edu', 's07nx1'],
    ['rtr-b31nx6-vdc0.tele.iastate.edu', 'rtr-b31nx6-vdc0'],
    ['rtr-e63nx6-vdc0.tele.iastate.edu', 'rtr-e63nx6-vdc0'],
    ['b31core0.tele.iastate.edu', 'b31core'],
    ['e63core0.tele.iastate.edu', 'e63core']

]

server = "twertz@10.10.138.100/home/twertz"

i = 0

for switch in switches:

    date = datetime.date(datetime.now())

    print("******************************")
    print("Starting switch %s." % switches[i][1])
    print("******************************")

    device = ConnectHandler(
        device_type='cisco_nxos',
        ip=switches[i][0],
        username=secrets.nx_uid,
        password=secrets.nx_pass
    )

    filename = ("%s_eth_%s" % (date, switches[i][1]))

    p = 0
    while p < 5:

        print("Starting ethanalyzer")
        start_ethanalyzer = [
            "ethanalyzer local interface inband limit-captured-frames 20000 write bootflash:%s" % filename
        ]
        device.send_config_set(start_ethanalyzer)

        print("Zipping file")
        zip_file = [
            "gzip bootflash:%s" % filename
        ]
        zip_name = ("%s.gz" % filename)

        device.send_config_set(zip_file)

        print("Copying to SCP server")
        export = [
            "copy bootflash:%s scp://%s vrf default" % (zip_name, server)
        ]
        device.send_config_set(export)

        print("Deleting zipped file")
        delete_zip = [
            "delete:%s" % zip_name
        ]
        device.send_config_set(delete_zip)

        p += 1

    i += 1
