#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

from config_files import config_system as LOG

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
# NST DATABASE
NST_LIST = []  #NOTE: More complex DBs are possible, maybe to keep the data in a file?

# add element in db
def add_nst(nst_element):
    LOG.logger.info("Element added into the NST DB.")
    NST_LIST.append(nst_element)
    return {'msg':'NST element added and saved.'}, 200

# update element in db
def update_nst(nst_id, nst_element):
    LOG.logger.info("Updating NST element in DB.")
    for nst_item in NST_LIST:
        if nst_item['id'] == nst_id:
            nst_item = nst_element
            return {'msg':'NST element updated and saved.'}, 200
    
    return {'msg':'NST element not found.'}, 404

# remove element in db
def remove_nst(nst_id):
    LOG.logger.info("Removing NST element from the DB.")
    for nst_item in NST_LIST:
        if nst_item['id'] == nst_id:
            NST_LIST.remove(nst_item)
            return {'msg':'NST element removed.'}, 200

    return {'msg':'NST element not found.'}, 404       

# retrieve all elements in db
def get_nsts():
    LOG.logger.info("Retrieving NST elements from DB.")
    return NST_LIST, 200

# retrieve element in db
def get_nst(nst_id):
    LOG.logger.info("Retrieving a NST element from the DB.")
    for nst_item in NST_LIST:
        if nst_item['id'] == nst_id:
            return nst_item, 200

    return {'msg':'NST element not found.'}, 404