#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
from xml.dom import minidom 

from config_files import config_system as config_sys
from databases import nst_db_mngr
from databases import secnsi_db_mngr
from sec_slice_mngr import slice2mspl
from mappers import pf_mapper as e2e_pf

"""
  {
    "nst": {
      "id":  "ca15d4fa-2bdc-41fb-9e25-82aaaf8c9e67",
      "name": "5g_voip_service_nst",
      "version": 0.2,
      "vendor": "inspire5gplus",
      "author": "inspire5gplus",
      "SNSSAI_identifier": {
        "slice-service-type": "eMBB",
        "slice-differentiator": "ca15d4fa-2bdc-41fb-9e25-82aaaf8c9e67"
      },
      "quality-of-service": {
        "availability": "99.9"
      },
      "netslice-subnets": [
        {
          "id": "64c4b6a6-d395-46ed-b3ae-a3351e515ee7",
          "name": "5GService-5GVoIP",
          "version": 0.2,
          "vendor": "inspire5gplus",
          "shared": "False"
        }
      ],
      "netslice-connection-point":[],
      "netslice-vld": [],
      "netslicefgd": []
    },
    "ssla_id": "uuid"
  }
"""
def deploy_sec_nsi(request_json, ssla_object):
  config_sys.logger.info('NSI-MNGR: Deploying E2E NST: ' + str(request_json["nst"]["name"])+ ' with SSLA ID: '+ str(request_json['ssla_id']))

  # Stores received E2E NST
  response = nst_db_mngr.add_nst(request_json["nst"])

  # Prepares Sec_NSI data object structure
  sec_nsi = {}
  sec_nsi["id"] = str(uuid.uuid4())
  sec_nsi["name"] = request_json["nst"]["name"]
  sec_nsi["description"] = request_json["nst"]["description"]
  sec_nsi["nst-ref"] = request_json["nst"]["id"]
  sec_nsi["status"] = "INSTANTIATING"

  # Copies the slice-subnets information
  #response = nst_db_mngr.get_nst(request_json["id"])
  #sec_nsi["netslice-subnets"] = response[0]["msg"]["netslice-subnets"]
  sec_nsi["netslice-subnets"] = request_json["nst"]["netslice-subnets"]

  # Copies the info about the QoS
  sec_nsi["quality-of-service"] = request_json["nst"]["quality-of-service"]
  
  # TODO: obtain the SMDs where to apply the slice (from Data Services)
  location_smd = []
  sec_nsi["location-smd"] = location_smd
  
  # obtain the deployment MSPL policy ID
  mspl_id = str(uuid.uuid4())
  mspl_id = mspl_id.replace('-', '')
  mspl_id = "mspl_"+mspl_id
  sec_nsi["deployment-policy"] = mspl_id
  
  #add all the policies associated to the SSLA.
  ssla_info = {}
  ssla_info["id"] = request_json['ssla_id']
  ssla_name = ssla_object.getElementsByTagName("wsag:Name")[0]
  ssla_info["name"] = str(ssla_name.firstChild.data)
  
  #TODO: to process and obtain the sloIDs for the security-requirements
  ssla_info["security-requirements"] = []

  # obtains the policies to apply based on the SSLA capabilites requested
  capabilities_list = ssla_object.getElementsByTagName("specs:capability")
  caps_list = []
  for capability in capabilities_list:
    cap_id = capability.getAttribute("id")
    caps_list.append(cap_id)
    config_sys.logger.info('NSI-MNGR: CAPABILITY ID FORM SSLA:' + str(cap_id))
  response = e2e_pf.get_policies_by_sla(caps_list)
  policies_list = response[0]
  
  # prepares the policies info to store it in the slice instance object
  mapped_policies = []
  for pol_item in policies_list:
    pol = {}
    mon_pol = {}
    pol["ssla-capability"] = pol_item["ssla-capability"]
    pol["policy-id"] = pol_item["id"]
    pol["name"] = pol_item["name"]
    mapped_policies.append(pol)
    mon_pol["ssla-capability"] = pol_item["ssla-capability"]
    mon_pol["policy-id"] = pol_item["monitoring-id"]
    mon_pol["name"] = pol_item["monitoring-name"]
    mapped_policies.append(mon_pol)
  ssla_info["mapped-policies"] = mapped_policies
  sec_nsi["security-sla"] = ssla_info
  config_sys.logger.info('NSI-MNGR: NSI DATA OBJECT READY:' + str(sec_nsi))
 
  # saves NSI into the Database
  response = secnsi_db_mngr.add_sec_nsi(sec_nsi)
  if response[1] != 200:
    config_sys.logger.error(response[0])

  # TODO: Prepares MSPL (XML format) data request to deploy
  slice2mspl.generateMSPL(sec_nsi)

  # TODO: Validates policy is applied = Sec_NSI is deployed
  config_sys.logger.info(response[0])

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