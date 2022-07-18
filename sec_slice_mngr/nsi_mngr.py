#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, requests, uuid
from datetime import datetime
from xml.dom import minidom 
import xml.etree.ElementTree as ET

from config_files import config_system as config_sys
from databases import nst_db_mngr
from databases import secnsi_db_mngr
from sec_slice_mngr import slice2mspl
from mappers import pf_mapper as e2e_pf
from mappers import so_mapper as e2e_so
from mappers import ssla_mngr_mapper as e2e_ssla
from mappers import data_services_mapper as e2e_ds

# manages the process to store the received NST, generate the NSI and MSPL objects associated.
def deploy_sec_nsi_test():
  config_sys.logger.info("Getting the XML")
  ssla_doc = "./data_objects/e2e-5g-slice-ssla1_v2.xml"
  config_sys.logger.info("This is the XML: " + str(ssla_doc))

  # Sends MSPL to the E2E SO
  so_ip = os.environ.get("SO_IP")
  config_sys.logger.info("so_ip: " + str(so_ip))
  so_port = os.environ.get("SO_PORT")
  config_sys.logger.info("so_port: " + str(so_port))
  url = "http://"+ str(so_ip) + ":" + str(so_port) +"/e2emeservice"
  config_sys.logger.info("url: " + str(url))
  header = {'Content-Type': 'application/xml; charset=UTF-8', 'Cache-Control': 'no-cache', 'Accept': 'application/json',}
  config_sys.logger.info("header: " + str(header))
  with open(ssla_doc) as xml:
    response = requests.post(url, data=xml, headers=header)
    config_sys.logger.info("______________________________________________________________________________")
    config_sys.logger.info("This is the response: " + str(response))
    config_sys.logger.info("******************************************************************************")
    config_sys.logger.info("This is the response.text: " + str(response.text))
    config_sys.logger.info("This is the response.status_code: " + str(response.status_code))
    if response.status_code != 200:
      config_sys.logger.info('NSI-MNGR: E2E_SO STATUS:' + str(response.status_code))
      config_sys.logger.info('NSI-MNGR: E2E_SO RESPONSE:' + str(response.text))
      return response.text, response.status_code
    else:
      #TODO: process the response.text from the E2E SO
      config_sys.logger.info('NSI-MNGR: E2E_SO RESPONSE:' + str(response.text))
      return response.text, response.status_code

