#connect to S3221
from netmiko import ConnectHandler
import configparser
un = "ION"
pw = "private"
se = "private"
config = configparser.ConfigParser()
config.read('S3221.ini')
print (config.sections())
print (config['DEFAULT'])
print (config.defaults())
print (config.options('S3221'))
print (config.items('S3221'))
for key in config['S3221']: 
    print (key,':',config.get('S3221',key))
 



#Open the S3221 Inventory file -- IP Addresses only
#try:
    with open('./S3221.inv') as inv_file:
        for x in inv_file:
            print("------ DEVICE: ", inv_file.readline())
            #Connect via SSH to the device
            net_connect = ConnectHandler(device_type='generic', conn_timeout=10, ip='192.168.128.4', username=un, password=pw)
            print(net_connect)
            
            #Check for the prompt
            output = net_connect.find_prompt()
            print(output)

            #get S3221 System Information
            sys_inf = net_connect.send_command('show system information')
            print(sys_inf)

            #Disconnect SSH
            net_connect.disconnect()
            #move to the next device in the list
            print("-------------------------------")
#except:
#    print("S3221.inv does not exist")




