import base64, os, getpass

prompt_nx_uid = input("Nexus User ID: ")
prompt_cat_uid = input("TACACS User ID: ")
prompt_ad_uid = input("Active Directory User ID: ")

nx = 0
while True:
    prompt_nx_pass = getpass.getpass(prompt="Nexus Password: ")
    prompt_nx_pass2 = getpass.getpass(prompt="Re-enter Nexus Password: ")
    if prompt_nx_pass == prompt_nx_pass2:
        break
    nx += 1
    if nx > 4:
        print("Maximum retries attempted.")
        exit()
    print("Your passwords did not match, please try again.")

cat = 0
while True:
    prompt_cat_pass = getpass.getpass(prompt="TACACS Password: ")
    prompt_cat_pass2 = getpass.getpass(prompt="Re-enter TACACS Password: ")
    if prompt_cat_pass == prompt_cat_pass2:
        break
    cat += 1
    if cat > 4:
        print("Maximum retries attempted.")
        exit()
    print("Your passwords did not match, please try again.")

ad = 0
while True:
    prompt_ad_pass = getpass.getpass(prompt="Active Directory Password: ")
    prompt_ad_pass2 = getpass.getpass(prompt="Re-enter Active Directory Password: ")
    if prompt_ad_pass == prompt_ad_pass2:
        break
    ad += 1
    if ad > 4:
        print("Maximum retries attempted.")
        exit()
    print("Your passwords did not match, please try again.")

nx_uid = base64.b64encode(prompt_nx_uid.encode('ascii'))
cat_uid = base64.b64encode(prompt_cat_uid.encode('ascii'))
ad_uid = base64.b64encode(prompt_ad_uid.encode('ascii'))
nx_pass = base64.b64encode(prompt_nx_pass.encode('ascii'))
cat_pass = base64.b64encode(prompt_cat_pass.encode('ascii'))
ad_pass = base64.b64encode(prompt_ad_pass.encode('ascii'))

path = "py"
try:
    os.makedirs(path)
except OSError:
    if not os.path.isdir(path):
        raise

logfile = open('py/secrets.py', 'w')

logfile.write("import base64\n")
logfile.write('nx_uid = base64.b64decode("%s")\n' % nx_uid)
logfile.write('cat_uid = base64.b64decode("%s")\n' % cat_uid)
logfile.write('ad_uid = base64.b64decode("%s")\n' % ad_uid)
logfile.write('nx_pass = base64.b64decode("%s")\n' % nx_pass)
logfile.write('cat_pass = base64.b64decode("%s")\n' % cat_pass)
logfile.write('ad_pass = base64.b64decode("%s")\n' % ad_pass)

logfile.close()

view = input("View your passwords? (y or n) ")

if view == "y":
    print (prompt_nx_pass)
    print (prompt_cat_pass)
    print (prompt_ad_pass)
    print ("Document created")
    print ("If these are incorrect, please re-run this script.")
else:
    print ("Document created")
