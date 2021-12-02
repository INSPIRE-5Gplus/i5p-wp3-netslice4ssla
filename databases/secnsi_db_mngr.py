#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
from threading import Lock

from config_files import config_system as LOG

# This script has the actions to manage the databe of the secured netslices objects.
# All the information is stored in a .txt file to keep their status in case the service fales.
# Withi the .txt, each line is a secure netslie object and it follows this structure:
# uuid - "string with the secured netslice in json format"
"""
EXAMPLE OF SECURE E2E NSI
#TODO: to improve
{
    "uuid": "uuid4",
    "status": "DEPLOYING, DEPLOYED, TERMINATING, TERMINATED, ERROR"
    "slice-subnets":[
        {
            "slice-subnet-id": "uuid4",
            "nst-ref": "uuid4",
            "ssla-ref": uuid4,
            "status": "DEPLOYING, DEPLOYED, TERMINATING, TERMINATED, ERROR",
            "slice-mngr-id": "uuid4"
        }
    ]
}
"""

# mutex used to ensure a single access to the DB
mutex_secnsi_db = Lock()

# add element in db
def add_sec_nsi(sec_nsi_json):
    LOG.logger.info("Element added into the SEC_NSI DB.")
    try:
        mutex_secnsi_db.acquire()
        # TODO: verify if element (uuid) exists before adding.
        # adds the new element into the file (creates file if it doesn't exist
        sec_nsi_element = str(sec_nsi_json["uuid"]) + " - " + json.dumps(sec_nsi_json) + "\n"
        with open('./databases/sec_nsi_list.txt', 'a') as f:
            f.write(sec_nsi_element)
        msg = 'SEC_NSI element added and saved.'
        code = 200
    finally:
        mutex_secnsi_db.release()

    return {'msg':msg}, code

# update element in db
def update_sec_nsi(sec_nsi_id, sec_nsi_json):
    LOG.logger.info("Updating SEC_NSI element in DB.")
    try:
        mutex_secnsi_db.acquire()
        line_found = False
        index_found = 0
        with open('./databases/sec_nsi_list.txt', 'r') as sec_nsi_file:
            lines = sec_nsi_file.readlines()
        for idx, line in enumerate(lines):
            line = line[:-1]
            x = line.split(" - ")
            if x[0] == sec_nsi_id:
                line_found = True
                index_found = idx
                break
        line = sec_nsi_id + " - " + json.dumps(sec_nsi_json) + "\n"
        lines[index_found] = line
        
        if line_found == False:
            msg = 'SEC_NSI element not found.'
            code = 404
        else:
            # saves updated data in the file
            with open('./databases/sec_nsi_list.txt', 'w') as new_sec_nsi_file:
                for line in lines:
                    new_sec_nsi_file.write(line)
            msg = 'SEC_NSI element updated and saved.'
            code = 200
    finally:
        mutex_secnsi_db.release()
    
    return {'msg':msg}, code

# remove element in db
def remove_sec_nsi(sec_nsi_id):
    LOG.logger.info("Removing SEC_NSI element from the DB.")
    try:
        mutex_secnsi_db.acquire()
        line_found = False
        index_found = 0
        with open('./databases/sec_nsi_list.txt', 'r') as sec_nsi_file:
            lines = sec_nsi_file.readlines()
        for idx, line in enumerate(lines):
            x = line.split(" - ")
            if x[0] == sec_nsi_id:
                line_found = True
                index_found = idx
                break
        
        #remove the specified line
        del lines[index_found]
        
        if line_found == False:
            msg = 'SEC_NSI element not found.'
            code = 404
        else:
            # saves updated data in the file
            with open('./databases/sec_nsi_list.txt', 'w') as new_sec_nsi_file:
                for line in lines:
                    new_sec_nsi_file.write(line)
            msg = 'SEC_NSI element removed.'
            code = 200  
    finally:
        mutex_secnsi_db.release()
    
    return {'msg':msg}, code    

# retrieve all elements in db
def get_sec_nsis():
    LOG.logger.info("Retrieving SEC_NSI elements from DB.")
    sec_nsi_list = []
    with open('./databases/sec_nsi_list.txt', 'r') as sec_nsi_file:
        lines = sec_nsi_file.readlines()
    for line in lines:
        x = line.split(" - ")
        nsi_string = x[1].replace("\n", " ")
        sec_nsi_list.append(json.loads(nsi_string))
    
    print(sec_nsi_list)
    if sec_nsi_list == []:
        msg = 'No SEC_NSI element in the DB'
        code = 404
    else:
        msg = sec_nsi_list
        code = 200
    
    return {'msg':msg}, code

# retrieve element in db
def get_sec_nsi(sec_nsi_id):
    LOG.logger.info("Retrieveing a SEC_NSI element from the DB.")
    sec_nsi_element = ""
    with open('./databases/sec_nsi_list.txt', 'r') as sec_nsi_file:
        lines = sec_nsi_file.readlines()
    for line in lines:
        x = line.split(" - ")
        if x[0] == sec_nsi_id:
            sec_nsi_element = json.loads(x[1])
            break

    if sec_nsi_element == "":
        msg = 'SEC_NSI element not found.'
        code = 404
    else:
        msg = sec_nsi_element
        code = 200
    
    return {"msg": msg}, code