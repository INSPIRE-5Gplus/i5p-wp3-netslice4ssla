#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

from config_files import config_system as config_sys
from databases import sec_nsi as secnsi_db
from sec_slice_mngr import slice2mspl


def deploy_sec_nsi(request_json):
    print("Deploying Secured NSI...")

    # TODO: Prepares Sec_NSI data object structure
    sec_nsi = {}
    sec_nsi["uuid"] = str(uuid.uuid4())
    sec_nsi["name"] = request_json["name"]
    # TODO: follow object creation...

    response = secnsi_db.add_sec_nsi(sec_nsi)
    if response[1] != 200:
        config_sys.logger.error(response[0])

    # TODO: Gets SSLA information & and maps it inot the Sec_NSI
    # TODO: Prepares MSPL (XML format) data request to deploy
        # calls functions in slice2mspl
    #TODO:  Validates policy is applied = Sec_NSI is deployed

    config_sys.logger.info(response[0])

def terminate_sec_nsi(request_json):
    print("Terminating Secured NSI...")
    # TODO: Gets Sec_NSI data object structure

    # TODO: Prepares MSPL (XML format) data request to terminate

    # TODO: Validates policy is applied = Sec_NSI is terminated
    pass

def remove_sec_nsi(sec_nsi_uuid):
    # Remove Sec NSI from DB
    response = secnsi_db.remove_sec_nsi(sec_nsi_uuid)
    return response[0], response[1]

def get_sec_nsis():
    # Retrieve all Sec NSI data objects from DB
    response = secnsi_db.get_all_sec_nsi()
    return response[0], response[1]

def get_sec_nsi(sec_nsi_uuid):
    # Retrieve specific Sec NSI data object from DB
    response = secnsi_db.get_sec_nsi(sec_nsi_uuid)
    return response[0], response[1]