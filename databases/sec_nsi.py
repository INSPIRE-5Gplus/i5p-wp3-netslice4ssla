#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

from config_files import config_system as config_sys


# database for Network Slice Instances
sec_nsi_db = []
""" sec_nsi data object
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

# add sec_nsi in db
def add_sec_nsi(sec_nsi_element):
    config_sys.logger.info("SecNSI added into the DB.")
    sec_nsi_db.append(sec_nsi_element)
    return {'msg':'SecNSI with uuid: '+ str(sec_nsi_element["uuid"]) +' - SAVED.'}, 200

# update sec_nsi in db
def update_sec_nsi(sec_nsi_element):
    config_sys.logger.info('Updating SecNSI with uuid: '+ str(sec_nsi_element["uuid"]))
    for sec_nsi_item in sec_nsi_db:
        if sec_nsi_item["uuid"] == sec_nsi_element["uuid"]:
            sec_nsi_item = sec_nsi_element
            return {'msg':'SecNSI updated and saved.'}, 200
    return {'msg':'SecNSI not found.'}, 404

# remove sec_nsi in db
def remove_sec_nsi(sec_nsi_id):
    config_sys.logger.info('Removed SecNSI with uuid: '+ str(sec_nsi_id))
    for sec_nsi_item in sec_nsi_db:
        if sec_nsi_item["uuid"] == sec_nsi_id:
            if sec_nsi_item["status"] == "TERMINATED":
                sec_nsi_db.remove(sec_nsi_item)
                return {'msg':'SecNSI removed from DB.'}, 200
            else:
                return {'msg':'SecNSI cannot be removed as it is not terminated.'}, 406
    return {'msg':'SecNSI not found.'}, 404

# retrieve all sec_nsi in db
def get_all_sec_nsi():
    config_sys.logger.info('Retrieving all SecNSI elements from DB.')
    return sec_nsi_db, 200

# retrieve sec_nsi in db
def get_sec_nsi(sec_nsi_id):
    config_sys.logger.info('Retrieveing SecNSI with uuid: '+ str(sec_nsi_id))
    for sec_nsi_item in sec_nsi_db:
        if sec_nsi_item["uuid"] == sec_nsi_id:
            return sec_nsi_item, 200
    return {'msg':'SecNSI not found.'}, 404