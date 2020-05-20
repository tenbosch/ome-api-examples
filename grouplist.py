import os
import subprocess
import sys
import argparse
from argparse import RawTextHelpFormatter
import requests
import getpass
import json
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#Get current sessions
strIP = '192.168.1.200'
strBaseURI = 'https://%s' % (strIP)
strSessionURL = 'https://%s/api/SessionService/Sessions' % (strIP)
strGroupURL = 'https://%s/api/GroupService/Groups' % (strIP)
strDeviceURL = 'https://%s/api/DeviceService/Devices' % (strIP)
strHeaders = {'content-type': 'application/json'}
strUsername = input("Enter Username: ")
strPassword = getpass.getpass(prompt='Enter Password: ')
strGroupName = input('Group Name: ')
strUserDetails = {'UserName': strUsername,
                  'Password': strPassword,
                  'SessionType': 'API'}
strNextGroupURL = None
print('\n')
strResponse = requests.post(strSessionURL, verify=False, data=json.dumps(strUserDetails), headers=strHeaders)

# print(strResponse.status_code)

strHeaders['X-Auth-Token'] = strResponse.headers['X-Auth-Token']
# print(strHeaders['X-Auth-Token'])

strGroups = requests.get(strGroupURL, headers=strHeaders, verify=False)
# print(strGroups.status_code)

#print(json.dumps(strGroups.json(), indent=4, sort_keys=True))

strGroupList = strGroups.json()
strGroupCount = strGroupList['@odata.count']

# print(strGroupList['value'])
for group in strGroupList['value']:
        if (group['Name'] == strGroupName):
                print('Group: ' + group['Name'] + ' found!')
                strDevicesURL = strGroupURL + "(" + str(group['Id']) + ")/Devices"
                strDevices = requests.get(strDevicesURL, headers=strHeaders, verify=False)
                # print('  Status Code: ' + str(strDevices.status_code))

                strDeviceList = strDevices.json()

                for devices in strDeviceList['value']:
                    strDeviceId = str(devices['Id'])
                    strDeviceName = str(devices['DeviceName'])
                    strDeviceDetailURL = strDeviceURL + "(" + strDeviceId + ")"
                    strDevice = requests.get(strDeviceDetailURL, headers=strHeaders, verify=False)
                    strDeviceDetail = strDevice.json()
                    # print(json.dumps(strDevice.json(), indent=4))
                    strManagement = strDeviceDetail['DeviceManagement'][0]
                    strDeviceDRACIP = strManagement['NetworkAddress']
                    print(strDeviceId + ' - ' + strDeviceName + ' - iDRAC IP Address: ' + strDeviceDRACIP)
                    #os.system("racadm -r " + $strDeviceDRACIP + " -u root -p " + strPassword + "getsysinfo --nocertwarn")
                    strReturnData = subprocess.run(["racadm", "-r", strDeviceDRACIP, "-u", "root", "-p", strPassword, "getsysinfo", "--nocertwarn"])
                    print(strReturnData.returncode)
        # else:
                # print(group['Name'])