from py import nodes

switches = []

question = raw_input("Will you use all fabricpath devices, all datacenter devices, all node devices? \n"
                  "Respond with 'all', 'datacenter', 'node' or 'other' - note, if you select datacenter or node,\n"
                  "you will be prompted to determine if you want individual devices from the other group.")

if question == "all":
    for switch in nodes.alldevices:
        switches.append(switch)

elif question == "datacenter":

    for switch in nodes.datacenterdevices:
        switches.append(switch)

    noderooms = raw_input("Will you use devices in node rooms? (y or n)")
    if noderooms == "y":
        i = 0
        for switch in nodes.noderoomdevices:
            noderoom = raw_input("Will you use %s?" % nodes.noderoomdevices[i][1])
            if noderoom == "y":
                switches.append(switch)
            elif noderoom == "n":
                print ("skipping %s" % nodes.noderoomdevices[i][1])
            else:
                print('input incorrect, responses may only be "y" or "n".')
                break
            i += 1
    elif noderooms == "n":
        print('no node room devices will be added')
    else:
        print('input incorrect, responses may only be "y" or "n".')

elif question == "node":

    for switch in nodes.noderoomdevices:
        switches.append(switch)

    datacenters = raw_input("Will you use devices in the datacenter? (y or n)")
    if datacenters == "y":
        i = 0
        for switch in nodes.datacenterdevices:
            noderoom = raw_input("Will you use %s?" % nodes.datacenterdevices[i][1])
            if noderoom == "y":
                switches.append(switch)
            elif noderoom == "n":
                print ("skipping %s" % nodes.datacenterdevices[i][1])
            else:
                print('input incorrect, responses may only be "y" or "n".')
                break
            i += 1
    elif datacenters == "n":
        print('no datacenter devices will be added')
    else:
        print('input incorrect, responses may only be "y" or "n".')

elif question == "other":
    print("You have selected 'other', you will be able to select any device to use.")
    i = 0
    for switch in nodes.alldevices:
        noderoom = raw_input("Will you use %s?" % nodes.alldevices[i][1])
        if noderoom == "y":
            switches.append(switch)
        elif noderoom == "n":
            print ("skipping %s" % nodes.alldevices[i][1])
        else:
            print('input incorrect, responses may only be "y" or "n".')
            break
        i += 1


else:
    print("input incorrect, responses must be 'all', 'datacenter', 'node' or 'other'.")


print(switches)
