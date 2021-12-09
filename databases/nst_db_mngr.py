#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
from threading import Lock

from config_files import config_system as config_sys

"""
Example of E2E NST
{
    "name": "NST_name",
    "version": 0.2,
    "author": "inspire5gplus_cttc",
    "vendor": "inspire5gplus",
    "SNSSAI_identifier": {
        "slice-service-type": "eMBB_URLLC_mMTC",
        "slice-differentiator": "uuid"
    },
    "usageState": "IN_USE||NOT_IN_USE",
    "slice-subnets": [
        {
            "id": "uuid",
            "ref": "uuid",
            "name": "nst_name",
            "version": 0.2,
            "vendor": "inspire5gplus",
            "shared": "True||False",
            "sla-name": "sla_name",
            "sla-ref": "uuid"
        }
    ],
    "slice_vld": [
        {
            "id": "uuid",
            "name": "vld_name",
            "mgmt-network": "True||False",
            "type": "E-LINE||E-TREE||E-LAN",
            "nsd-connection-point-ref": [
            {
                "subnet-ref": "nsd_name_ref",
                "nsd-cp-ref": "nsd_cp_ref",
                "ip-address": "10.0.37.13/24"
            }
        }
    ]
}
"""
# mutex used to ensure a single access to the DB
mutex_nts_db = Lock()

# add element in db
def add_nst(nst_json):
    config_sys.logger.info("Element added into the NST DB.")
    try:
        mutex_nts_db.acquire()
        # TODO: verify if element (uuid) exists before adding.
        # adds the new element into the file (creates file if it doesn't exist
        nst_element = str(nst_json["uuid"]) + " - " + json.dumps(nst_json) + "\n"
        with open('./databases/nst_list.txt', 'a') as nst_file:
            nst_file.write(nst_element)
        msg = 'E2E NST element added and saved.'
        code = 200
    finally:
        mutex_nts_db.release()

    return {'msg':msg}, code

# update element in db
def update_nst(nst_id, nst_json):
    config_sys.logger.info("Updating NST element in DB.")
    try:
        mutex_nts_db.acquire()
        line_found = False
        index_found = 0
        with open('./databases/nst_list.txt', 'r') as nst_file:
            lines = nst_file.readlines()
        for idx, line in enumerate(lines):
            line = line[:-1]
            x = line.split(" - ")
            if x[0] == nst_id:
                line_found = True
                index_found = idx
                break
        line = nst_id + " - " + json.dumps(nst_json) + "\n"
        lines[index_found] = line
        
        if line_found == False:
            msg = 'NST element not found.'
            code = 404
        else:
            # saves updated data in the file
            with open('./databases/nst_list.txt', 'w') as new_nst_file:
                for line in lines:
                    new_nst_file.write(line)
            msg = 'NST element updated and saved.'
            code = 200
    finally:
        mutex_nts_db.release()
    
    return {'msg':msg}, code

# remove element in db
def remove_nst(nst_id):
    config_sys.logger.info("Removing NST element from the DB.")
    try:
        mutex_nts_db.acquire()
        line_found = False
        index_found = 0
        with open('./databases/nst_list.txt', 'r') as nst_file:
            lines = nst_file.readlines()
        for idx, line in enumerate(lines):
            x = line.split(" - ")
            if x[0] == nst_id:
                line_found = True
                index_found = idx
                break
        
        #remove the specified line
        del lines[index_found]
        
        if line_found == False:
            msg = 'NST element not found.'
            code = 404
        else:
            # saves updated data in the file
            with open('./databases/nst_list.txt', 'w') as new_nst_file:
                for line in lines:
                    new_nst_file.write(line)
            msg = 'NST element removed.'
            code = 200  
    finally:
        mutex_nts_db.release()
    
    return {'msg':msg}, code    

# retrieve all elements in db
def get_nsts():
    config_sys.logger.info("Retrieving NST elements from DB.")
    nst_list = []
    with open('./databases/nst_list.txt', 'r') as nst_file:
        lines = nst_file.readlines()
    for line in lines:
        x = line.split(" - ")
        nst_string = x[1].replace("\n", " ")
        nst_list.append(json.loads(nst_string))
    
    if nst_list == []:
        msg = 'No NST element in the DB'
        code = 404
    else:
        msg = nst_list
        code = 200
    
    return {'msg':msg}, code

# retrieve element in db
def get_nst(nst_id):
    config_sys.logger.info("Retrieving a NST element from the DB.")
    nst_element = ""
    with open('./databases/nst_list.txt', 'r') as nst_file:
        lines = nst_file.readlines()
    for line in lines:
        x = line.split(" - ")
        if x[0] == nst_id:
            nst_element = json.loads(x[1])
            break

    if nst_element == "":
        msg = 'NST element not found.'
        code = 404
    else:
        msg = nst_element
        code = 200
    
    return {"msg": msg}, code