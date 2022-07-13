#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
from xml.dom import minidom
import xml.etree.ElementTree as ET

from config_files import config_system as config_sys

CONTENT_HEADER_xml = {'Accept':'application/xml'}
CONTENT_HEADER_json = {'Accept':'application/json'}

# SSLA MANAGER EMULATED

## Security Service Level Agreement Manager API Options ##
# Create SSLA (POST /ssla) --> # NOTE: NOT NECESSARY
# Remove SSLA (DELETE /sla/{slaId}) --> # NOTE: NOT NECESSARY
# Update SSLA (PUT /sla/{slaId}) --> # NOTE: NOT NECESSARY

# Retrieve SSLA List (GET /sla)
def get_ssla_list():
    config_sys.logger.info('SSLA-MNGR: Retrieving SSLA element IDs.')
    ssla_mngr_ip = os.environ.get("SSLA_IP")
    ssla_mngr_port = os.environ.get("SSLA_PORT")
    url = "http://"+ str(ssla_mngr_ip) + ":" + str(ssla_mngr_port) +"sla"
    config_sys.logger.info('SSLA-MNGR: url: ' + url)
    response = requests.get(url, headers=CONTENT_HEADER_json)
    if response.status_code != 200:
        config_sys.logger.info('SSLA-MNGR: response: ' + str(response))
        return [], response.status_code
    else:
        ssla_list_json = ET.ElementTree(ET.fromstring(response[0]))

    return ssla_list_json, 201

# Retrieve SSLA (GET /sla/{slaId})
def get_ssla(ssla_id):
    config_sys.logger.info('SSLA-MNGR: Retrieving SSLA information.')
    """ #NOTE: REAL DEMO uncomment & comment below
    ssla_mngr_ip = os.environ.get("SSLA_IP")
    ssla_mngr_port = os.environ.get("SSLA_PORT")
    url = "http://" + str(ssla_mngr_ip) + ":" + str(ssla_mngr_port) + "/sla/" + str(ssla_id)
    config_sys.logger.info('SSLA-MNGR: url - ' + url)
    #config_sys.logger.info('SSLA-MNGR: CONTENT_HEADER_xml - ' + str(CONTENT_HEADER_xml))
    response = requests.get(url, headers=CONTENT_HEADER_xml)
    config_sys.logger.info('SSLA-MNGR: response.status_code - ' + str(response.status_code))
    #config_sys.logger.info('SSLA-MNGR: response.text - ' + str(response.text))
    if response.status_code != 200:
        return [], response.status_code
        
    return response.text, 201
    """
    config_sys.logger.info('SSLA-MNGR: LOCAL STORED FILE SSLA')
    if ssla_id == "5G_SERVICE_SSLA":
        ssla_doc = minidom.parse("./data_objects/SSLA1_v2.xml")
        code = 201
    elif ssla_id == "5G_IOT_BROKER_SSLA":
        ssla_doc = minidom.parse("./data_objects/SSLA2_v3.xml")
        code = 201
    else:
        # TODO: ERROR MANAGEMENT
        ssla_doc = ""
        code = 404
    return ssla_doc, code
    
    

