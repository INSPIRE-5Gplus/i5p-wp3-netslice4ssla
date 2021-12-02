#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
from threading import Lock

from config_files import config_system as LOG

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

# SEC NSI DATABASE
SEC_NSI_LIST = []  #NOTE: More complex DBs are possible, maybe to keep the data in a file?
# sec_nsi_list.txt structure: uuid - string (json element)

# add element in db
def add_sec_nsi(sec_nsi_json):
    LOG.logger.info("Element added into the SEC_NSI DB.")
    #SEC_NSI_LIST.append(sec_nsi_json)
    try:
        mutex_secnsi_db.acquire()
        # TODO: verify if element (uuid) exists before adding.
        # adds the new element into the file (creates file if it doesn't exist
        sec_nsi_element = str(sec_nsi_json["uuid"]) + " - " + json.dumps(sec_nsi_json)
        with open('sec_nsi_list.txt', 'a') as f:
            f.write(sec_nsi_element)
        msg = 'SEC_NSI element added and saved.'
        code = 200
    finally:
        mutex_secnsi_db.release()

    return {'msg':msg}, code

# update element in db
def update_sec_nsi(sec_nsi_id, sec_nsi_json):
    LOG.logger.info("Updating SEC_NSI element in DB.")
    #for sec_nsi_item in SEC_NSI_LIST:
    #    if sec_nsi_item['id'] == sec_nsi_id:
    #        sec_nsi_item = json.dumps(sec_nsi_json)
    #        return {'msg':'SEC_NSI element updated and saved.'}, 200
    try:
        mutex_secnsi_db.acquire()
        line_found = False
        with open('sec_nsi_list.txt', 'r') as sec_nsi_file:
            lines = sec_nsi_file.readlines()
        for line in lines:
            x = line.split(" - ")
            if x[0] == sec_nsi_id:
                # update specific element
                x[1] = json.dumps(sec_nsi_json)
                line_found = True
                break
        
        if line_found == False:
            msg = 'SEC_NSI element not found.'
            code = 404
        else:
            # saves updated data in the file
            with open('sec_nsi_list.txt', 'w') as new_sec_nsi_file:
                new_sec_nsi_file.writelines(lines) 

            msg = 'SEC_NSI element updated and saved.'
            code = 200
    finally:
        mutex_secnsi_db.release()
    
    return {'msg':msg}, code

# remove element in db
def remove_sec_nsi(sec_nsi_id):
    LOG.logger.info("Removing SEC_NSI element from the DB.")
    #for sec_nsi_item in SEC_NSI_LIST:
    #    if sec_nsi_item['id'] == sec_nsi_id:
    #        SEC_NSI_LIST.remove(sec_nsi_item)
    #        return {'msg':'SEC_NSI element removed.'}, 200
    #return {'msg':'SEC_NSI element not found.'}, 404 
    try:
        mutex_secnsi_db.acquire()
        line_found = False
        with open('sec_nsi_list.txt', 'r') as sec_nsi_file:
            lines = sec_nsi_file.readlines()
            for idx, line in enumerate(lines):
                x = line.split(" - ")
                if x[0] == sec_nsi_id:
                    del lines[idx]
                    line_found = True
                    break
        
        if line_found == False:
            msg = 'SEC_NSI element not found.'
            code = 404
        else:
            msg = 'SEC_NSI element removed.'
            code = 200    
    finally:
        mutex_secnsi_db.release()
    
    return {'msg':msg}, code    

# retrieve all elements in db
def get_sec_nsis():
    LOG.logger.info("Retrieving SEC_NSI elements from DB.")
    #return SEC_NSI_LIST, 200

    sec_nsi_list = []
    with open('sec_nsi_list.txt', 'r') as sec_nsi_file:
        lines = sec_nsi_file.readlines()
    for line in lines:
        x = line.split(" - ")
        sec_nsi_list.append(json.loads(x[1]))
    
    if sec_nsi_list == []:
        return {'msg':'No SEC_NSI element in the DB'}, 404
    else:
        return sec_nsi_list, 200

# retrieve element in db
def get_sec_nsi(sec_nsi_id):
    LOG.logger.info("Retrieveing a SEC_NSI element from the DB.")
    #for sec_nsi_item in SEC_NSI_LIST:
    #    if sec_nsi_item['id'] == sec_nsi_id:
    #        return sec_nsi_item, 200

    sec_nsi_element = ""
    with open('sec_nsi_list.txt', 'r') as sec_nsi_file:
        lines = sec_nsi_file.readlines()
    for line in lines:
        x = line.split(" - ")
        if x[0] == sec_nsi_id:
            sec_nsi_element = json.loads(x[1])
            break

    if sec_nsi_element == "":
        return {'msg':'SEC_NSI element not found.'}, 404
    else:
        return sec_nsi_element, 200