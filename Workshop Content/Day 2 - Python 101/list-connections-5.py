from netmiko import ConnectHandler

# set un equal to your username
# set pw equal to your password
# set se to the secret password for enable mode
un = "admin"
pw = "cisco123!"
se = "Cisco123!"
ios_type = "cisco_xe"
ip_addr = "192.168.128.151"

net_connect = ConnectHandler(device_type=ios_type, ip=ip_addr, username=un, password=pw, secret=se)

# First, test initial login prompt
output = net_connect.find_prompt()	# 'LAB'>’ – Returns the current prompt as Unicode string - note prompt
print("this is the login prompt")
print(output)
checkerror = net_connect.find_prompt()
if not '#' in checkerror:
	print("Not in Enable Mode!")
else:
	print("You are in Enable Mode")

print()
print("*************************************")
print()

# Now, go into enable mode and test again 
net_connect.enable()
output = net_connect.find_prompt()	# 'LAB'#’ – Returns the current prompt as Unicode string - note enable prompt
print("Is this the enable prompt?")
print(output)
checkerror = net_connect.find_prompt()
if not '#' in checkerror:
	print("Error - Not in Enable Mode!")
else:
	print("You are in Enable Mode")
 

net_connect.disconnect()
exit()

