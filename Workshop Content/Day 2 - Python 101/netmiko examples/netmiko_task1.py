from netmiko import ConnectHandler

cisco_cloud_router = {'device_type': 'cisco_ios',
                      'ip': '10.1.2.101',
                      'username': 'ignw',
                      'password': 'password'}
connection = ConnectHandler(**cisco_cloud_router)

# print(connection)
# print(type(connection))

interface_output = connection.send_command('show run int g1')
# print(interface_output)

hostname = connection.find_prompt()
# print(hostname[:-1])

interface_name = connection.send_command('show run int g1 | i ^interface')
# print(interface_name)

ip_output = connection.send_command('show run int g1 | i ip address')
if 'no' in ip_output:
    interface_ip_address = []
    interface_ip_address[0] = 'N/A'
else:
    interface_ip_address = []
    for line in ip_output.split('\n'):
        interface_ip_address.append(line[12:])
print(interface_ip_address)

interface_description = connection.send_command('show run int g1 | i des')
if not interface_description:
    interface_description = 'N/A'
print(interface_description)
