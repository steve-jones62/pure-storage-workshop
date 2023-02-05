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

interfacelist=[ ]		                ######################### NEW ############################

# connect to switch
net_connect = ConnectHandler(device_type=ios_type, ip=ip_addr, username=un, password=pw, secret=se)
net_connect.enable()
cmdoutput = net_connect.send_command('show ip int brief | include up')
# Lets see the raw output
print('************** The raw output from the command *************')
print(cmdoutput)
print()


outputlist = cmdoutput.split() 	        ######################### NEW ############################
# Lets see the parsed output
print('************** The parsed output from the command *************')
print(outputlist)
print()


for eachword in outputlist:
	if 'Gi' in eachword:
		interfacelist.append(eachword)
print("Output of interfacelist list:")
print('*' * 70)
print(interfacelist)
print('*' * 70)