import re
from py import nodes, secrets
from netmiko import ConnectHandler

# array for all datacenter switches
switches = nodes.datacenterdevices

# one switch for testing, commented out when not testing
# switch = 'b06dc1.tele.iastate.edu'

for switch in switches:
    # log for each switch
    logfile = file('%s.txt' % switch, 'w')
    # use netmiko to log into switches
    device = ConnectHandler(
        device_type='cisco_nxos',
        ip=switches[i][0],
        username=secrets.nx_uid,
        password=secrets.nx_pass
    )
    # have to use fabricpath isis command to get "active" vlans from switch. The first sed cuts the first 3 lines, the
    # rest of the seds cut the last line (cant be done together)
    vlans_in_topo_6 = device.send_command_expect(
        "show fabricpath isis topology 6 vlan-range | sed '1,3d' | sed '$d' | sed '$d'"
    )
    # have to use regex to get rid of spaces, etc
    pattern = re.compile("^\s+|\s*,\s*|\s+$")
    # this is mostly google-fu to find how to properly split the list for the array
    vlans = [x for x in pattern.split(vlans_in_topo_6) if x]
    # this is a secondary empty array that we build in the for-in loop
    array = []

    # this loop analyzes the elements of the original array to find where it has to split data and where it has to
    # simply copy data from one array to the new one
    for ele in vlans:
        # looking for a "-" to know I need to expand that element, if no "-" exists, it goes straight into the new array
        if "-" in ele:
            # l for left and r for right, these get seperated at the "-"
            l, r = ele.split("-")
            # adding the l, or first datapoint as an array element
            array.append(int(l))
            # bring in i to increment up, make it same as l plus one (next number)
            i = int(l) + 1
            # while loop creates rest of numbers in array by adding element to array then incrementing by one, stops
            # before it is equal to the value of r
            while i < int(r):
                array.append(int(i))
                i = i + 1
            # put the value of r into new array
            array.append(int(r))
            # if there is no "-" above indicating it is a single number, loop drops to here and just puts the element
            # the new array
        else:
            array.append(int(ele))

    # wouldn't let me put integers directly into the array, they had to go in as string or it threw an exception:
    # TypeError: int() argument must be a string or a number, not 'list'
    # it will store the data in the array but you can't write to the logfile without the next two lines... weird.
    array = str(array)
    logfile.seek(0)

    # write output of array to logfile for external consumption
    logfile.write(array)
    logfile.close()
