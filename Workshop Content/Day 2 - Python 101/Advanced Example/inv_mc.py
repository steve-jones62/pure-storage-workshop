import csv
from netmiko import ConnectHandler
#
#--------------------------------------
# the Userid and password for the IONs
#--------------------------------------
un ="ION"
pw = "private"

#------------------------------------------------------------------------------------------------------------------------------
# the CSV file with the ION information.  Firt line of the file are the field names
# CRE	City	    Site	        Site Type	ION	            Interface	Used For	Operational State	Address_Mask List	Address
# CA074	Brisbane	CA074_Brisbane	Branch	    CA074-SDW-I2K-1	controller	Controller	up	                192.168.14.159/24	192.168.14.159
# the "CSV" module reads these into a Dictionary, each field addressable by name
#---------------------------------------------------------------------------------------------------------------------------------
csv_input_file = "pitneybowes_ION_interfaces_test.csv"
#
#---------------------------------------------------------------------------------------
#  Our output file, again a CSV.   We just need the CRE, City, IP_addr, and return data
#  Blank return means no Media Converter
#  LLDP information means there is a media converter attached
#---------------------------------------------------------------------------------------
#
#
csv_output_file = "pitneybowes_MC_results.csv"
#------------------------------------------------------------
# Open the output file first, stays open until we are done
#------------------------------------------------------------
with open (csv_output_file, 'w', newline='') as csv_output:
    fieldnames = ['CRE', 'City', 'Address', 'ION_Int_1', 'ION_Int_4']
    csv_output_file_writer = csv.DictWriter(csv_output, fieldnames=fieldnames)
    csv_output_file_writer.writeheader()
#
#------------------------------------------------------------------------------------------------------------------------------
# Main body -- loop through the input file and grab output
#------------------------------------------------------------------------------------------------------------------------------
    try:
     with open(csv_input_file, newline='') as ION_inv:
        ION_inv_reader = csv.DictReader(ION_inv)
        for row in ION_inv_reader:

#+++++++++++++++++++++++debug
            print(row['CRE'], row['City'], row['Address'])

            #-------------- Connect via Shttps://www.italeri.com/en/product/2422SH to the ION
            #
            net_connect = ConnectHandler(device_type='terminal_server', conn_timeout=12, ip=row['Address'], username=un, password=pw)
            #net_connect = ConnectHandler(device_type='cloudgenix', conn_timeout=12, ip=row['Address'], username=un, password=pw)

#+++++++++++++++++++++++debug
            print(net_connect)

            #------------------Check for the prompt -------------------------------------
            # We wait for a prompt so we know the CLI processor is ready for the command
            output = net_connect.find_prompt()

#+++++++++++++++++++++++debug
            print(output)

            #--------------------------------For testing info --------------------------------------------------
            #test the command
            #get S3221 System Informationhttps://www.italeri.com/en/product/2422
            sys_inf = net_connect.send_command('show system information')

#+++++++++++++++++++++++debug
            print(sys_inf)

            #
            #--------------------------------For gathering ION info --------------------------------------------------
            #get the ION interface information System Information
            #int_inf_1 = net_connect.send_command('dump lldp interface=1 | grep local')
            #int_inf_4 = net_connect.send_command('dump lldp interface=4 | grep local')
            int_inf_1 = "int 1 info"
            int_inf_4 = "int 4 info"
            #
            #----------------------------------
            # Load the Cell values into vars
            #----------------------------------
            cre = row['CRE']
            city = row['City']
            ip_address = row['Address']

#+++++++++++++++++++++++debug
            print (cre, city, ip_address)
            print(int_inf_1, int_inf_4)

            #----------------------------------------------------------------------------------------------------------------------------------
            # Write the information to our output file
            #-----------------------------------------------------------------------------------------------------------------------------------
            csv_output_file_writer.writerow({'CRE': cre, 'City': city, 'Address': ip_address, 'ION_Int_1': int_inf_1, 'ION_Int_4': int_inf_4})
            #------------------------------------------------------------------------------
            #
            #----------------------------------------------
            # Disconnect SSH and
            # move to the next device in the list
            net_connect.disconnect()
            print("-------------------------------")


    except:
        if csv_output_file_writer.Error:
            print("output error")
        print(csv_input_file, " does not exist")

exit()
