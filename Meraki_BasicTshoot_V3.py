"""Python Script - Meraki basic troubleshooting by NesALba """
from datetime import datetime
import meraki
import pandas as pd
import requests
import json

def print_banner():

    print("  __  __              _   _ ")
    print(" |  \/  |___ _ _ __ _| |_(_)")
    print(" | |\/| / =_) '_/ =` | / / |")
    print(" |_|  |_\___|_| \__,_|_\_\_|")
    print("      **Basic T-shoot**     ")
    print("         by @NesAlba        ")
    print()

def saveFiles (pdVar, sheet,xlsVar,csvVar):

    """Function to save files as XLS or CSV"""
    #This is the xlsVar example:  xlsVar= datetime.now().strftime("MyOrgs__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
    #This is the xlsVar example:  csvVar = datetime.now().strftime("MyOrgs__%m-%d-%Y-%Hh%Mm%Ss.csv")
    save = input("Q.Save to file? (Y/N): ")  # Save file
    save = save.upper()
    if save == "Y":
        print("1 -- Save as excel file")
        print("2 -- Save as csv file")
        saveType = input("Enter your option: ")
        if saveType == "1":  # Save to excel
            pdVar.to_excel(xlsVar, sheet_name=sheet, index=False)
            print("** Excel file successfully saved **")
        elif saveType == "2":  # Save to csv
            pdVar.to_csv(csvVar, index=False)
            print("** CSV file successfully saved **")
        else:
            print()
            print("** Invalid option **")
            print()
            print()
            merakiMenu()

