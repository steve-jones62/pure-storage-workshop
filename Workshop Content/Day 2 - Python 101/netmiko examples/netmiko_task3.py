import sys
import time
from netmiko import ConnectHandler


cisco_cloud_router = {'device_type': 'cisco_ios',
                      'ip': '10.1.2.101',
                      'username': 'ignw',
                      'password': 'password'}

connection = ConnectHandler(**cisco_cloud_router)

commands = ['interface loopback1',
            'description IGNW was here!',
            'ip address 10.1.255.1 255.255.255.255',
            'no shut']

connection.config_mode()

connection.send_config_set(commands)
time.sleep(2)

show_output = connection.send_command('show ip int loopback1 | i Loopback1')
if show_output.count('up') == 2:
    print('It looks like loopback1 is "up/up"! Way to go!')
else:
    print('Something went wrong... let\'s get outa here before we break something!')
    sys.exit()

print('Moving on to GigabitEthernet2...')
commands = ['interface GigabitEthernet2',
            'description This goes to the ASAv',
            'ip address 10.1.253.5 255.255.255.0',
            'no shut']

connection.send_config_set(commands)
time.sleep(2)

show_output = connection.send_command('show ip int GigabitEthernet2 | i GigabitEthernet2')
if show_output.count('up') == 2:
    print('It looks like GigabitEthernet2 is "up/up"! Keep going!')
else:
    print('Something went wrong... let\'s get outa here before we break something!')
    sys.exit()

print('Moving on to static routing...')

commands = ['ip route 10.1.254.5 255.255.255.255 10.1.253.6']

connection.send_config_set(commands)
time.sleep(2)

show_output = connection.send_command('show ip route 10.1.254.5')
if 'Network not in table' in show_output:
    print('Something went wrong... let\'s get outa here before we break something!')
    sys.exit()
else:
    print('It looks like the route made it into the table!')

connection.send_command('wr')


print('Moving on to ASA interfaces!')

asav = {'device_type': 'cisco_asa',
        'ip': '10.1.2.102',
        'username': 'ignw',
        'password': 'supersecure',
        'secret' : 'evenmoresecure'}
connection = ConnectHandler(**asav)

print('Starting on GigabitEthernet0/0...')

commands = ['interface GigabitEthernet0/0',
            'description Connected to CSR',
            'nameif outside',
            'security-level 10',
            'ip address 10.1.253.6 255.255.255.0',
            'no shut']

connection.send_config_set(commands)

print('Starting on GigabitEthernet0/1...')

commands = ['interface GigabitEthernet0/1',
            'description Connected to DMZ Node',
            'nameif outside',
            'security-level 50',
            'ip address 10.1.254.6 255.255.255.0',
            'no shut']

connection.send_config_set(commands)
time.sleep(2)

show_output = connection.send_command('show int ip brief | i GigabitEthernet0/0')
if show_output.count('up') == 2:
    print('It looks like GigabitEthernet0/0 is "up/up"!')
else:
    print('Something went wrong... let\'s get outa here before we break something!')
    sys.exit()
show_output = connection.send_command('show int ip brief | i GigabitEthernet0/1')
if show_output.count('up') == 2:
    print('It looks like GigabitEthernet0/1 is "up/up"!')
else:
    print('Something went wrong... let\'s get outa here before we break something!')
    sys.exit()

print('Moving on to static routing...')

commands = ['route outside 10.1.255.1 255.255.255.255 10.1.253.5']

connection.send_config_set(commands)
time.sleep(2)

show_output = connection.send_command('show route 10.1.255.1')
if 'Network not in table' in show_output:
    print('Something went wrong... let\'s get outa here before we break something!')
    sys.exit()
else:
    print('It looks like the route made it into the table!')

print('Moving on to access-list configuration...')

commands = ['access-list outside_in extended permit icmp any any',
            'access-group outside_in in interface outside']

connection.send_config_set(commands)
connection.send_command('wr')

connection = ConnectHandler(**cisco_cloud_router)
show_output = connection.send_command('ping 10.1.254.5 source 10.1.255.1')
print(show_output)
