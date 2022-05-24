from netmiko import ConnectHandler
from py import secrets

subnets = [
    6,
    78,
    138,
    238,
    254,
    260,
    547,
    557,
    558,
    3101,
    3102,
    3104,
    3105,
    3107,
    3108,
    3114,
    3124,
    3128,
    3130,
    3131,
    3132,
    3138,
    3141,
    3160,
    3162,
    3206,
    3589,
    3590,
    3612,
    572,
    3572,
    570,
    3570,
    571,
    3571,
    575,
    3575,
    995,
    3595,
    2254,
    2258,
    2410,
    2419,
    2420,
    2421,
    2422
]

logfile = file('output.txt', 'w')

nxos_config = {
    'device_type': 'cisco_nxos',
    'ip': 'b06dc1.tele.iastate.edu',
    'username': secrets.nx_uid,
    'password': secrets.nx_pass,
    'global_delay_factor': 0.25,
}

device = ConnectHandler(**nxos_config)

total = 0

for subnet in subnets:

    output = device.send_command("sho run int subnet %i | grep 'ip address' | count" % subnet)
    output2 = int(output)
    logfile.write("subnet %i has %i subnet(s)\n" % (subnet, output2))
    total = total + output2

logfile.write("%i total subnets" % total)
logfile.close()
