#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
from xml.dom import minidom
import xml.etree.ElementTree as ET

from config_files import config_system as config_sys

CONTENT_HEADER = {'Content-Type':'application/xml'}

# SSLA MANAGER EMULATED

## Security Service Level Agreement Manager API Options ##
# Create SSLA (POST /services/sla) --> # NOTE: NOT NECESSARY
# Remove SSLA (DELETE /services/sla/{slaId}) --> # NOTE: NOT NECESSARY
# Update SSLA (PUT /services/sla/{slaId}) --> # NOTE: NOT NECESSARY

# Retrieve SSLA List (GET /sla)
def get_ssla_list():
    config_sys.logger.info('SSLA-MNGR: Retrieving SSLA element IDs.')
    ssla_mngr_ip = os.environ.get("SSLA_IP")
    ssla_mngr_port = os.environ.get("SSLA_PORT")
    url = "http://"+ str(ssla_mngr_ip) + ":" + str(ssla_mngr_port) +"/services/sla"
    config_sys.logger.info('SSLA-MNGR: url: ' + url)
    response = requests.get(url, headers=CONTENT_HEADER)
    if response.status_code != 200:
        config_sys.logger.info('SSLA-MNGR: response: ' + str(response))
        return [], response.status_code
    else:
        ssla_list_json = ET.ElementTree(ET.fromstring(response[0]))

    return ssla_list_json, 201

# Retrieve SSLA (GET /sla/{slaId})
def get_ssla(ssla_id):
    config_sys.logger.info('SSLA-MNGR: Retrieving SSLA information.')
    
    ssla_mngr_ip = os.environ.get("SSLA_IP")
    ssla_mngr_port = os.environ.get("SSLA_PORT")
    url = "http://" + str(ssla_mngr_ip) + ":" + str(ssla_mngr_port) + "/services/sla/" + str(ssla_id)
    response = requests.get(url, headers=CONTENT_HEADER)
    config_sys.logger.info('SSLA-MNGR: response - ' + str(response))
    if response.status_code != 200:
        return [], response.status_code
    else:
        ssla_xml = ET.ElementTree(ET.fromstring(response[0]))
    return ssla_xml, 201
    """
    config_sys.logger.info('SSLA-MNGR: LOCAL STORED FILE SSLA')
    if ssla_id == "Secure 5G Mobile Communications":
        ssla_doc = minidom.parse("./data_objects/SSLA1_v2.xml")
        code = 201
    elif ssla_id == "Secure 5G IoT Communications":
        ssla_doc = minidom.parse("./data_objects/SSLA2_v3.xml")
        code = 201
    else:
        # TODO: ERROR MANAGEMENT
        ssla_doc = ""
        code = 404
    return ssla_doc, code
    """