def deploy_sec_nsi(request_json, ssla_string, start_ts):
  config_sys.logger.info('NSI-MNGR: Deploying E2E NST: ' + str(request_json["nst"]["name"])+ ' with SSLA ID: '+ str(request_json['ssla_id']))

  # Stores received E2E NST
  response = nst_db_mngr.add_nst(request_json["nst"])

  # Prepares Sec_NSI data object structure
  sec_nsi = {}
  sec_nsi["id"] = str(uuid.uuid4())
  # Prepares a id base 10 based on timestamp for the E2E SO
  dt = datetime.now()
  ts = str(round(dt.timestamp()))
  sec_nsi['base10_id'] = ts
  sec_nsi["name"] = request_json["nst"]["name"]
  sec_nsi["description"] = request_json["nst"]["description"]
  sec_nsi["nst-ref"] = request_json["nst"]["id"]
  # Copies the info about the QoS
  sec_nsi["quality-of-service"] = request_json["nst"]["quality-of-service"]

  # Copies the slice-subnets information
  sec_nsi["netslice-subnets"] = request_json["nst"]["netslice-subnets"]
  for subnet_item in sec_nsi["netslice-subnets"]:
    # Obtains the deployment MSPL policy ID
    mspl_id = str(uuid.uuid4())
    mspl_id = mspl_id.replace('-', '')
    mspl_id = "mspl_"+mspl_id
    subnet_item["deployment-policy"] = mspl_id
 
  # Parses the received SSLA from string to XML (minidom library)
  ssla_info = {}
  ssla_info["id"] = request_json['ssla_id']
  
  ssla_xml = minidom.parseString(ssla_string) #NOTE: REAL DEMO uncomment & comment below
  #ssla_xml = ssla_string
  
  # Obtains the SSLA name
  ssla_name2 = ssla_xml.getElementsByTagName("wsag:Name")[0]
  ssla_info["name"] = str(ssla_name2.firstChild.data)
  
  # Obtains the SSLA capabilities and the policies to apply based on them
  capabilities_list = ssla_xml.getElementsByTagName("specs:capability")
  caps_list = []
  for capability in capabilities_list:
    cap_id = capability.getAttribute("id")
    caps_list.append(cap_id)
  
  response = e2e_pf.get_policies_sla_capability(caps_list)
  policies_list = response[0]

  # prepare the policies/capabilities info to generate the MSPL and be added into the NSI
  # Prepares the policies info to store it in the slice instance object
  capabilities = []
  for subnet_item in sec_nsi["netslice-subnets"]:
    if subnet_item['domain'] != '':
      temp_policies_list = policies_list.copy()
      for pol_item in temp_policies_list:
        selected_pol = False
        temp_pol = pol_item.copy()
        for pol_option in temp_pol['policy']:
          for pol_option_item in pol_option['slice']:
            if subnet_item['name'] == pol_option_item:
              config_sys.logger.info('NSI-MNGR: Policy Found for the service!')
              # Reduces and prepares the capabilities info to attach it in the NSI
              mspl_id = str(uuid.uuid4())
              mspl_id = mspl_id.replace('-', '')
              mspl_id = "mspl_"+mspl_id
              temp_pol["mspl_id"] = mspl_id
              temp_pol.pop("policy", None)
              capabilities.append(temp_pol)
              
              # NOTE: this next steps need to be rethink, but for the KPIs we keep just the neede element
              # Modifies the policies_list to have only the right policies to deploy (if below is related)
              selected_pol = True
              temp_pol_option_item = pol_option.copy()
              break
        if selected_pol == True:
          pol_item_policy = []
          pol_item_policy.append(temp_pol_option_item)
          pol_item['policy'] = pol_item_policy
          
  # obtains the SMDs where to deploy the security elements
  service_list = []
  for subnet_item in sec_nsi["netslice-subnets"]:
      service_list.append(subnet_item['name'])
  response = e2e_ds.get_domains_security_capability(capabilities, service_list)
  if response[1] != 200:
    pass
  else:
    capabilities = response[0]
  
  ssla_info["capabilities"] = capabilities
  sec_nsi["security-sla"] = ssla_info
  #config_sys.logger.info('NSI-MNGR: ssla_info:' + str(ssla_info))
  
  # NOTE: this piece of code is hardcoded for the SSLA2 due to a problem with the information in the Data Service
  # ----------
  if ssla_info['id'] == '5G_IOT_BROKER_SSLA':
    for capability_item in ssla_info['capabilities']:
      if capability_item['capability-ssla'] == 'Channel_Protection':
        capability_item['domains'] = [6,7]
      if capability_item['capability-ssla'] == 'Network_traffic_analysis':
        capability_item['domains'] = [6]
  # ----------
  
  config_sys.logger.info('NSI-MNGR: ssla_info:' + str(ssla_info))

  # saves NSI into the Database
  response = secnsi_db_mngr.add_sec_nsi(sec_nsi)
  if response[1] != 200:
    config_sys.logger.error(response[0])
  
  config_sys.logger.info('NSI-MNGR: NSI DATA OBJECT READY:' + str(sec_nsi))
  # Prepares MSPL (XML format) data request to deploy
  xml_tree = slice2mspl.generateMSPL(sec_nsi, temp_policies_list)
  config_sys.logger.info('NSI-MNGR: MSPL READY FOR THE E2E SO:' + str(xml_tree))
  
  # Sends MSPL to the E2E SO
  response = e2e_so.request_deployment(xml_tree) #NOTE: REAL DEMO uncomment & comment below
  #response= ["msg", 200]

  # Validates policy is applied = Sec_NSI is deployed
  if response[1] == 200:
    sec_nsi["status"] = "INSTANTIATED"
  else:
    sec_nsi["status"] = "ERROR"
  response = secnsi_db_mngr.update_sec_nsi(sec_nsi['id'], sec_nsi)
  config_sys.logger.info('NSI-MNGR: NSI DATA OBJECT READY:' + str(sec_nsi))
  config_sys.logger.info(response[0])

  # Logs the initial (deployment) time KPI (DO NOT REMOVE)
  end_ts = datetime.now()
  delta = end_ts - start_ts
  tsecs = delta.total_seconds()
  config_sys.logger_kpi.info('***********************************************************')
  config_sys.logger_kpi.info('START DEPLOYMENT TIME ->' + str(start_ts))
  config_sys.logger_kpi.info('FINAL DEPLOYMENT TIME ->' + str(end_ts))
  config_sys.logger_kpi.info('TOTAL DEPLOYMENT TIME (sec) ->' + str(delta))

def update_sec_nsi(nsi_json):
  # TODO: nsi_json (nsi_uuid, subnet_uuid, status)
  # TODO: take nsi_uuid to get it from DB, look for the slice-subnet based with the subnet_uuid) & update status
  pass

def terminate_sec_nsi(sec_nsi_uuid):
    config_sys.logger.info('GET SEC NSI')
    # TODO: Gets Sec_NSI data object structure
    response = secnsi_db_mngr.get_sec_nsi(sec_nsi_uuid)
    if response[1] == 200:
        sec_nsi_json = response[0]["msg"]
    else:
        return response[0], response[1]

    # TODO: Prepares MSPL (XML format) data request to terminate

    # TODO: Validates policy is applied = Sec_NSI is terminated
    sec_nsi_json["status"] = "TERMINATED"
    response = secnsi_db_mngr.update_sec_nsi(sec_nsi_json["uuid"], sec_nsi_json)

def remove_sec_nsi(sec_nsi_uuid):
    # Remove Sec NSI from DB
    response = secnsi_db_mngr.remove_sec_nsi(sec_nsi_uuid)
    return response[0], response[1]

def get_sec_nsis():
    # Retrieve all Sec NSI data objects from DB
    response = secnsi_db_mngr.get_sec_nsis()
    return response[0], response[1]

def get_sec_nsi(sec_nsi_uuid):
    # Retrieve specific Sec NSI data object from DB
    response = secnsi_db_mngr.get_sec_nsi(sec_nsi_uuid)
    return response[0], response[1]