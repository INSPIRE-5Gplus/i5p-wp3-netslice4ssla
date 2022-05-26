#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
from xml.dom import minidom 

from config_files import config_system as config_sys

CONTENT_HEADER = {'Content-Type':'application/xml'}

# SSLA MANAGER EMULATED

## Security Service Level Agreement Manager API Options ##
# Create SSLA (POST /sla) --> # NOTE: NOT NECESSARY
# Remove SSLA (DELETE /sla/{slaId}) --> # NOTE: NOT NECESSARY
# Update SSLA (PUT /sla/{slaId}) --> # NOTE: NOT NECESSARY

# Retrieve SSLA List (GET /sla)
def get_ssla_list():
    ssla_mngr_ip = os.environ.get("SSLA_IP")
    ssla_mngr_port = os.environ.get("SSLA_PORT")
    url = "http://"+ str(ssla_mngr_ip) + ":" + str(ssla_mngr_port) +"/sla"
    response = requests.get(url, headers=CONTENT_HEADER)
    if response.status_code != 200:
        return [], response.status_code
    else:
        #TODO: process the response.text from XML to JSON
        ssla_list_json = []

    return ssla_list_json, 201

# Retrieve SSLA (GET /sla/{slaId})
def get_ssla(ssla_id):
    config_sys.logger.info('SSLA-MNGR: Retrieving SSLA information.')
    """
        ssla_mngr_ip = os.environ.get("SSLA_IP")
        ssla_mngr_port = os.environ.get("SSLA_PORT")
        url = "http://"+ str(ssla_mngr_ip) + ":" + str(ssla_mngr_port) +"/sla/"+str(ssla_id)
        response = requests.get(url, headers=CONTENT_HEADER)
        if response.status_code != 200:
            return [], response.status_code
        else:
            #TODO: process the response.text from XML to JSON
            ssla_json = []
        return ssla_json, 201
    """
    config_sys.logger.info('SSLA: A')
    if ssla_id == "Secure 5G Mobile Communications":
        config_sys.logger.info('SSLA: B')
        ssla_doc = minidom.parse("./data_objects/specs-SLATemplate-5G-Mobile-Comms.xml")
        code = 201
    elif ssla_id == "Secure 5G IoT Communications":
        config_sys.logger.info('SSLA: C')
        ssla_doc = minidom.parse("./data_objects/specs-SLATemplate-5G-IoT-Comms.xml")
        code = 201
    else:
        # TODO: ERROR MANAGEMENT
        ssla_doc = ""
        code = 404
    config_sys.logger.info('SSLA: D')
    return ssla_doc, code