def merakiOrgs(apiKey):

    """Function to get the Organizations list under your meraki API key"""
    try:
        dashboard = meraki.DashboardAPI(apiKey)
        response = dashboard.organizations.getOrganizations()
        listOrgs = []
        for orgs in response:
            orgsName = (orgs["name"])
            orgsId =  (orgs["id"])
            orgsLicense = (orgs["licensing"]["model"])
            listOrgsVar =[orgsName,orgsId,orgsLicense]
            listOrgs.append(listOrgsVar)
        Headers = ["Org Name", "Org ID", "Licensing"]
        orgsPd = pd.DataFrame(listOrgs, columns=Headers)
        orgsPd = orgsPd.reset_index(drop=True)
        orgsPd.index += 1
        print(orgsPd)
        xlsOrgsVar = datetime.now().strftime("MyOrgs__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
        csvOrgsVar = datetime.now().strftime("MyOrgs__%m-%d-%Y-%Hh%Mm%Ss.csv")
        saveFiles(orgsPd,"Orgs",xlsOrgsVar,csvOrgsVar)
        merakiMenu()
    except meraki.APIKeyError as e:
        print(e)
    except meraki.APIError as e:
        print(e)

def merakiNetworks(apiKey):

    """Function to get the Networks list under a specific Organization"""
    try:
        askOrg = input("Copy/paste Organization id: ")
        dashboard = meraki.DashboardAPI(apiKey)
        organization_id = askOrg
        response = dashboard.organizations.getOrganizationNetworks(organization_id, total_pages='all')
        listNetworks = []
        for networks in response:
            ntwksName = (networks["name"])
            ntwksId = (networks["id"])
            ntwksTimeZone = (networks["timeZone"])
            listNetworksVar = [ntwksName,ntwksId,ntwksTimeZone]
            listNetworks.append(listNetworksVar)
        Headers =["Network Name", "Network ID", "Time Zone"]
        ntwksPd = pd.DataFrame(listNetworks, columns=Headers)
        ntwksPd = ntwksPd.reset_index(drop=True)
        ntwksPd.index += 1
        print("** Networks in your organization")
        print(ntwksPd)
        xlsNetVar = datetime.now().strftime("Netwoks_in_Org_"+str(askOrg)+"__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
        csvNetVar = datetime.now().strftime("Netwoks_in_Org_"+str(askOrg)+"__%m-%d-%Y-%Hh%Mm%Ss.csv")
        saveFiles(ntwksPd,"Networks",xlsNetVar,csvNetVar)
        merakiMenu()
    except meraki.APIError as e:
        print(e)

def merakiDevicesNet(apiKey):
    """This function pull information about all devices in the selected network"""

    try:
        askNetwork = input("Enter Network id: ")
        dashboard = meraki.DashboardAPI(apiKey)
        response = dashboard.networks.getNetworkDevices(askNetwork)
        listDevices = []
        for devices in response:
            deviceToPrint = {
                "lanIp": devices["lanIp"] if "lanIp" in devices else None,
                "wan1Ip": devices["wan1Ip"] if "wan1Ip" in devices else None,
                "name": devices["name"] if "name" in devices else None,
                "serial": devices["serial"] if "serial" in devices else None,
                "model": devices["model"] if "model" in devices else None,
                "status": devices["status"] if "status" in devices else None,
                "tags": devices["tags"] if "tags" in devices else None,
            }
            deviceName = (deviceToPrint["name"])
            deviceSerial = (deviceToPrint["serial"])
            deviceModel = (deviceToPrint["model"])
            devieLanIp = (deviceToPrint["lanIp"])
            deviceWanIp = (deviceToPrint["wan1Ip"])
            deviceTag = (deviceToPrint["tags"])
            listDevicesVar = [deviceName, deviceSerial, deviceModel, devieLanIp, deviceWanIp, deviceTag]
            listDevices.append(listDevicesVar)
        Headers = ["Name", "Serial", "Model", "Lan ip", "Wan ip", "Tag"]
        devicesPd = pd.DataFrame(listDevices,columns=Headers)
        devicesPd = devicesPd.sort_values("Lan ip")
        devicesPd.reset_index(drop=True)
        devicesPd.index +=1
        print("** Devices in your network **")
        print(devicesPd)
        xlsDevVar = datetime.now().strftime("Devices_in_Network_"+str(askNetwork)+"_by_IP__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
        csvDevVar = datetime.now().strftime("Devices_in_Network_"+str(askNetwork)+"_by_IP__%m-%d-%Y-%Hh%Mm%Ss.csv")
        saveFiles(devicesPd, "Devices",xlsDevVar,csvDevVar)
        merakiMenu()
    except meraki.APIError as e:
        print(e)
    except Exception as a:
        print(a)

def merakiMenu():
    """This function has the main menu"""
    try:
        print()
        print("** Menu **")
        print("----------")
        print("1 -- Show my Organizations")
        print("2 -- Show my Networks")
        print("3 -- Devices in your network")
        print("4 -- Wireless info")
        print("5 -- Switch info")
        print("6 -- MX applicance info")
        print("7 -- Blink device leds")
        print("8 --> EXIT <--")

        deviceSelect = input("Type your choice: ")
        if deviceSelect == "1":
            merakiOrgs(apiKey)
        elif deviceSelect == "2":
            merakiNetworks(apiKey)
        elif deviceSelect == "3":
            merakiDevicesNet(apiKey)
        elif deviceSelect == "4":
            merakiWirelessMenu()
        elif deviceSelect == "5":
            merakiSwitch(apiKey)
        elif deviceSelect == "6":
            merakiMxMenu()
        elif deviceSelect == "7":
            merakiBlinkLed(apiKey)
        elif deviceSelect == "8":
            print()
            print(" -- Hope this helped you --")
            print("         Goodbye!          ")
            quit()
        else:
            print()
            print("** Invalid option **")
            print()
            print()
            merakiMenu()
    except KeyboardInterrupt:
        print()
        print(" -- Program terminated manually --")
        print("            Goodbye!              ")
        print()
        raise SystemExit

def merakiWirelessMenu():

    """This function has a Wireless Menu"""
    print()
    print("** Wireless Menu **")
    print("-------------------")
    print("1 -- MR Device info")
    print("2 -- Network Wireless RF Profiles info")
    print("3 -- Organization Top SSIDs by Usage")
    print("4 -- Network Ssids info")
    print("5 --> BACK <--")
    choiceWireless = input("Type your choice: ")
    if choiceWireless == "1":
        merakiMrInfo(apiKey)
    elif choiceWireless == "2":
        merakRfProf(apiKey)
    elif choiceWireless == "3":
        merakiWlessTopSsid(apiKey)
    elif choiceWireless == "4":
        merakiNetworkSsid(apiKey)
    elif choiceWireless == "5":
        merakiMenu()
    else:
        print()
        print("** Invalid option **")
        print()
        print()
        merakiMenu()

def merakiMrInfo(apiKey):

    """This function pull information about an specific MR form the network"""
    try:
        print()
        print("** MR device info **")
        print("i - you can pull MR device serial from Menu>Devices in your network")
        choiceMr = input("Type MR device serial: ")
        dashboard = meraki.DashboardAPI(apiKey)
        response = dashboard.wireless.getDeviceWirelessStatus(choiceMr)
        listApsInfo=[]
        for apsInfo in response["basicServiceSets"]:
            if apsInfo["enabled"]==True:
                mrSsid = (apsInfo["ssidName"])
                mrBand = (apsInfo["band"])
                mrChan = (apsInfo["channel"])
                mrChanWidth = (apsInfo["channelWidth"])
                mrPower = (apsInfo["power"])
                mrBroad = (apsInfo["broadcasting"])
                mrVisible = (apsInfo["visible"])
                listApsVar = [mrSsid, mrBand, mrChan, mrChanWidth, mrPower, mrBroad, mrVisible]
                listApsInfo.append(listApsVar)
        Headers = ["SSID", "Band", "Channel", "ChanWidth", "Power", "Broadcasting", "Visible"]
        mrInfoPd = pd.DataFrame(listApsInfo, columns=Headers)
        mrInfoPd.index +=1
        print()
        print("** Wireless info **")
        print(mrInfoPd)
        xlsMrVar = datetime.now().strftime("Wireless_MR_"+str(choiceMr)+"_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
        csvMrVar = datetime.now().strftime("Wireless_MR_"+str(choiceMr)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
        saveFiles(mrInfoPd, "MR Device info", xlsMrVar,csvMrVar)
        merakiWirelessMenu()
    except meraki.APIError as e:
        print(e)
    except Exception as a:
        print(a)

def merakRfProf(apiKey):

    """This function pull information about custom RF profiles in a network"""
    try:
        print()
        print("** Custom Network RF profiles info **")
        print("i - you can pull the Network id from 'Menu>Devices' in your network")
        askNetwork = input("Copy/paste Network id: ")
        dashboard = meraki.DashboardAPI(apiKey)
        response = dashboard.wireless.getNetworkWirelessRfProfiles(askNetwork)
        if response == []:
            print("\n")
            print("** No Custom RF Profiles in this Network **")
            print()
            merakiWirelessMenu()
        else:
            listRf = []
            for rfSett in response:
                rfName =(rfSett["name"])
                rf24max =(rfSett["twoFourGhzSettings"]["maxPower"])
                rf24min =(rfSett["twoFourGhzSettings"]["minPower"])
                rf24minBit =(rfSett["twoFourGhzSettings"]["minBitrate"])
                rf5max =(rfSett["fiveGhzSettings"]["maxPower"])
                rf5min =(rfSett["fiveGhzSettings"]["minPower"])
                rf5minBit =(rfSett["fiveGhzSettings"]["minBitrate"])
                listRfVar = [rfName, rf24max, rf24min, rf24minBit, rf5max, rf5min, rf5minBit]
                listRf.append(listRfVar)
            Headers = ["Name", "2.4 MaxPower", "2.4 minPower", "2.4 minBitrate", "5Ghz MaxPower", "5Ghz minPower", "5Ghz minBitrate"]
            rfInfoPd = pd.DataFrame(listRf, columns=Headers)
            rfInfoPd.index +=1
            print("** Custom Network RF profiles info **")
            print(rfInfoPd)
            xlsRfVar = datetime.now().strftime("Wireless_RF_Network"+str(askNetwork)+"_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
            csvRfVar = datetime.now().strftime("Wireless_RF_Network"+str(askNetwork)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
            saveFiles(rfInfoPd, "RF Profiles", xlsRfVar, csvRfVar)
            merakiWirelessMenu()
    except meraki.APIError as e:
        print(e)

def merakiWlessTopSsid(apiKey):

    """This function pull the top SSIDs on the Organization"""
    try:
        askOrg = input("Copy/paste Organization id: ")
        t0 = input("Start Date(YYYY-MM-DD): ")
        t1 = input("End Date(YYYY-MM-DD): ")
        t0hr = input("Start Time(hh:mm:ss): ")
        t1hr = input("End Time(hh:mm:ss): ")
        payload = {}
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Cisco-Meraki-API-Key": str(apiKey)
        }
        apiTopSsid = "/organizations/"+str(askOrg)+"/summary/top/ssids/byUsage?t0="+str(t0)+"T"+str(t0hr)+"Z&t1="+str(t1)+"T"+str(t1hr)+"Z"
        urlTopSsid = "https://api.meraki.com/api/v1/" + str(apiTopSsid)

        responseTopSsid = requests.request('GET', urlTopSsid, headers=headers, data=payload)
        response = json.loads(responseTopSsid.text.encode('utf8'))
        """dashboard = meraki.DashboardAPI(apiKey)
        response = dashboard.organizations.getOrganizationSummaryTopSsidsByUsage(askOrg)"""
        listTopSsids = []
        for topSsids in response:
            topSsidName = (topSsids["name"])
            topSsidTotal = round(topSsids["usage"]["total"])
            topSsidPrct = (topSsids["usage"]["percentage"])
            topSsidClients = (topSsids["clients"]["counts"]["total"])
            listTopSsidsVar = [topSsidName, topSsidTotal, topSsidClients, topSsidPrct]
            listTopSsids.append(listTopSsidsVar)
        Headers = ["SSID Name", "Total Usage MB", "Clients","Total Percentage"]
        topSsidsPd = pd.DataFrame(listTopSsids, columns= Headers)
        topSsidsPd.index +=1
        print("** Organization Top SSIDs by Usage in Megabytes** ")
        print(topSsidsPd)
        xlsTopVar = datetime.now().strftime("Top_SSIDs_in_Org_"+str(askOrg)+"_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
        csvTopVar = datetime.now().strftime("Top_SSIDs_in_Org_"+str(askOrg)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
        saveFiles(topSsidsPd, "Top SSIDs",xlsTopVar, csvTopVar)
        merakiWirelessMenu()
    except meraki.APIError as e:
        print(e)
    except Exception as a:
        print(a)

def merakiNetworkSsid(apiKey):

    """This function pull info about the SSIDs form the selected network"""
    try:
        print("** Netwotk SSIDs info  **")
        print("i - you can pull the Network id from 'Menu>Devices' in your network")
        askNetwork = input("Copy/paste Network id: ")
        dashboard = meraki.DashboardAPI(apiKey)
        response = dashboard.wireless.getNetworkWirelessSsids(askNetwork)
        listSsidsNet = []
        for ssidsInf in response:
            if ssidsInf["enabled"] == True:
                ssidsName = (ssidsInf["name"])
                ssidsAuth = (ssidsInf["authMode"])
                ssidsEnc = (ssidsInf["encryptionMode"])
                ssidsWpa = (ssidsInf["wpaEncryptionMode"])
                ssidsIpAss = (ssidsInf["ipAssignmentMode"])
                if ssidsInf["authMode"] == "8021x-radius":
                    for ssidsRadVar in ssidsInf["radiusServers"]:
                        ssidsRad = (ssidsRadVar["host"])
                        ssidsRadPort = (ssidsRadVar["port"])
                else:
                    ssidsRad = "None"
                    ssidsRadPort = "None"
                    listSsidsVar = [ssidsName, ssidsAuth, ssidsEnc, ssidsWpa, ssidsRad, ssidsRadPort, ssidsIpAss]
                    listSsidsNet.append(listSsidsVar)
        Headers = ["ssidName","Auth", "Encryption","WPAmode","Radius","radiusPort", "ipAssignment"]
        ssidsPd = pd.DataFrame(listSsidsNet, columns=Headers)
        ssidsPd.index +=1
        print("** Network SSIDs info **")
        print(ssidsPd)
        xlsSsidNetVar = datetime.now().strftime("SSIDs_in_Network_"+str(askNetwork)+"_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
        csvSsidBetVar = datetime.now().strftime("SSIDs_in_Network_"+str(askNetwork)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
        saveFiles(ssidsPd, "Network SSIDs info", xlsSsidNetVar, csvSsidBetVar)
        merakiWirelessMenu()
    except meraki.APIError as e:
        print(e)

def merakiSwitch(apiKey):

    """This function pull a specific switch information  """
    try:
        print()
        print("** Switch info **")
        print("i -- you can pull switch serial number from Menu>Devices in your network")
        choiceMs = input("Type MS device serial: ")
        dashboard =meraki.DashboardAPI(apiKey)
        response = dashboard.switch.getDeviceSwitchPortsStatuses(choiceMs)
        listMsInfo= []
        for ports in response:
            msPort =(ports["portId"])
            msUplink = (ports["isUplink"])
            msSpeed = (ports["speed"])
            msDuplex = (ports["duplex"])
            msErrors = (ports["errors"])
            msWarnings = (ports["warnings"])
            listMsInfoVar = [msPort, msUplink, msSpeed, msDuplex, msErrors, msWarnings]
            listMsInfo.append(listMsInfoVar)
        Headers = ["Port", "Uplink", "Speed", "Duplex", "Errors", "Warnings"]
        msInfoPd = pd.DataFrame(listMsInfo, columns=Headers)
        msInfoPd.index +=1
        print()
        print("** Switch info **")
        print(msInfoPd)
        xlsSwVar = datetime.now().strftime("Switch_MS_"+str(choiceMs)+"_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
        csvSwVar = datetime.now().strftime("Switch_MS_"+str(choiceMs)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
        saveFiles(msInfoPd,"MS info",xlsSwVar,csvSwVar)
        print()
        moreMsInfo = input("Q -- Do you want more info about this MS device?(Y/N): ")
        moreMsInfo = moreMsInfo.upper()
        if moreMsInfo == "Y":
            dashboard = meraki.DashboardAPI(apiKey)
            response = dashboard.switch.getDeviceSwitchPorts(choiceMs)
            listMsPortInfo = []
            for ports in response:
                msPortInfoPort = (ports["portId"])
                mSPortInfoPOE = (ports["poeEnabled"])
                msPortInfoVlan = (ports["vlan"])
                msPortInfoVoiceLan = (ports["voiceVlan"])
                msPortInfoType = (ports["type"])
                msPortInfoRSTP = (ports["rstpEnabled"])
                msPortInfoSTP = (ports["stpGuard"])
                msPortInfoName = (ports["name"])
                mSPortInfoAllowedVlans = (ports["allowedVlans"])
                listMsPortInfoVar = [msPortInfoPort, mSPortInfoPOE, msPortInfoVlan, msPortInfoVoiceLan,
                                     mSPortInfoAllowedVlans, msPortInfoType, msPortInfoRSTP, msPortInfoSTP,
                                     msPortInfoName]
                listMsPortInfo.append(listMsPortInfoVar)
            Headers = ["Port", "PoE", "Vlan", "voiceVlan", "allowedVlans", "Type", "RSTP", "STP Guard", "Description"]
            msPortInfoPD = pd.DataFrame(listMsPortInfo, columns=Headers)
            print()
            print("** MS detailed ports info **")
            print(msPortInfoPD)
            xlsSwInfVar = datetime.now().strftime("Switch_MS_"+str(choiceMs)+"_Ports_detailed_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
            csvSwInfVar = datetime.now().strftime("Switch_MS_"+str(choiceMs)+"_Ports_detailed_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
            saveFiles(msPortInfoPD, "Port detailed Info", xlsSwInfVar, csvSwInfVar)
        merakiMenu()
    except meraki.APIError as e:
        print(e)

def merakiMxMenu():

    """This function has MX applicance menu"""
    print()
    print ("** MX Menu **")
    print("--------------")
    print("1 -- Mx in Organization Sie-To-Site VPN")
    print("2 -- MX in Network Uplink Status")
    print("3 -- MX in Network Static Routes")
    print("4 --> BACK <--")
    choiceMx = input("Type your choice: ")
    if choiceMx == "1":
        merakiStSVpn(apiKey)
    elif choiceMx =="2":
        merakiMxUplink(apiKey)
    elif choiceMx =="3":
        merakiMxStatic(apiKey)
    elif choiceMx == "4":
        merakiMenu()
    else:
        print()
        print("** Invalid option **")
        print()
        print()
        merakiMenu()

def merakiStSVpn(apiKey):
    """This function pull information about Site-to-Site Vpn from Organization"""
    try:
        print()
        askOrg = input("Enter an Organization id: ")
        dashboard = meraki.DashboardAPI(apiKey)
        response = dashboard.appliance.getOrganizationApplianceVpnStatuses(askOrg, total_pages='all')
        listVpnInfo = []
        for vpnStatuses in response:
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
        print("** Organization Site-To-Site VPN info")
        print(vpnInfoPd)
        xlsVpnVar = datetime.now().strftime("MX_Site-to-Site_VPN_"+str(askOrg)+"_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
        csvVpnVar = datetime.now().strftime("MX_Site-to-Site_VPN_"+str(askOrg)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
        saveFiles(vpnInfoPd, "Site-To-Site", xlsVpnVar, csvVpnVar)
        merakiMxMenu()
    except meraki.APIError as e:
        print(e)

def merakiMxUplink(apiKey):

    """This function pull uplink information from netwok"""
    try:
        print()
        askNetwork = input("Enter Network id: ")
        dashboard = meraki.DashboardAPI(apiKey)
        response = dashboard.appliance.getNetworkApplianceVlans(askNetwork)
        listMxVlans = []
        for mxVlans in response:
            wMxVlanNtwk = (mxVlans["networkId"])
            wMxVlanId = (mxVlans["id"])
            wMxVlanName = (mxVlans["name"])
            wMxAppIp = (mxVlans["applianceIp"])
            wMxSubnet = (mxVlans["subnet"])
            wMxDns = (mxVlans["dnsNameservers"])
            wMxDhcpHand = (mxVlans["dhcpHandling"])
            listMxVlansVar = [wMxVlanNtwk, wMxVlanId, wMxVlanName, wMxAppIp, wMxSubnet, wMxDns, wMxDhcpHand]
            listMxVlans.append(listMxVlansVar)
        Headers = ["Network ID", "Vlan", "Name", "applicanceIP", "Subnet", "DNS", "dhcpHandling"]
        mxVlansPd = pd.DataFrame(listMxVlans, columns=Headers)
        mxVlansPd.index += 1
        print("** Network Uplink Info **")
        print(mxVlansPd)
        xlsMxVlanVar = datetime.now().strftime("MX_Appliance_Vlans_form_Network_"+str(askNetwork)+"_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
        csvMxVlanVar = datetime.now().strftime("MX_Appliance_Vlans_form_Network_"+str(askNetwork)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
        saveFiles(mxVlansPd, "Uplinks", xlsMxVlanVar, csvMxVlanVar)
        merakiMxMenu()
    except meraki.APIError as e:
        print(e)

def merakiMxStatic(apiKey):

    """This function pull static routes from slected network"""
    try:
        print()
        askNetwork = input("Enter Network id: ")
        dashboard = meraki.DashboardAPI(apiKey)
        response = dashboard.appliance.getNetworkApplianceStaticRoutes(askNetwork)
        if response == []:
            print("\n")
            print("** No Static Routes in this Network **")
        else:
            listMXStaticRoutes = []
            for MxStatic in response:
                wMxStaticNtwk = (MxStatic["networkId"])
                wMxStaticName = (MxStatic["name"])
                wMxStaticSubnet = (MxStatic["subnet"])
                wMxStaticGw = (MxStatic["gatewayIp"])
                listMxStaticVar = [wMxStaticNtwk, wMxStaticName, wMxStaticSubnet, wMxStaticGw]
                listMXStaticRoutes.append(listMxStaticVar)
            Headers = ["Network ID", "Name", "Subnet", "Gateway"]
            mxStaticRoutePd = pd.DataFrame(listMXStaticRoutes, columns=Headers)
            mxStaticRoutePd.index += 1
            print("** Network Static Routes **")
            print(mxStaticRoutePd)
            xlsStaticVar = datetime.now().strftime("MX_Appliance_Static Route_form_Network_"+str(askNetwork)+"_info__%m-%d-%Y-%Hh%Mm%Ss.xlsx")
            csvStaticVar = datetime.now().strftime("MX_Appliance_Static Route_form_Network_"+str(askNetwork)+"_info__%m-%d-%Y-%Hh%Mm%Ss.csv")
            saveFiles(mxStaticRoutePd, "StaticRoutes",xlsStaticVar, csvStaticVar)
            merakiMxMenu()
    except meraki.APIError as e:
        print(e)

def merakiBlinkLed(apiKey):

    try:
        print("i -- Blink device leds")
        dashboard = meraki.DashboardAPI(apiKey)
        choosedevice = input("Type device serial number: ")
        chooseDuration = input ("For how long?(in sec):")
        response = dashboard.devices.blinkDeviceLeds(
            choosedevice,
            duration=20,
            period=160,
            duty=50
        )
    except meraki.APIError as e:
        print(e)

#Program strats here
print_banner()
apiKey = input("Enter your Meraki API Key: ")
merakiMenu()

