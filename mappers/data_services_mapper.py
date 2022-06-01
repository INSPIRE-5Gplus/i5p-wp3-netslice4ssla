#!/usr/local/bin/python3.4

from doctest import OutputChecker
import os, sys, logging, json, argparse, time, datetime, requests, uuid
from xml.dom import minidom
from requests.auth import HTTPBasicAuth

from config_files import config_system as config_sys

CONTENT_HEADER_XML = {'Content-Type':'application/xml'}
CONTENT_HEADER_JSON = {'Content-Type':'application/json'}


# GETS DATA SERVICES CAPABILITIES INFO
def get_ds_capabilities():
    ds_ip = os.environ.get("DATASERV_IP")
    ds_port = os.environ.get("DATASERV_PORT")
    url = "http://"+ str(ds_ip) + ":" + str(ds_port) +"/capability"
    response = requests.get(url, headers=CONTENT_HEADER_JSON, auth=HTTPBasicAuth('admin', 'admin'))
    if response.status_code != 200:
        return [], response.status_code
    else:
        return response.text, response.status_code

# GETS DATA SERVICES ENABLERS INFO
def get_ds_enablers():
    ds_ip = os.environ.get("DATASERV_IP")
    ds_port = os.environ.get("DATASERV_PORT")
    url = "http://"+ str(ds_ip) + ":" + str(ds_port) +"/enabler"
    response = requests.get(url, headers=CONTENT_HEADER_JSON, auth=HTTPBasicAuth('admin', 'admin'))
    if response.status_code != 200:
        return [], response.status_code
    else:
        return response.text, response.status_code

# GETS DATA SERVICES SOFTWARE INFO
def get_ds_softwares():
    ds_ip = os.environ.get("DATASERV_IP")
    ds_port = os.environ.get("DATASERV_PORT")
    url = "http://"+ str(ds_ip) + ":" + str(ds_port) +"/software"
    response = requests.get(url, headers=CONTENT_HEADER_JSON, auth=HTTPBasicAuth('admin', 'admin'))
    if response.status_code != 200:
        return [], response.status_code
    else:
        return response.text, response.status_code

# GETS DATA SERVICES DEVICE INFO
def get_ds_devices():
    ds_ip = os.environ.get("DATASERV_IP")
    ds_port = os.environ.get("DATASERV_PORT")
    url = "http://"+ str(ds_ip) + ":" + str(ds_port) +"/device"
    response = requests.get(url, headers=CONTENT_HEADER_JSON, auth=HTTPBasicAuth('admin', 'admin'))
    if response.status_code != 200:
        return [], response.status_code
    else:
        return response.text, response.status_code

# Input
"""
    {
      "id": "64c4b6a6-d395-46ed-b3ae-a3351e515ee7",
      "name": "5GCore",
      "type": "5GCore",
      "version": 0.2,
      "vendor": "inspire5gplus",
      "shared": "False",
      "deployment-policy": "mspl_62ab08c8e76f4071bbd01892a83315cb"
    }
"""
# Output
"""
    {
      "id": "64c4b6a6-d395-46ed-b3ae-a3351e515ee7",
      "name": "5GCore",
      "type": "5GCore",
      "version": 0.2,
      "vendor": "inspire5gplus",
      "shared": "False",
      "deployment-policy": "mspl_62ab08c8e76f4071bbd01892a83315cb",
      "domain": "1"
    }
"""
def get_domains_subnet(subnet_item):
    config_sys.logger.info('DATA-SERVICES: Retrieving Service Capabilities information.')
    # GETS DATA SERVICES CAPABILITIES INFO
    response = get_ds_capabilities()
    ds_capabilities = json.loads(response[0])
    
    # GETS DATA SERVICES ENABLERS INFO
    response = get_ds_enablers()
    ds_enablers = json.loads(response[0])

    # GETS DATA SERVICES SOFTWARE INFO
    response = get_ds_softwares()
    ds_softwares = json.loads(response[0])

    # GETS DATA SERVICES DEVICE INFO
    response = get_ds_devices()
    ds_devices = json.loads(response[0])

    ## Processes the received data to add the right domain into each capability
    # getting the id of the capability
    for ds_cap_item in ds_capabilities:
        if subnet_item['name'] == ds_cap_item['name']:
            cap_id = ds_cap_item['id']
            break
    
    # getting the enablers ids having the capability
    enablers_list = []
    for enabler_item in ds_enablers:
        if cap_id in enabler_item['capabilities']:
            enablers_list.append(cap_id)
    
    # getting the software ids having the enablers
    softwares_list = []
    for software_item in ds_softwares:
        for ena_item in software_item['enablers']:
            if ena_item['id'] in enablers_list:
                softwares_list.append(software_item['id'])
    
    # getting the domain ids having the softwares
    domains_list = []
    for device_item in ds_devices:
        for soft_item in device_item['softwares']:
            if soft_item['id'] in softwares_list:
                domains_list.append(device_item['domain'])

    subnet_item['domains'] = domains_list
    return subnet_item, 200

#Input
"""
 [
   {
       "capability-ssla": "Channel_Protection"
       ...
   }
 ]
"""
#Output
"""
 [
   {
        "capability-ssla": "Channel_Protection",
        ...
        "domains":[2,4,5]
   }
 ]
"""
def get_domains_security_capability(capabilities):
    config_sys.logger.info('DATA-SERVICES: Retrieving Security Capabilities information.')
    # GETS DATA SERVICES CAPABILITIES INFO
    response = get_ds_capabilities()
    ds_capabilities = json.loads(response[0])
    
    # GETS DATA SERVICES ENABLERS INFO
    response = get_ds_enablers()
    ds_enablers = json.loads(response[0])

    # GETS DATA SERVICES SOFTWARE INFO
    response = get_ds_softwares()
    ds_softwares = json.loads(response[0])

    # GETS DATA SERVICES DEVICE INFO
    response = get_ds_devices()
    ds_devices = json.loads(response[0])

    # processes the received data to add the right domain into each capability  
    for capability_item in capabilities:
        for slo_item in capability_item['slos']:
            # getting the id of the capability
            for ds_cap_item in ds_capabilities:
                if ds_cap_item['name'] == slo_item['capability']:
                    cap_id = ds_cap_item['id']
                    break
            
            # getting the enablers ids having the capability
            enablers_list = []
            for enabler_item in ds_enablers:
                if cap_id in enabler_item['capabilities']:
                    enablers_list.append(cap_id)
            
            # getting the software ids having the enablers
            softwares_list = []
            for software_item in ds_softwares:
                for ena_item in software_item['enablers']:
                    if ena_item['id'] in enablers_list:
                        softwares_list.append(software_item['id'])
            
            # getting the domain ids having the softwares
            domains_list = []
            for device_item in ds_devices:
                for soft_item in device_item['softwares']:
                    if soft_item['id'] in softwares_list:
                        domains_list.append(device_item['domain'])
        
            capability_item['domains'] = domains_list
  
    return capabilities, 200