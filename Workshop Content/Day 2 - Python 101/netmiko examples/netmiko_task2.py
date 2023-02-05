from netmiko import ConnectHandler

cisco_cloud_router = {'device_type': 'cisco_ios',
                      'ip': '10.1.2.101',
                      'username': 'ignw',
                      'password': 'password'}
connection = ConnectHandler(**cisco_cloud_router)

commands = ['interface loopback0',
            'description I made this with Python!',
            'ip address 10.255.255.1 255.255.255.255',
            'no shut']

connection.config_mode()
connection.send_config_set(commands)
connection.send_command('wr')

show_output = connection.send_command('show ip int loopback0 | i Loopback0')
if show_output.count('up') == 2:
    print('It looks like loopback0 is "up/up"! Way to go!')
