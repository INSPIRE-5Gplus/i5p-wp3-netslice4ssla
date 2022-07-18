#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
from xml.dom import minidom
import xml.etree.ElementTree as ET

from config_files import config_system as config_sys

CONTENT_HEADER_XML = {'Content-Type':'application/xml'}
CONTENT_HEADER_JSON = {'Content-Type':'application/json'}


def request_deployment(xml_data):
    so_ip = os.environ.get("SO_IP")
    so_port = os.environ.get("SO_PORT")
    url = "http://"+ str(so_ip) + ":" + str(so_port) +"/e2emeservice"
    config_sys.logger.info('E2ESO_MAPPER: E2E_SO url:' + str(url))
    header = {'Content-Type': 'application/xml; charset=UTF-8', 'Cache-Control': 'no-cache', 'Accept': 'application/json',}

    ssla_doc = "./MSPL_test.xml"
    with open(ssla_doc) as xml_data:
        #root= xml_data.getroot()
        #data = ET.tostring(root, encoding='UTF-8', method='xml')
        #config_sys.logger.info('E2ESO_MAPPER: data: ' + str(data))
        config_sys.logger.info('E2ESO_MAPPER: xml_data type:' + str(type(xml_data)))
        response = requests.post(url, data=xml_data, headers=header, timeout=600)
        config_sys.logger.info('E2ESO_MAPPER: E2E_SO RESPONSE:' + str(response))
    
    if response.status_code != 200:
        config_sys.logger.info('E2ESO_MAPPER: E2E_SO STATUS:' + str(response.status_code))
        config_sys.logger.info('E2ESO_MAPPER: E2E_SO RESPONSE_TEXT:' + str(response.text))
        return [], response.status_code
    else:
        #TODO: process the response.text from the E2E SO
        config_sys.logger.info('E2ESO_MAPPER: E2E_SO RESPONSE:' + str(response.text))
        return response.text, response.status_code