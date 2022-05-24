import sys
import pexpect
from py import secrets

switch = str(sys.argv[1])
timer = 20

child = pexpect.spawn('ssh %s@%s' % (secrets.cat_uid, switch))
child.timeout = 90

while True:

    i = child.expect(
        [
            'Are you sure you want to continue connecting*',
            '.*assword:.*|.*ASSWORD:.*|Enter PASSCODE*',
            '.*#.*',
            'USERNAME:*',
            '.*>.*',
            pexpect.EOF,
            pexpect.TIMEOUT
        ],
        timeout=timer
    )

    if i == 0:
        child.sendline("yes")
    elif i == 1:
        child.sendline(secrets.cat_pass)
    elif i == 2:
        child.sendline("terminal length 0")
        break
    elif i == 3:
        child.sendline(secrets.cat_uid)
    elif i == 4:
        child.sendline("enable")
        child.sendline(secrets.cat_pass)
        break
    elif i == 5:
        exit()
    elif i == 6:
        exit()

child.interact()
