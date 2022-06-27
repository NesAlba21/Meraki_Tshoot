### Meraki basic Tshoot- v2 by NesAlba

import json
from operator import index
from typing import Type
import requests
import csv
from datetime import datetime
import meraki
import pandas as pd


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
            print("Your Orgs: ")
            listOrgs=[]
            for device in respuesta:
                OrgsName = (device["name"])
                OrgsId = (device["id"])
                OrgsLicensing = (device["licensing"]["model"])
                #Create file output
                listOrgsVar = [OrgsName,OrgsId,OrgsLicensing]
                listOrgs.append(listOrgsVar)
            Headers = ["Org Name", "Org ID", "Licensing"]
            orgsPd = pd.DataFrame(listOrgs, columns=Headers)
            print(orgsPd)
            save = input( "Q.Save to file? (Y/N): ")#Save file
            save = save.upper()
            if save == "Y":
                saveType= input("1.-Save as Excel file\n2.-Save as CSV file\nType your choice: ")
                saveType = int(saveType)
                if saveType == 1:
                    MyOrgsCsv = datetime.now().strftime("MyOrgs__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
                    orgsPd.to_excel(MyOrgsCsv, index=False)
                    print("** Excel file successfully saved **")
                elif saveType == 2:            
                    MyOrgsCsv = datetime.now().strftime("MyOrgs__%m-%d-%Y-%Hh%Mm%Ss.csv")
                    orgsPd.to_csv(MyOrgsCsv, index=False)
                    print("** CSV file successfully saved **")
                #End csv File
    except meraki.APIKeyError as e:
        print (e)
        print("\n")
        main()
    except Exception as e:
        print(e)
        print("\n")
        main()
    try:
        #Return all the Networks form the selected Org
        print("\n")
        print("i.Pull Organization Networks")
        
        UserOrgChoice = input("Copy and Paste the Org Id: ")
        apiNtwksInOrg = "organizations/"+str(UserOrgChoice)+"/networks"
        urlNtwks = "https://api.meraki.com/api/v1/"+str(apiNtwksInOrg)

        responseNtwks = requests.request('GET', urlNtwks, headers=headers, data = payload)
        respuestaNtwks = json.loads(responseNtwks.text.encode('utf8'))
        #print(respuestaNtwks)
        
        listNtwks = []
        for Networks in respuestaNtwks:
            NtwksName = (Networks["name"])
            NtwksId = (Networks["id"])
            NtwksProdType = (Networks["productTypes"])
            NtwksTimeZone =(Networks["timeZone"])
            #Create csv file
            listNtwksVar = [NtwksName,NtwksId,NtwksTimeZone]
            listNtwks.append(listNtwksVar)
        Headers = ["Network Name", "Network ID", "Time Zone"]
        NtwksPd = pd.DataFrame(listNtwks, columns=Headers)
        NtwksPd = NtwksPd.reset_index(drop=True)
        NtwksPd.index +=1
        print(NtwksPd)
        save = input( "Q.Save to file? (Y/N): ")#Save file
        save = save.upper()
        if save == "Y":
            saveType= input("1.-Save as Excel file\n2.-Save as CSV file\nType your choice: ")
            saveType = int(saveType)
            if saveType == 1:
                NtwksCsv = datetime.now().strftime("Netwoks_in_Org_"+str(UserOrgChoice)+"__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
                NtwksPd.to_excel(NtwksCsv, index=False)
                print("** Excel file successfully saved **")
            elif saveType == 2:            
                NtwksCsv = datetime.now().strftime("Netwoks_in_Org_"+str(UserOrgChoice)+"__%m-%d-%Y-%Hh%Mm%Ss.csv")
                NtwksPd.to_csv(NtwksCsv, index=False)
                print("** CSV file successfully saved **")

            
    except meraki.APIError as e:
        print (e)
        print("\n")
        main()
    except Exception as e:
        print(e)
        print("\n")
        main()
    try:
        #Return all Devices from the selected Network
        print("\n")
        print("i.Pull network devices")
        UserChoiceNtwk = input("Copy and Paste the Network Id: ")
        apiDevicesinNetwork ="networks/"+str(UserChoiceNtwk)+"/devices"
        urlDevicesinNwk = "https://api.meraki.com/api/v1/"+str(apiDevicesinNetwork)

        responseDevices = requests.request('GET', urlDevicesinNwk, headers=headers, data = payload)
        respuestaDevices = json.loads(responseDevices.text.encode('utf8'))

        print("i.Existing devices on  your network.")
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
        devicesPd = pd.DataFrame(listDevices, columns=Headers)
        devicesSort = input("Q.Sort devices? (Y/N): ") #Sort Question
        devicesSort =devicesSort.upper()
        if devicesSort =="Y":
            devSort = input ("1.- Sort by IP\n2.- Sort by Name\nType your choice: ")
            devSort = int(devSort)
            if devSort == 1: #Sort by Ip Address
                devSortIp = devicesPd.sort_values("LAN IP")
                devSortIp =devSortIp.reset_index(drop=True)
                devSortIp.index +=1 
                print(devSortIp)
                save = input( "Q.Save to file? (Y/N): ")
                save = save.upper()
                if save == "Y":
                    saveType= input("1.-Save as Excel file\n2.-Save as CSV file\nType your choice: ")
                    saveType = int(saveType)
                    if saveType == 1:
                        devicesInNtwkCsv = datetime.now().strftime("Devices_in_Network_"+str(UserChoiceNtwk)+"_by_IP__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
                        devSortIp.to_excel(devicesInNtwkCsv, index=False)
                        print("** Excel file successfully saved **")
                    elif saveType == 2:           
                        devicesInNtwkCsv = datetime.now().strftime("Devices_in_Network_"+str(UserChoiceNtwk)+"_by_IP__%m-%d-%Y-%Hh%Mm%Ss.csv")
                        devSortIp.to_csv(devicesInNtwkCsv, index=False)
                        print("** CSV file successfully saved **")
            elif devSort ==2: #Sort by Name 
                devSortName = devicesPd.sort_values("Name")
                devSortName = devSortName.reset_index(drop=True)
                devSortName.index +=1
                print(devSortName)
                save = input( "Q.Save to file? (Y/N): ") #Save to file question
                save = save.upper()
                if save == "Y":
                    saveType= input("1.-Save as Excel file\n2.-Save as CSV file\nType your choice: ")
                    saveType = int(saveType)
                    if saveType == 1:
                        devicesInNtwkCsv = datetime.now().strftime("Devices_in_Network_"+str(UserChoiceNtwk)+"_by_Name__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
                        devSortName.to_excel(devicesInNtwkCsv, index=False)
                        print("** Excel file successfully saved **")
                    elif saveType == 2:            
                        devicesInNtwkCsv = datetime.now().strftime("Devices_in_Network_"+str(UserChoiceNtwk)+"_by_Name__%m-%d-%Y-%Hh%Mm%Ss.csv")
                        devSortName.to_csv(devicesInNtwkCsv, index=False)
                        print("** CSV file successfully saved **")
        elif devicesSort == "N": #No to Sort
            devicesPd.index +=1
            print(devicesPd)
            save = input( "Q.Save to file? (Y/N): ")
            save = save.upper()
            if save == "Y":
                saveType= input("1.-Save as Excel file\n2.-Save as CSV file\nType your choice: ")
                saveType = int(saveType)
                if saveType == 1:
                    devicesInNtwkCsv = datetime.now().strftime("Devices_in_Network_"+str(UserChoiceNtwk)+"__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
                    devicesPd.to_excel(devicesInNtwkCsv, index=False)
                    print("** Excel file successfully saved **")
                elif saveType == 2:            
                    devicesInNtwkCsv = datetime.now().strftime("Devices_in_Network_"+str(UserChoiceNtwk)+"__%m-%d-%Y-%Hh%Mm%Ss.csv")
                    devicesPd.to_csv(devicesInNtwkCsv, index=False)
                    print("** CSV file successfully saved **")
    except meraki.APIError as e:
        print (e)
        print("\n")
        main()
    except Exception as e:
        print(e)
        print("\n")
        main()
    print("\n")
    #Questions to user
    moreInfo = input("Do you want more info? (Y/N): ")
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
                    print ("** MR Device Info **")
                    listMRinfo = []
                    for Ap in respuestaAp["basicServiceSets"]:
                        if Ap["enabled"]== True:
                            MRssid = (Ap["ssidName"])
                            MRband = (Ap["band"])
                            MRchannel = (Ap["channel"])
                            MRchWidht = (Ap["channelWidth"])
                            MRpower = (Ap["power"])
                            #Create csv file
                            listMRinfoVar = [MRssid, MRband, MRchannel, MRchWidht, MRpower]
                            listMRinfo.append(listMRinfoVar)
                    Headers = ["SSID", "Band", "Channel", "ChanWidth", "Power"]
                    mrInfoPd = pd.DataFrame(listMRinfo, columns=Headers)
                    mrInfoPd.index +=1
                    print(mrInfoPd)
                    save = input( "Q.Save to file? (Y/N): ")
                    save = save.upper()
                    if save == "Y":
                        saveType= input("1.-Save as Excel file\n2.-Save as CSV file\nType your choice: ")
                        saveType = int(saveType)
                        if saveType == 1:
                            MrInfoCsv = datetime.now().strftime("Wireless_MR_"+str(wirelessApStatus)+"_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
                            mrInfoPd.to_excel(MrInfoCsv, index=False)
                            print("** Excel file successfully saved **")
                        elif saveType == 2:            
                            MrInfoCsv = datetime.now().strftime("Wireless_MR_"+str(wirelessApStatus)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
                            mrInfoPd.to_csv(MrInfoCsv, index=False)
                            print("** CSV file successfully saved **")
                            #End  files
                except meraki.APIError as e:
                    print (e)
                    print("\n")
                    main()
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
                        RfName = (rfSettings["name"])
                        Rf24max = (rfSettings["twoFourGhzSettings"]["maxPower"])
                        Rf24min = (rfSettings["twoFourGhzSettings"]["minPower"])
                        Rf24minBitrate = (rfSettings["twoFourGhzSettings"]["minBitrate"])
                        Rf5max = (rfSettings["fiveGhzSettings"]["maxPower"])
                        Rf5min = (rfSettings["fiveGhzSettings"]["minPower"])
                        Rf5minBitrate = (rfSettings["fiveGhzSettings"]["minBitrate"])
                        print("** Network Custom RF Profiles **")
                        #print("Name: {:18} 2.4-MaxPwr:{:2}\t 2.4-MinPwr:{:2}\t 2.4-MinBitrate:{}\t 5-MaxPwr:{:3}\t 5-MinPwr:{:3}\t 5-MinBitrate:{}".format(rfSettings["name"], rfSettings["twoFourGhzSettings"]["maxPower"], rfSettings["twoFourGhzSettings"]["minPower"],rfSettings["twoFourGhzSettings"]["minBitrate"], rfSettings["fiveGhzSettings"]["maxPower"], rfSettings["fiveGhzSettings"]["minPower"], rfSettings["fiveGhzSettings"]["minBitrate"]))

                        #Create  file
                        
                        listRFinfoVar = [RfName, Rf24max, Rf24min, Rf24minBitrate, Rf5max, Rf5min, Rf5minBitrate]
                        listRFinfo.append(listRFinfoVar)
                    
                    Headers = ["Name", "2.4 MaxPower", "2.4 minPower", "2.4 minBitrate", "5Ghz MaxPower", "5Ghz minPower", "5Ghz minBitrate"]
                    rfInfoPd = pd.DataFrame(listRFinfo, columns=Headers)
                    rfInfoPd.index +=1
                    print(rfInfoPd)
                    save = input( "Q.Save to file? (Y/N): ")
                    save = save.upper()
                    if save == "Y":
                        saveType= input("1.-Save as Excel file\n2.-Save as CSV file\nType your choice: ")
                        saveType = int(saveType)
                        if saveType == 1:
                            RfCsv = datetime.now().strftime("Wireless_RF_Network"+str(UserChoiceNtwk)+"_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
                            rfInfoPd.to_excel(RfCsv, index=False)
                            print("** Excel file successfully saved **")
                        elif saveType == 2:            
                            RfCsv = datetime.now().strftime("Wireless_RF_Network"+str(UserChoiceNtwk)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
                            rfInfoPd.to_csv(RfCsv, index=False)
                            print("** CSV file successfully saved **")
                        #End  write file
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
                    print("--Total usage and percentage values are rounded --")
                    listTopSsid = []
                    for TopSsid in respuestaTopSsid:
                        totUse = round(TopSsid["usage"]["total"])
                        percentage = round(TopSsid["usage"]["percentage"])
                        #Create csv file
                        TopSsidName = (TopSsid["name"])
                        TopSsidTotal = round(TopSsid["usage"]["total"])
                        TopSsidPrct = round(TopSsid["usage"]["percentage"])
                        TopSsidClients = (TopSsid["clients"]["counts"]["total"])
                        listTopSsidVar = [TopSsidName,TopSsidTotal,TopSsidClients,TopSsidPrct]
                        listTopSsid.append(listTopSsidVar)
                    Headers = ["SSID Name", "Total Usage MB", "Clients","Total Percentage"]
                    Explain = ["Top SSIDs by Usage in MB"]
                    topSsidPd = pd.DataFrame(listTopSsid, columns=Headers)
                    topSsidPd.index +=1
                    print(topSsidPd)
                    save = input( "Q.Save to file? (Y/N): ")
                    save = save.upper()
                    if save == "Y":
                        saveType= input("1.-Save as Excel file\n2.-Save as CSV file\nType your choice: ")
                        saveType = int(saveType)
                        if saveType == 1:
                            topSsidCsv = datetime.now().strftime("Top_SSIDs_in_Org_"+str(UserOrgChoice)+"_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
                            topSsidPd.to_excel(topSsidCsv, index=False)
                            print("** Excel file successfully saved **")
                        elif saveType == 2:            
                            topSsidCsv = datetime.now().strftime("Top_SSIDs_in_Org_"+str(UserOrgChoice)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
                            topSsidPd.to_csv(topSsidCsv, index=False)
                            print("** CSV file successfully saved **")
                        #End write file
                except meraki.APIError as e:
                    print (e)
                    print("\n")
                    main()
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
                #print(respuestaSw)
                
                listMSinfo = []
                for ports in respuestaSw: #Return the status for all the ports of a switch
                    MsPort = (ports["portId"])
                    MsUplink =(ports["isUplink"])
                    MsSpeed =(ports["speed"])
                    MsDuplex =(ports["duplex"])
                    MsErrors =(ports["errors"])
                    MsWarnings =(ports["warnings"])
                    
                    #Create files
                    
                    listMSinfoVar = [MsPort, MsUplink, MsSpeed, MsDuplex,MsErrors, MsWarnings]
                    listMSinfo.append(listMSinfoVar)
        
                Headers = ["Port", "Uplink", "Speed", "Duplex", "Errors", "Warnings"]
                msInfoPd = pd.DataFrame(listMSinfo, columns=Headers)
                msInfoPd.index +=1
                print(msInfoPd)
                
                save = input( "Q.Save to file? (Y/N): ")
                save = save.upper()
                if save == "Y":
                    saveType= input("1.-Save as Excel file\n2.-Save as CSV file\nType your choice: ")
                    saveType = int(saveType)
                    if saveType == 1:
                        MsInfoCsv = datetime.now().strftime("Switch_MS_"+str(swStatus)+"_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
                        msInfoPd.to_excel(MsInfoCsv, index=False)
                        print("** Excel file successfully saved **")
                    elif saveType == 2:            
                        MsInfoCsv = datetime.now().strftime("Switch_MS_"+str(swStatus)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
                        msInfoPd.to_csv(MsInfoCsv, index=False)
                        print("** CSV file successfully saved **")
                
                    #End write files

                print("\n")
                
                #More MS info
                moreMsInfo = input("Do you want more info about this MS?(Y/N): ")
                moreMsInfo = moreMsInfo.upper()

                if moreMsInfo == "Y":

                    apiSwStatusP ="devices/"+str(swStatus)+"/switch/ports"
                    urlSwStatusP = "https://api.meraki.com/api/v1/"+str(apiSwStatusP)

                    responseSwP = requests.request('GET', urlSwStatusP, headers=headers, data = payload)
                    respuestaSwP = json.loads(responseSwP.text.encode('utf8'))
                    #print(respuestaSwP)

                    listMSportInfo = []
                    for p in respuestaSwP: #List the switch ports for a switch
                
                        #Create csv file
                        MsPortInfoPort =(p["portId"])
                        MSPortInfoPOE =(p["poeEnabled"])
                        MsPortInfoVlan =(p["vlan"])
                        MsPortInfoVoiceLan =(p["voiceVlan"])
                        MsPortInfoType =(p["type"])
                        MsPortInfoRSTP=(p["rstpEnabled"])
                        MsPortInfoSTP =(p["stpGuard"])
                        MsPortInfoName = (p["name"])
                        MSPortInfoAllowedVlans = (p["allowedVlans"])
                        listMSportInfoVar = [MsPortInfoPort,MSPortInfoPOE, MsPortInfoVlan, MsPortInfoVoiceLan,MSPortInfoAllowedVlans, MsPortInfoType, MsPortInfoRSTP, MsPortInfoSTP, MsPortInfoName]
                        listMSportInfo.append(listMSportInfoVar)

                    Headers = ["Port", "PoE", "Vlan", "voiceVlan","allowedVlans", "Type", "RSTP", "STP Guard", "Description"]
                    msPortInfoPD = pd.DataFrame(listMSportInfo, columns=Headers)
                    print(msPortInfoPD)
                    #Create files
                    save = input( "Q.Save to file? (Y/N): ")
                    save = save.upper()
                    if save == "Y":
                        saveType= input("1.-Save as Excel file\n2.-Save as CSV file\nType your choice: ")
                        saveType = int(saveType)
                        if saveType == 1:
                            MsMoreInfoCsv = datetime.now().strftime("Switch_MS_"+str(swStatus)+"_Ports_detailed_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
                            msPortInfoPD.to_excel(MsMoreInfoCsv, index=False)
                            print("** Excel file successfully saved **")
                        elif saveType == 2:            
                            MsMoreInfoCsv = datetime.now().strftime("Switch_MS_"+str(swStatus)+"_Ports_detailed_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
                            msPortInfoPD.to_csv(MsMoreInfoCsv, index=False)
                            print("** CSV file successfully saved **")
                        #End write file
                else:
                    main()
            except meraki.APIError as e:
                print (e)
                print("\n")
                main()
            except Exception as e:
                print(e)
                print("\n")
                main()
        elif deviceSelect == 3: #MX Info
            print("\n")
            mxSelect = input("1.- Mx in Organization Sie-To-Site VPN\n2.- MX in Network Uplink Status\n3.- MX in Network Static Routes\nType your choice: ")
            mxSelect = int(mxSelect)
            if mxSelect ==1: #MX Site-To-Site VPN
                try:
                #Mx Site-To-Site VPN
                    apiSiteToSiteVPN ="/organizations/"+str(UserOrgChoice)+"/appliance/vpn/statuses"
                    urlSiteToSiteVPN = "https://api.meraki.com/api/v1/"+str(apiSiteToSiteVPN)

                    responseSiteToSiteVPN = requests.request('GET', urlSiteToSiteVPN, headers=headers, data = payload)
                    respuestaSiteToSiteVPN = json.loads(responseSiteToSiteVPN.text.encode('utf8'))
                    print(respuestaSiteToSiteVPN)
                    print("** Org VPN Site-To-Site **")
                    
                    listVpnInfo = []
                    for vpnStatuses in respuestaSiteToSiteVPN:
                        for uplinks in vpnStatuses["uplinks"]:
                            for vpnPeers in vpnStatuses["merakiVpnPeers"]:
                                for exportedSub in vpnStatuses["exportedSubnets"]:
                                    VpnExpSub = (exportedSub["subnet"])
                                    VpnNtwk =(vpnStatuses["networkName"])
                                    VpnStatus =(vpnStatuses["deviceStatus"])
                                    VpnMode =(vpnStatuses["vpnMode"])
                                    VpnInt = (uplinks["interface"])
                                    VpnPublic  =(uplinks["publicIp"])
                                    VpnPeers =(vpnPeers["networkName"])
                                    listVpnInfoVar = [VpnNtwk, VpnStatus, VpnMode, VpnInt, VpnPublic, VpnPeers, VpnExpSub]
                                    listVpnInfo.append(listVpnInfoVar)
                    Headers =["Name", "Status", "vpnMode", "Interface", "publicIP", "vpnPeers", "exportedSubnets"]
                    vpnInfoPd = pd.DataFrame(listVpnInfo, columns=Headers)
                    vpnInfoPd.index +=1
                    print(vpnInfoPd)
                except meraki.APIError as e:
                    print (e)
                    print("\n")
                    main()
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
                    Headers =["Network ID","Vlan","Name", "applicanceIP", "Subnet", "DNS", "dhcpHandling"]
                    mxVlansPd = pd.DataFrame(listMxVlans, columns=Headers)
                    mxVlansPd.index +=1
                    print(mxVlansPd)
                    save = input( "Q.Save to file? (Y/N): ")
                    save = save.upper()
                    if save == "Y":
                        saveType= input("1.-Save as Excel file\n2.-Save as CSV file\nType your choice: ")
                        saveType = int(saveType)
                        if saveType == 1:
                            MxVlanCsv = datetime.now().strftime("MX_Appliance_Vlans_form_Network_"+str(UserChoiceNtwk)+"_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
                            mxVlansPd.to_excel(MxVlanCsv, index=False)
                            print("** Excel file successfully saved **")
                        elif saveType == 2:
                            MxVlanCsv = datetime.now().strftime("MX_Appliance_Vlans_form_Network_"+str(UserChoiceNtwk)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")         
                            mxVlansPd.to_csv(MxVlanCsv, index=False)
                            print("** CSV file successfully saved **")
                    
                    
                        #End csv file
                except meraki.APIError as e:
                    print (e)
                    print("\n")
                    main()
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
                            #Create csv file
                            wMxStaticNtwk = (MxStatic["networkId"])
                            wMxStaticName = (MxStatic["name"])
                            wMxStaticSubnet =(MxStatic["subnet"])
                            wMxStaticGw = (MxStatic["gatewayIp"])
                            listMxStaticVar=[wMxStaticNtwk,wMxStaticName,wMxStaticSubnet,wMxStaticGw]
                            listMXStaticRoutes.append(listMxStaticVar)
                        Headers = ["Network ID", "Name", "Subnet", "Gateway"]
                        mxStaticRoutePd = pd.DataFrame(listMXStaticRoutes, columns=Headers)
                        mxStaticRoutePd.index +=1
                        print(mxStaticRoutePd)
                        
                        save = input( "Q.Save to file? (Y/N): ")
                        save = save.upper()
                        if save == "Y":
                            saveType= input("1.-Save as Excel file\n2.-Save as CSV file\nType your choice: ")
                            saveType = int(saveType)
                            if saveType == 1:
                                MxStaticCsv = datetime.now().strftime("MX_Appliance_Static Route_form_Network_"+str(UserChoiceNtwk)+"_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
                                mxStaticRoutePd.to_excel(MxStaticCsv, index=False)
                                print("** Excel file successfully saved **")
                            elif saveType == 2:
                                MxStaticCsv = datetime.now().strftime("MX_Appliance_Static Route_form_Network_"+str(UserChoiceNtwk)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
                                mxStaticRoutePd.to_csv(MxStaticCsv, index=False)
                                print("** CSV file successfully saved **")
                            #End csv file
                except meraki.APIError as e:
                    print (e)
                    print("\n")
                    main()
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
