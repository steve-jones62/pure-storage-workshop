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

output = net_connect.find_prompt()	# 'LAB'>’ – Returns the current prompt as Unicode string - note prompt
print("this is the login prompt")
print(output)
net_connect.enable()
output = net_connect.find_prompt()	# 'LAB'#’ – Returns the current prompt as Unicode string - note enable prompt
print("This is the enable prompt")
print(output)

net_connect.disconnect()
exit()