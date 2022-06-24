

import json
from msilib.schema import Error
import requests
import csv
from datetime import datetime


def print_banner():
    print("  __  __              _   _ ")
    print(" |  \/  |___ _ _ __ _| |_(_)")
    print(" | |\/| / =_) '_/ =` | / / |")
    print(" |_|  |_\___|_| \__,_|_\_\_|")
    print("      **Basic T-shoot**     ")
    print("         by @NesAlba        ")
    print()
                            
print_banner()    

def main():
    #Ask for your Meraki-API-Key
    apiKey = input("Enter your Meraki API Key: ")
    
    payload = {}

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": str(apiKey) 
        
    }
    try: 
        #Returns all the Orgs from your account
        apiOrgs = "organizations"
        urlOrgs = "https://api.meraki.com/api/v1/"+str(apiOrgs)
        response = requests.request('GET', urlOrgs, headers=headers, data = payload)
        respuesta = json.loads(response.text.encode('utf8'))
        if apiKey == "quit":
            print("** Goodbye **")
            print("\n")
            exit()
        else:
            listOrgs=[]
            for device in respuesta:
                AllOrgs = ("Name: {:30}\t Id: {}\t".format(device["name"], device["id"]))
                print(AllOrgs)
                #Create csv file
                wOrgsName = (device["name"])
                wOrgsId = (device["id"])
                listOrgsVar = [wOrgsName,wOrgsId]
                listOrgs.append(listOrgsVar)
            Headers = ["Org Name", "Org ID"]
            MyOrgsCsv = datetime.now().strftime("MyOrgs__%m-%d-%Y-%Hh%Mm%Ss.csv")
            with open(MyOrgsCsv, "a", newline="") as orgsFile:
                writeFile = csv.writer(orgsFile)
                writeFile.writerow(Headers)
                writeFile.writerows(listOrgs)
                orgsFile.close()
                #End csv File
    except Exception as e:
        print(e)
        print("\n")
        main()

    try:
        #Return all the Networks form the selected Org
        print("\n")
        
        UserOrgChoice = input("Copy and Paste the Org Id: ")
        apiNtwksInOrg = "organizations/"+str(UserOrgChoice)+"/networks"
        urlNtwks = "https://api.meraki.com/api/v1/"+str(apiNtwksInOrg)

        responseNtwks = requests.request('GET', urlNtwks, headers=headers, data = payload)
        respuestaNtwks = json.loads(responseNtwks.text.encode('utf8'))
        print(UserOrgChoice)
        
        listNtwks = []
        for Networks in respuestaNtwks:
            AllNwks = ("Name: {:30}\t Id: {}\t".format(Networks["name"], Networks["id"]))
            print(AllNwks)
            
            #Create csv file
            wNtwksName = (Networks["name"])
            wNtwksId = (Networks["id"])
            listNtwksVar = [wNtwksName,wNtwksId]
            listNtwks.append(listNtwksVar)
        Headers = ["Network Name", "Network ID"]
        NtwksInOrgCsv = datetime.now().strftime("Netwoks_in_Org_"+str(UserOrgChoice)+"__%m-%d-%Y-%Hh%Mm%Ss.csv")
        with open(NtwksInOrgCsv, "a", newline="") as ntwksFile:
            writeFile = csv.writer(ntwksFile)
            writeFile.writerow(Headers)
            writeFile.writerows(listNtwks)
            ntwksFile.close()
            #End csv File
            
    except Exception as e:
        print(e)
        print("\n")
        main()
    try:
        #Return all Devices from the selected Network
        print("\n")
        UserChoiceNtwk = input("Copy and Paste the Network Id: ")
        apiDevicesinNetwork ="networks/"+str(UserChoiceNtwk)+"/devices"
        urlDevicesinNwk = "https://api.meraki.com/api/v1/"+str(apiDevicesinNetwork)

        responseDevices = requests.request('GET', urlDevicesinNwk, headers=headers, data = payload)
        respuestaDevices = json.loads(responseDevices.text.encode('utf8'))

        print("**** List of devices on your Network ****")
        listDevices = []
        for device in respuestaDevices:
            deviceToPrint = {
                "lanIp": device["lanIp"] if "lanIp" in device else None,
                "wan1Ip": device["wan1Ip"] if "wan1Ip" in device else None,
                "name": device["name"] if "name" in device else None,
                "serial": device["serial"] if "serial" in device else None,
                "model": device["model"] if "model" in device else None,
                "status": device["status"] if "status" in device else None,
                "tags": device["tags"] if "tags" in device else None,                
            }
            print("Name: {:25} Serial: {:16} Model: {:11} IP: {}\tWanIP: {}\tTag:{}".format(deviceToPrint["name"], deviceToPrint["serial"], deviceToPrint["model"], deviceToPrint["lanIp"], deviceToPrint["wan1Ip"], deviceToPrint["tags"]))

            #Create csv file
            wDeviceName = (deviceToPrint["name"])
            wDeviceSerial = (deviceToPrint["serial"])
            wDeviceModel = (deviceToPrint["model"])
            wDevieLanIp = (deviceToPrint["lanIp"])
            wDeviceWanIp = (deviceToPrint["wan1Ip"])
            wDeviceTag = (deviceToPrint["tags"])
            listDevicesVar = [wDeviceName,wDeviceSerial, wDeviceModel, wDevieLanIp, wDeviceWanIp, wDeviceTag]
            listDevices.append(listDevicesVar)
        Headers = ["Name", " Serial", "Model", "LAN IP", "WAN IP", "Tags"]
        devicesInNtwkCsv = datetime.now().strftime("Devices_in_Network_"+str(UserChoiceNtwk)+"__%m-%d-%Y-%Hh%Mm%Ss.csv")
        with open(devicesInNtwkCsv, "a", newline="") as devicesFile:
            writeFile = csv.writer(devicesFile)
            writeFile.writerow(Headers)
            writeFile.writerows(listDevices)
            devicesFile.close()
            #End csv File

    except Exception as e:
        print(e)
        print("\n")
        main()
    print("\n")
    #Questions to user
    moreInfo = input("Do you want more device info? (Y/N): ")
    moreInfo = moreInfo.upper()
    if moreInfo == "Y":
        deviceSelect = input("1.- MR info\n2.- MS info\n3.- MX info\nType your choice: ")
        deviceSelect = int(deviceSelect)
        if deviceSelect == 1: #MR Info
            print("\n")
            selectWirelesInfo = input("1.- MR Device info\n2.- Network Wireless RF Profiles info\n3.- Organization Top SSIDs by Usage\nType your choice: ")
            selectWirelesInfo = int(selectWirelesInfo)
            if selectWirelesInfo == 1: #MR Device Info
                try:
                #Return info from selected MR device
                    wirelessApStatus = input("Wireless MR info - Copy and Paste MR Serial: ")
                    apiApStatus ="devices/"+str(wirelessApStatus)+"/wireless/status"
                    urlApStatus = "https://api.meraki.com/api/v1/"+str(apiApStatus)

                    responseAp = requests.request('GET', urlApStatus, headers=headers, data = payload)
                    respuestaAp = json.loads(responseAp.text.encode('utf8'))
                    
                    listMRinfo = []
                    for Ap in respuestaAp["basicServiceSets"]:
                        if Ap["enabled"]== True:
                            print ("** MR Device Info **")
                            print("SSID: {:20}\t Band: {}\t Channel: {}\t ChWidth: {}\t Power: {} ".format(Ap["ssidName"], Ap["band"], Ap["channel"], Ap["channelWidth"], Ap["power"]))
                            
                            #Create csv file
                            wMRssid = (Ap["ssidName"])
                            wMRband = (Ap["band"])
                            wMRchannel = (Ap["channel"])
                            wMRchWidht = (Ap["channelWidth"])
                            wMRpower = (Ap["power"])
                            listMRinfoVar = [wMRssid, wMRband, wMRchannel, wMRchWidht, wMRpower]
                            listMRinfo.append(listMRinfoVar)
                    Headers = ["SSID", "Band", "Channel", "Channel Widht", "Power"]
                    MrInfoCsv = datetime.now().strftime("Wireless_MR_"+str(wirelessApStatus)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
                    with open(MrInfoCsv, "a", newline="") as MRinfoFile:
                        writeFile = csv.writer(MRinfoFile)
                        writeFile.writerow(Headers)
                        writeFile.writerows(listMRinfo)
                        MRinfoFile.close()
                            #End csv file

                except Exception as e:
                    print(e)
                    print("\n")
                    main()
            elif selectWirelesInfo == 2: #Wireless RF Profile
                #RF Profiles from Network
                apiRfProfiles ="networks/"+str(UserChoiceNtwk)+"/wireless/rfProfiles"
                urlRfProfiles = "https://api.meraki.com/api/v1/"+str(apiRfProfiles)
                
                responseRfProfiles = requests.request('GET', urlRfProfiles, headers=headers, data = payload)
                respuestaRfProfiles = json.loads(responseRfProfiles.text.encode('utf8'))
                if respuestaRfProfiles == []:
                    print("\n")
                    print("** No Custom RF Profiles in this Network **")
                else:
                    listRFinfo = []
                    for rfSettings in respuestaRfProfiles:
                        print("** Network Custom RF Profiles **")
                        print("Name: {:18} 2.4-MaxPwr:{:2}\t 2.4-MinPwr:{:2}\t 2.4-MinBitrate:{}\t 5-MaxPwr:{:3}\t 5-MinPwr:{:3}\t 5-MinBitrate:{}".format(rfSettings["name"], rfSettings["twoFourGhzSettings"]["maxPower"], rfSettings["twoFourGhzSettings"]["minPower"],rfSettings["twoFourGhzSettings"]["minBitrate"], rfSettings["fiveGhzSettings"]["maxPower"], rfSettings["fiveGhzSettings"]["minPower"], rfSettings["fiveGhzSettings"]["minBitrate"]))

                        #Create csv file
                        wRfName = (rfSettings["name"])
                        wRf24max = (rfSettings["twoFourGhzSettings"]["maxPower"])
                        wRf24min = (rfSettings["twoFourGhzSettings"]["minPower"])
                        wRf24minBitrate = (rfSettings["twoFourGhzSettings"]["minBitrate"])
                        wRf5max = (rfSettings["fiveGhzSettings"]["maxPower"])
                        wRf5min = (rfSettings["fiveGhzSettings"]["minPower"])
                        wRf5minBitrate = (rfSettings["fiveGhzSettings"]["minBitrate"])
                        listRFinfoVar = [wRfName, wRf24max, wRf24min, wRf24minBitrate, wRf5max, wRf5min, wRf5minBitrate]
                        listRFinfo.append(listRFinfoVar)
                    Headers = ["Name", "2.4 MaxPower", "2.4 minPower", "2.4 minBitrate", "5Ghz MaxPower", "5Ghz minPower", "5Ghz minBitrate"]
                    RfCsv = datetime.now().strftime("Wireless_RF_Network"+str(UserChoiceNtwk)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
                    with open(RfCsv, "a", newline="") as RFinfoFile:
                        writeFile = csv.writer(RFinfoFile)
                        writeFile.writerow(Headers)
                        writeFile.writerows(listRFinfo)
                        RFinfoFile.close()
                        #End csv file
            elif selectWirelesInfo == 3: #Wireless Top SSIDs by Usage
                t0= input( "Start Date(YYYY-MM-DD): ")
                t1 = input ("End Date(YYYY-MM-DD): ")
                t0hour = input("Start Time(hh:mm:ss): ")
                t1hour = input("End Time(hh:mm:ss): ")
                try:
                    apiTopSsid ="/organizations/"+str(UserOrgChoice)+"/summary/top/ssids/byUsage?t0="+str(t0)+"T"+str(t0hour)+"Z&t1="+str(t1)+"T"+str(t1hour)+"Z"
                    urlTopSsid = "https://api.meraki.com/api/v1/"+str(apiTopSsid)
                
                    responseTopSsid = requests.request('GET', urlTopSsid, headers=headers, data = payload)
                    respuestaTopSsid = json.loads(responseTopSsid.text.encode('utf8'))

                    print("** Organization Top SSIDs by Usage in Megabytes** ")
                    print("--Total usage and percentage values are rounded, for entire values please check the csv file--")
                    listTopSsid = []
                    for TopSsid in respuestaTopSsid:
                        totUse = round(TopSsid["usage"]["total"])
                        percentage = round(TopSsid["usage"]["percentage"])
                        # percentage = round(percentageInt)
                        # totUse = round(totUseInt)
                        print("Name: {:25} TotalUsg: {:10}  Percentage: {:3}\t Clients: {}".format(TopSsid["name"], totUse, percentage, TopSsid["clients"]["counts"]["total"]))

                        #Create csv file
                        wTopSsidName = (TopSsid["name"])
                        wTopSsidTotal = (TopSsid["usage"]["total"])
                        wTopSsidDown = (TopSsid["usage"]["downstream"])
                        wTopSsidUp = (TopSsid["usage"]["upstream"])
                        wTopSsidPrct =(TopSsid["usage"]["percentage"])
                        wTopSsidClients = (TopSsid["clients"]["counts"]["total"])
                        listTopSsidVar = [wTopSsidName,wTopSsidTotal,wTopSsidDown,wTopSsidUp,wTopSsidClients,wTopSsidPrct]
                        listTopSsid.append(listTopSsidVar)
                    Headers = ["SSID Name", "Total Usage MB", "Total Downstream MB", "Total Upstream MB", "Clients","Total Percentage"]
                    Explain = ["Top SSIDs by Usage in MB"]
                    topSsidCsv = datetime.now().strftime("Top_SSIDs_in_Org_"+str(UserOrgChoice)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
                    with open(topSsidCsv, "a", newline="") as topSsidFile:
                        writeFile = csv.writer(topSsidFile)
                        writeFile.writerow(Explain)
                        writeFile.writerow(Headers)
                        writeFile.writerows(listTopSsid)
                        topSsidFile.close()
                        #End csv file
                except Exception as e:
                    print(e)
                    print("\n")
                    exit()
            else:
                print("** Invalid Selection **")
                print("\n")
                main()   
        elif deviceSelect == 2: #MS Info
            print("\n")
            try:
                #Return info from selected MS device
                swStatus = input("MS info - Copy and Paste MS Serial: ")
                apiSwStatus ="devices/"+str(swStatus)+"/switch/ports/statuses"
                urlSwStatus = "https://api.meraki.com/api/v1/"+str(apiSwStatus)

                responseSw = requests.request('GET', urlSwStatus, headers=headers, data = payload)
                respuestaSw = json.loads(responseSw.text.encode('utf8'))
                
                listMSinfo = []
                for ports in respuestaSw: #Return the status for all the ports of a switch  
                    print("Port: {:16}\t Uplink: {}\t Speed: {:10}\t Duplex: {:6}\t Errors: {}".format(ports["portId"], ports["isUplink"], ports["speed"], ports["duplex"], ports["errors"]))
                    
                    #Create csv file
                    wMsPort = (ports["portId"])
                    wMsUplink =(ports["isUplink"])
                    wMsSpeed =(ports["speed"])
                    wMsDuplex =(ports["duplex"])
                    wMsErrors =(ports["errors"])
                    listMSinfoVar = [wMsPort, wMsUplink, wMsSpeed, wMsDuplex, wMsErrors]
                    listMSinfo.append(listMSinfoVar)

                Headers = ["Port", "Uplink", "Speed", "Duplex", "Errors"]
                MsInfoCsv = datetime.now().strftime("Switch_MS_"+str(swStatus)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
                with open(MsInfoCsv, "a", newline="") as MSinfoFile:
                    writeFile = csv.writer(MSinfoFile)
                    writeFile.writerow(Headers)
                    writeFile.writerows(listMSinfo)
                    MSinfoFile.close()
                    #End csv file

                print("\n")
                
                #More MS info
                moreMsInfo = input("Do you want more info about this MS?(Y/N): ")
                moreMsInfo = moreMsInfo.upper()

                if moreMsInfo == "Y":

                    apiSwStatusP ="devices/"+str(swStatus)+"/switch/ports"
                    urlSwStatusP = "https://api.meraki.com/api/v1/"+str(apiSwStatusP)

                    responseSwP = requests.request('GET', urlSwStatusP, headers=headers, data = payload)
                    respuestaSwP = json.loads(responseSwP.text.encode('utf8'))

                    listMSportInfo = []
                    for p in respuestaSwP: #List the switch ports for a switch
                        print("Port: {:16}\t PoE: {}\t Vlan: {}\t VoiceVlan: {}\t PortType: {:8} RSTP en: {}\t StpGuard: {}".format(p["portId"], p["poeEnabled"], p["vlan"], p["voiceVlan"],p["type"], p["rstpEnabled"], p["stpGuard"]))
                
                        #Create csv file
                        wMsPortInfoPort =(p["portId"])
                        wMSPortInfoPOE =(p["poeEnabled"])
                        wMsPortInfoVlan =(p["vlan"])
                        wMsPortInfoVoiceLan =(p["voiceVlan"])
                        wMsPortInfoType =(p["type"])
                        wMsPortInfoRSTP=(p["rstpEnabled"])
                        wMsPortInfoSTP =(p["stpGuard"])
                        listMSportInfoVar = [wMsPortInfoPort,wMSPortInfoPOE, wMsPortInfoVlan, wMsPortInfoVoiceLan, wMsPortInfoType, wMsPortInfoRSTP, wMsPortInfoSTP]
                        listMSportInfo.append(listMSportInfoVar)

                    Headers = ["Port", "PoE", "Vlan", "Voice Vlan", "Port Type", "RSTP", "STP Guard"]
                    MsMoreInfoCsv = datetime.now().strftime("Switch_MS_"+str(swStatus)+"_Ports_detailed_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
                    with open( MsMoreInfoCsv, "a", newline="") as MSportInfoFile:
                        writeFile = csv.writer(MSportInfoFile)
                        writeFile.writerow(Headers)
                        writeFile.writerows(listMSportInfo)
                        MSportInfoFile.close()
                        #End csv file
                else:
                    main()
            except Exception as e:
                print("** MS Serial Number - Not Found - Please input a valid MS Serial Number **")
                print("\n")
                main()
        elif deviceSelect == 3: #MX Info
            print("\n")
            mxSelect = input("1.- Mx in Organization Sie-To-Site VPN\n2.- MX in Network Uplink Status\n3.- MX in Network Static Routes\nType your choice: ")
            mxSelect = int(mxSelect)
            if mxSelect == 1: #MX Site-To-Site VPN
                try:
                #Mx Site-To-Site VPN
                    apiSiteToSiteVPN ="/organizations/"+str(UserOrgChoice)+"/appliance/vpn/statuses"
                    urlSiteToSiteVPN = "https://api.meraki.com/api/v1/"+str(apiSiteToSiteVPN)

                    responseSiteToSiteVPN = requests.request('GET', urlSiteToSiteVPN, headers=headers, data = payload)
                    respuestaSiteToSiteVPN = json.loads(responseSiteToSiteVPN.text.encode('utf8'))
                    
                    listVpnInfo = []
                    for vpnStatuses in respuestaSiteToSiteVPN:
                        for uplinks in vpnStatuses["uplinks"]:
                            for vpnPeers in vpnStatuses["merakiVpnPeers"]:
                                print("** Org VPN Site-To-Site **")
                                print("Network: {:20}\t Status: {:8} VPN mode: {:7} Interface: {:6} Public IP: {:17} Peers: {}".format(vpnStatuses["networkName"],vpnStatuses["deviceStatus"], vpnStatuses["vpnMode"], uplinks["interface"], uplinks["publicIp"], vpnPeers["networkName"]))

                                #Create csv file
                                wVpnNtwk =(vpnStatuses["networkName"])
                                wVpnStatus =(vpnStatuses["deviceStatus"])
                                wVpnMode =(vpnStatuses["vpnMode"])
                                wVpnInt = (uplinks["interface"])
                                wVpnPublic  =(uplinks["publicIp"])
                                wVpnPeers =(vpnPeers["networkName"])
                                listVpnInfoVar = [wVpnNtwk, wVpnStatus, wVpnMode, wVpnInt, wVpnPublic, wVpnPeers]
                                listVpnInfo.append(listVpnInfoVar)
                    Headers =["Name", "Status", "VPN Mode", "Interface", "Pibic IP", "VPN Peers"]
                    VpnCsv = datetime.now().strftime("Site-To-Site VPN_in Org_"+str(UserOrgChoice)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
                    with open(VpnCsv, "a", newline="") as VpnInfoFile:
                        writeFile = csv.writer(VpnInfoFile)
                        writeFile.writerow(Headers)
                        writeFile.writerows(listVpnInfo)
                        VpnInfoFile.close()
                                #End csv file
                except Exception as e:
                    print(e)
                    exit()
            elif mxSelect == 2: #MX Ntwk Uplink Status
                try:
                #MX Vlans
                    apiMxVlans ="/networks/"+str(UserChoiceNtwk)+"/appliance/vlans"
                    urlMxVlans = "https://api.meraki.com/api/v1/"+str(apiMxVlans)

                    responseMxVlans = requests.request('GET', urlMxVlans, headers=headers, data = payload)
                    respuestaMxVlans = json.loads(responseMxVlans.text.encode('utf8'))

                    listMxVlans =[]
                    for mxVlans in respuestaMxVlans:
                        print("** Network Uplink Info **")
                        print("Vlan id: {}\tname: {}\tapplIp: {}\tSubnet: {}\tDns: {}\tDhcpHand: {}".format(mxVlans["id"], mxVlans["name"], mxVlans["applianceIp"], mxVlans["subnet"],mxVlans["dnsNameservers"], mxVlans["dhcpHandling"] ))

                        #Create csv file
                        wMxVlanNtwk = (mxVlans["networkId"])
                        wMxVlanId = (mxVlans["id"])
                        wMxVlanName =(mxVlans["name"])
                        wMxAppIp = (mxVlans["applianceIp"])
                        wMxSubnet =(mxVlans["subnet"])
                        wMxDns = (mxVlans["dnsNameservers"])
                        wMxDhcpHand =(mxVlans["dhcpHandling"])
                        listMxVlansVar =[wMxVlanNtwk,wMxVlanId,wMxVlanName,wMxAppIp,wMxSubnet,wMxDns,wMxDhcpHand]
                        listMxVlans.append(listMxVlansVar)
                    Headers =["Network ID","Vlan Id","Name", "Applicance IP", "Subnet", "DNS", "DHCP Handling"]
                    MxVlanCsv = datetime.now().strftime("MX_Appliance_Vlans_form_Network_"+str(UserChoiceNtwk)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
                    with open(MxVlanCsv, "a", newline="") as MxVlanFile:
                        writeFile = csv.writer(MxVlanFile)
                        writeFile.writerow(Headers)
                        writeFile.writerows(listMxVlans)
                        MxVlanFile.close()

                        #End csv file
                except Exception as e:
                    print(e)
                    exit()
            elif mxSelect == 3: #MX Static Routes
                #MX Static Routes
                try:
                    apiMxStaticRoutes ="/networks/"+str(UserChoiceNtwk)+"/appliance/staticRoutes"
                    urlMxStaticRoutes = "https://api.meraki.com/api/v1/"+str(apiMxStaticRoutes)

                    responseMxStaticRoutes = requests.request('GET', urlMxStaticRoutes, headers=headers, data = payload)
                    respuestaMxStaticRoutes = json.loads(responseMxStaticRoutes.text.encode('utf8'))
                    
                    if respuestaMxStaticRoutes == []:
                        print("\n")
                        print("** No Static Routes in this Network **")
                    else:
                        listMXStaticRoutes = []
                        for MxStatic in respuestaMxStaticRoutes:
                            print("** Network Static Routes **")
                            print("Name: {}\t Subet: {}\t Gateway: {}".format(MxStatic["name"], MxStatic["subnet"], MxStatic["gatewayIp"]))
                            
                            #Create csv file
                            wMxStaticNtwk = (MxStatic["networkId"])
                            wMxStaticName = (MxStatic["name"])
                            wMxStaticSubnet =(MxStatic["subnet"])
                            wMxStaticGw = (MxStatic["gatewayIp"])
                            listMxStaticVar=[wMxStaticNtwk,wMxStaticName,wMxStaticSubnet,wMxStaticGw]
                            listMXStaticRoutes.append(listMxStaticVar)
                        Headers = ["Network ID", "Name", "Subnet", "Gateway"]
                        MxStaticCsv = datetime.now().strftime("MX_Appliance_Static Route_form_Network_"+str(UserChoiceNtwk)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
                        with open(MxStaticCsv, "a", newline="") as MxStaticFile:
                            writeFile = csv.writer(MxStaticFile)
                            writeFile.writerow(Headers)
                            writeFile.writerows(listMXStaticRoutes)
                            MxStaticFile.close()
                            #End csv file
                except Exception as e:
                    print(e)
                    exit()
            else:
                main()
        else:
            main()
    else:
        #Exit
        print(" Hope this helped you ")
        print("** Goodbye **")
        print("\n")
        exit()
    print("\n")
    #loop
    anotherSearch = input("Do you want to start over? (Y/N): ")
    anotherSearch = anotherSearch.upper()
    if anotherSearch == "Y":
         main()
    else:
    #Exit
        anotherSearch == "N"
        print("Hope this helped you")
        print("** Goodbye **")
        print("\n")
        exit()
main()