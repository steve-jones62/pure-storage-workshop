from netmiko import ConnectHandler

# set un equal to your username
# set pw equal to your password
# set se to the secret password for enable mode
un = "admin"
pw = "cisco123!"
se = "Cisco123!"
ios_type = "cisco_xe"
ip_addr = "192.168.128.151"
new_vlan = "20"

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

# Build and send commands to build and name your VLAN

command1 = "vlan " + new_vlan 						#################### Space after ‘vlan’ is important!
command2 = "name " + un 							#################### Space after ‘name’ is important!

cmd_list = [command1, command2]        				#################### a list of commands is required

checkerror = net_connect.send_config_set(cmd_list)  #################### the send_config takes the list as an argument
net_connect.exit_config_mode()

if not 'Invalid' in checkerror:                     #################### send_config sets an error code on exit for testing
	print(command1 + " setup!") 					# Space before ‘setup’!
else:
	print("You failed to create the VLAN")
	exit()
#VLAN Created!
# Lets just prove it to ourselves
cmdoutput = net_connect.send_command('show vlan')
# 
print('************** Show the new VLAN *************')
print(cmdoutput)
print()

# Build and send commands to add your VLAN to active ports trunks
command2 = "switchport trunk allowed vlan " + new_vlan        # Space after 'add' important!

# Walk through interfacelist list and assign VLAN to trunk list
for interfacename in interfacelist:
     command1 = "interface " + interfacename        # Space after 'interface' important!
    
     cmd_list = [command1, command2]
     print(cmd_list)
     checkerror = net_connect.send_config_set(cmd_list)
     print(checkerror)                              ##### Pay attention here!!!
     net_connect.exit_config_mode()

     if not 'Invalid' in checkerror:
         print(command1 + " complete!")
     else:
         print("You failed to set the interface properly")

net_connect.disconnect()
exit()
