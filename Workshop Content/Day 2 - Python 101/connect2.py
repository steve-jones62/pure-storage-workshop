from netmiko import ConnectHandler
import keyring as mykeyring
# set un equal to your username
# set pw equal to your password
print("Password: ", mykeyring.get_password("2960l", "admin"))
admin_pass = mykeyring.get_password("2960l", "admin")
print(admin_pass)
admin_pass_en = mykeyring.get_password("2960l", "admin-en")
print(admin_pass_en)

un = "admin"
#pw = "cisco123!"

pw = admin_pass
en = admin_pass_en
ios_type = "cisco_xe"
ip_addr = "192.168.128.151"


net_connect = ConnectHandler(device_type=ios_type, ip=ip_addr, username=un, password=pw)
output = net_connect.find_prompt()

# 'LAB'>’ – Returns the current prompt as Unicode string
print(output)
net_connect.disconnect()
exit()
