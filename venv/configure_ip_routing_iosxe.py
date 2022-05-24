"""
This script does the following:
- Creates two log files, one for error handling and one to record successful changes.
- Parses a file with a list of Cisco IOS-XE switches (one per line).
- Logs into each switch with stored credentials, enters enable mode if necessary.
- Finds switch's default-gateway IP.
- Creates static route to named default-gateway IP.
- Turns on IP routing
- Deletes default-gateway.
After each change, the script will test to ensure the switch "sees" the changes that
have been made. Any failure along the way will stop the script from making further
changes to the switch and error messages will be recorded in the "failure log".

Version 1.0 - TJ Wertz 5-22-2022; twertz@iastate.edu
"""


import re
from netmiko import ConnectHandler
from py import secrets

document = open('switches.txt', 'r')
success_log = open('success_log.txt', 'a+')
failure_log = open('failure_log.txt', 'a+')

switches = document.read().splitlines()


def test_switch_output(switch_output, test_string, command_string, switch_name, match=True):
    """
    test_switch_output will take output from the switch and ensure it matches the expected response.
    The function will record successes and failures in the appropriate log file. If the test requires
    that the two values not match, the match value can be overridden with a "False" statement.
    """
    if match == True:
        if switch_output == test_string:
            success_log.write("%s successfully implemented on %s" % (command_string, switch_name))
        else:
            failure_log.write("%s failed validation on %s" % (command_string, switch_name))
            print("%s failed validation on %s" % (command_string, switch_name))
            return "FAIL"
    else:
        if switch_output != test_string:
            success_log.write("%s successfully implemented on %s" % (command_string, switch_name))
        else:
            failure_log.write("%s failed validation on %s" % (command_string, switch_name))
            print("%s failed validation on %s" % (command_string, switch_name))
            return "FAIL"


def find_ip_in_string(string, switch_name):
    """
    find_ip_in_string takes a string, divides it into elements in an array, then looks for an IP and returns that.
    Alternatively, the function will return a statement if the string is empty or if there isn't a valid IP.
    """
    list_of_words = []
    for word in string.split():
        list_of_words.append(word)
    ip_in_string = re.match(
        r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',
        list_of_words[2]
    )
    if ip_in_string:
        success_log.write("Default gateway successfully identified for %s" % switch_name)
        return ip_in_string.group()
    else:
        failure_log.write("No Valid IP Found in %s for %s" % (string, switch_name))
        print("No Valid IP Found in %s for %s" % (string, switch_name))
        return "FAIL"


for switch in switches:
    start_text = "\n==================STARTING SWITCH %s==================\n" % switch
    print(start_text)
    success_log.write(start_text)
    failure_log.write(start_text)
    connection = ConnectHandler(
        device_type='cisco_xe',
        host=switch,
        username=secrets.cat_uid,
        password=secrets.cat_pass,
        secret=secrets.cat_pass
    )
    connection.enable()

    show_run_default_gateway = connection.send_command("show running-config | include ip default-gateway")
    show_run_default_gateway_test = test_switch_output(
        len(show_run_default_gateway),
        0,
        "show running-config | include ip default-gateway",
        switch,
        False
    )
    if show_run_default_gateway_test == "FAIL":
        continue

    gateway_ip = find_ip_in_string(show_run_default_gateway, switch)
    if gateway_ip == "FAIL":
        continue

    # ip_route_configuration_set = [
    #     "ip route 0.0.0.0 0.0.0.0 %s" % gateway_ip,
    #     ]
    # connection.send_config_set(ip_route_configuration_set)

    show_run_ip_route = connection.send_command("show running-config | include ip route")
    show_run_ip_route_test = test_switch_output(
        show_run_ip_route,
        "ip route 0.0.0.0 0.0.0.0 %s" % gateway_ip,
        "show running-config | include ip route",
        switch,
    )
    if show_run_ip_route_test == "FAIL":
        continue

    # ip_routing_configuration_set = [
    #     "ip routing"
    # ]
    # connection.send_config_set(ip_routing_configuration_set)

    show_run_ip_routing = connection.send_command("show running-config | include ip routing")
    show_run_ip_routing_test = test_switch_output(
        show_run_ip_routing,
        "ip routing",
        "show running-config | include ip routing",
        switch,
    )
    if show_run_ip_routing_test == "FAIL":
        continue

    # remove_default_gateway_configuration_set = [
    #     "no ip default-gateway %s" % gateway_ip
    # ]
    # connection.send_config_set(remove_default_gateway_configuration_set)

    show_run_default_gateway = connection.send_command("show running-config | include ip default-gateway")
    test_switch_output(
        len(show_run_default_gateway),
        0,
        "show running-config | include ip default-gateway",
        switch,
    )
    if show_run_default_gateway == "FAIL":
        continue

document.close()
success_log.close()
failure_log.close()

complete_text = "\n==================ALL SWITCHES COMPLETE==================\n"
print(complete_text)
