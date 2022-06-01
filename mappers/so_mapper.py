#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
from xml.dom import minidom 

from config_files import config_system as config_sys

CONTENT_HEADER_XML = {'Content-Type':'application/xml'}
CONTENT_HEADER_JSON = {'Content-Type':'application/json'}


def request_deployment(xml_data):
    so_ip = os.environ.get("SO_IP")
    so_port = os.environ.get("SO_PORT")
    url = "http://"+ str(so_ip) + ":" + str(so_port) +"/e2emeservice"
    header = {'Content-Type': 'application/xml; charset=UTF-8', 'Cache-Control': 'no-cache', 'Accept': 'application/json',}
    #data = ElementTree.tostring(elem, encoding='UTF-8')
    
    response = requests.post(url, data=xml_data, headers=header)
    config_sys.logger.info('NSI-MNGR: E2E_SO RESPONSE:' + str(response))
    
    if response.status_code != 200:
        config_sys.logger.info('NSI-MNGR: E2E_SO STATUS:' + str(response.status_code))
        config_sys.logger.info('NSI-MNGR: E2E_SO RESPONSE_TEXT:' + str(response.text))
        return [], response.status_code
    else:
        #TODO: process the response.text from the E2E SO
        config_sys.logger.info('NSI-MNGR: E2E_SO RESPONSE:' + str(response.text))
        return response.text, response.status_code