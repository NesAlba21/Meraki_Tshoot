# Meraki_Tshoot
## Meraki Basic Tshoot for MX, MS, and MR
*This will help you to pull basic troubleshoot information about your Orgs and your Networks
*This script creates CSV file for each output

## How it works
1. Run the "Meraki_BasicTshoot.py" file
2. Type your Meraki-API-Key
3. Follow the instructions 
4. It'll do the rest

## notes
* API Key - it'll ask you to enter your API key every time you run the file
* This is beta, lots of stuff broken but I´ll fix it. May the force be with you andhave fun!

## Requirements
* Own your Meraki-API-Key

# what works today? 

###### General (working)
* show/create csv file with your Organizations
* show/create csv file with your Networks in your selected organization
* show/create csv file with the devices in your selected network

###### Wireless (MR) (working)
* show/create csv file with MR device info based on selected Serial Number
* show/create csv file with Custom RF profiles in your selected network
* show/create csv file with Top SSIDs by Usage (MB) in your selected organization

###### Switching (MS) (working)
* show/create csv file with MS device info based on selected serial number
* show/create csv file with MS device detailed ports info based on selected serial number

###### Appliance (MX) (working)
* show/create csv file with Site-To-Site VPN info in your selected organization
* show/create csv file with Uplink status info in youir network
* show/create csv file with Static Routes info in your network

