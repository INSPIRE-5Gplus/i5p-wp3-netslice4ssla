#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

CONTENT_HEADER = {'Content-Type':'application/xml'}

## Security Service Level Agreement Manager API Options ##
# Create SSLA (POST /sla) --> # NOTE: NOT NECESSARY
# Remove SSLA (DELETE /sla/{slaId}) --> # NOTE: NOT NECESSARY
# Update SSLA (PUT /sla/{slaId}) --> # NOTE: NOT NECESSARY

# Retrieve SSLA List (GET /sla)
def get_ssla_list():
    ssla_list = []

    return ssla_list, 201
""" CODE
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
"""

# Retrieve SSLA (GET /sla/{slaId})
def get_ssla(ssla_id):
    ssla = ssla_id

    return ssla, 201
""" CODE
    #ssla_mngr_ip = os.environ.get("SSLA_IP")
    #ssla_mngr_port = os.environ.get("SSLA_PORT")
    #url = "http://"+ str(ssla_mngr_ip) + ":" + str(ssla_mngr_port) +"/sla/"+str(ssla_id)
    #response = requests.get(url, headers=CONTENT_HEADER)
    if response.status_code != 200:
        return [], response.status_code
    else:
        #TODO: process the response.text from XML to JSON
        ssla_json = []

    return ssla_json, 201
"""