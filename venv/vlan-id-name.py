from netmiko import ConnectHandler

from py import secrets

vlans = [
    1,
    6,
    78,
    98,
    138,
    216,
    217,
    238,
    239,
    254,
    257,
    260,
    261,
    266,
    267,
    268,
    269,
    270,
    271,
    272,
    341,
    408,
    409,
    498,
    499,
    501,
    504,
    505,
    508,
    526,
    529,
    534,
    537,
    538,
    539,
    540,
    547,
    549,
    550,
    555,
    557,
    558,
    559,
    560,
    561,
    562,
    563,
    564,
    565,
    566,
    567,
    568,
    569,
    570,
    571,
    572,
    573,
    574,
    575,
    577,
    578,
    579,
    580,
    581,
    582,
    583,
    584,
    585,
    586,
    587,
    590,
    592,
    594,
    601,
    604,
    605,
    606,
    608,
    609,
    610,
    611,
    612,
    613,
    614,
    620,
    625,
    666,
    898,
    910,
    995,
    998,
    999,
    2254,
    2255,
    2258,
    2400,
    2410,
    2419,
    2420,
    2421,
    2422,
    3100,
    3101,
    3102,
    3103,
    3107,
    3108,
    3109,
    3110,
    3111,
    3112,
    3113,
    3114,
    3116,
    3117,
    3120,
    3121,
    3122,
    3123,
    3124,
    3125,
    3126,
    3127,
    3128,
    3130,
    3131,
    3132,
    3133,
    3134,
    3135,
    3136,
    3137,
    3138,
    3141,
    3142,
    3160,
    3161,
    3162,
    3170,
    3206,
    3207,
    3211,
    3222,
    3231,
    3250,
    3271,
    3570,
    3571,
    3572,
    3575,
    3589,
    3590,
    3595,
    3612

]

logfile = open('vlan-ID-output.txt', 'w')

device = ConnectHandler(
    device_type='cisco_nxos',
    ip='b06dc1.tele.iastate.edu',
    username=secrets.nx_uid,
    password=secrets.nx_pass
)

for vlan in vlans:
    output = device.send_command("sho run vlan %s" % vlan)
    logfile.write(output)
    logfile.write("\n")

logfile.close()
