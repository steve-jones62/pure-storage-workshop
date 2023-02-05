from netmiko import ConnectHandler
# set un equal to your username
# set pw equal to your password
un = "admin"
pw = "cisco123!"
ios_type = "cisco_xe"
ip_addr = "192.168.128.151"

net_connect = ConnectHandler(device_type=ios_type, ip=ip_addr, username=un, password=pw)
output = net_connect.send_command('show ip int brief | include up')
print(output)
net_connect.disconnect()
exit()