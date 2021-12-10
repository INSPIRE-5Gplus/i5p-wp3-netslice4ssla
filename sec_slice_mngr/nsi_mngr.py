#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

from config_files import config_system as config_sys
from databases import nst_db_mngr
from databases import secnsi_db_mngr
from sec_slice_mngr import slice2mspl


def deploy_sec_nsi(request_json):
    print("Deploying Secured NSI...")

    # TODO: Prepares Sec_NSI data object structure
    sec_nsi = {}
    sec_nsi["uuid"] = str(uuid.uuid4())
    sec_nsi["name"] = request_json["name"]
    response = nst_db_mngr.get_nst(request_json["nst-ref"])
    nst_ref_json = response[0]["msg"]
    nst_ref = {}
    nst_ref["uuid"] = nst_ref_json["uuid"]
    nst_ref["name"] = nst_ref_json["name"]
    nst_ref["version"] = nst_ref_json["version"]
    sec_nsi["nst-ref"] = nst_ref
    # TODO: follow object creation...

    response = secnsi_db_mngr.add_sec_nsi(sec_nsi)
    if response[1] != 200:
        config_sys.logger.error(response[0])

    # TODO: Gets SSLA information & and maps it inot the Sec_NSI
    # TODO: Prepares MSPL (XML format) data request to deploy
        # calls functions in slice2mspl
    # TODO: Validates policy is applied = Sec_NSI is deployed

    config_sys.logger.info(response[0])

def terminate_sec_nsi(sec_nsi_uuid):
    config_sys.logger.info('GET SEC NSI')
    # TODO: Gets Sec_NSI data object structure
    response = secnsi_db_mngr.get_sec_nsi(sec_nsi_uuid)
    if response[1] == 200:
        sec_nsi_json = response[0]["msg"]
    else:
        return response[0], response[1]

    # TODO: Prepares MSPL (XML format) data request to terminate

    # TODO: Validates policy is applied = Sec_NSI is terminated
    sec_nsi_json["status"] = "TERMINATED"
    response = secnsi_db_mngr.update_sec_nsi(sec_nsi_json["uuid"], sec_nsi_json)

def remove_sec_nsi(sec_nsi_uuid):
    # Remove Sec NSI from DB
    response = secnsi_db_mngr.remove_sec_nsi(sec_nsi_uuid)
    return response[0], response[1]

def get_sec_nsis():
    # Retrieve all Sec NSI data objects from DB
    response = secnsi_db_mngr.get_sec_nsis()
    return response[0], response[1]

def get_sec_nsi(sec_nsi_uuid):
    # Retrieve specific Sec NSI data object from DB
    response = secnsi_db_mngr.get_sec_nsi(sec_nsi_uuid)
    return response[0], response[1]