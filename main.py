#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, uuid, requests, uuid
from flask.wrappers import Response
from flask import Flask, request, jsonify
from configparser import ConfigParser
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Lock

from config_files import config_system as config_sys
from mappers import ssla_mngr_mapper as ssla_mngr
from sec_slice_mngr import nsi_mngr
from databases import nst_db_mngr


# Define inner applications
app = Flask(__name__)

########################################### Test API #################################################
# PING function to validate if the slice-docker is active
@app.route('/sec_nsi/pings', methods=['GET'])
def getPings():
  ping_response  = {'code creation date': '2021-10-14 14:15:00 UTC', 'current_time': str(datetime.datetime.now().isoformat())}
  return jsonify(ping_response), 200

########################################### SSLA API #################################################
# gets all the SLAs
@app.route('/ssla', methods=['GET'])
def get_all_ssla():
  response = ssla_mngr.get_ssla_list()
  if response[1] == 201 and response[0] != []:
    return response[0], 201
  else:
    response = {}
    response["error_msg"] = "There are no SSLAs available."
    return response, 404
    
# gets a specific SSLA
@app.route('/ssla/<ssla_uuid>', methods=['GET'])
def get_ssla(ssla_uuid):
  response = ssla_mngr.get_ssla(ssla_uuid)
  if response[1] == 201 and response[0] != []:
    return response[0], 201
  else:
    response = {}
    response["error_msg"] = "The selected SSLA with UUID: " + str(ssla_uuid) + " does not exist."
    return response, 404

########################################### E2E NST API #################################################
# ADDS a new NST
@app.route('/nst', methods=['POST'])
def new_nst():
  config_sys.logger.info('Request to add an E2E NST.')
  nst_json = request.json
  nst_json["uuid"] = str(uuid.uuid4())
  response = nst_db_mngr.add_nst(nst_json)
  return response[0], response[1]

# GETS all the NSTs
@app.route('/nst', methods=['GET'])
def get_all_nst():
  response = nst_db_mngr.get_nsts()
  return response[0], response[1]

# GETS a specific NST
@app.route('/nst/<nst_uuid>', methods=['GET'])
def get_nst(nst_uuid):
  response = nst_db_mngr.get_nst(nst_uuid)
  return response[0], response[1]

# UPDATES NST
# NOTE: function not implemented, if there's a new NST. Remove the old, and add the new.
@app.route('/nst/<nst_uuid>', methods=['PUT'])
def nst_update(nst_uuid):
  #response = nst_db_mngr.update_nst(nst_uuid, request.json)
  #return response[0], response[1]
  pass

# DELETES NST
@app.route('/nst/<nst_uuid>', methods=['DELETE'])
def nst_remove(nst_uuid):
  response = nst_db_mngr.remove_nst(nst_uuid)
  return response[0], response[1]

########################################### NSI API #################################################
# Triggers a Sec_NSI deployment
@app.route('/sec_nsi/test', methods=['POST'])
def deploy_sec_nsi_test():
  config_sys.logger.info('MAIN: Request to deploy Sec NSI received.')
  response = nsi_mngr.deploy_sec_nsi_test()
  config_sys.logger.info('MAIN: Response from E2E SO')

  return response[0], response[1]

# Triggers a Sec_NSI deployment
@app.route('/sec_nsi', methods=['POST'])
def deploy_sec_nsi():
  config_sys.logger.info('MAIN: Request to deploy Sec NSI received.')
  incoming_request =  request.json
  response = ssla_mngr.get_ssla(incoming_request['ssla_id'])    # TODO: integrate with the real SSLA MNGR
  request_response = {}
  if response[1] == 201:
    config_sys.executor.submit(nsi_mngr.deploy_sec_nsi(incoming_request, response[0]))
    request_response['log'] = "Request accepted, setting up the E2E Network Slice."
    code = 200
  else:
    request_response['log'] = "Request NOT ACCEPTED, there is NO SSLA with this ID."
    code = 404
  return request_response, code

# GETS all the Sec_NSI
@app.route('/sec_nsi', methods=['GET'])
def get_all_sec_nsi():
  config_sys.logger.info('Request to get all Sec NSI received.')
  response = nsi_mngr.get_sec_nsis()
  return response[0], response[1]

# GETS a specific Sec_NSI
@app.route('/sec_nsi/<sec_nsi_uuid>', methods=['GET'])
def get_sec_nsi(sec_nsi_uuid):
  config_sys.logger.info('Request to get Sec NSI received.')
  response = nsi_mngr.get_sec_nsi(sec_nsi_uuid)
  return response[0], response[1]

# Deletes a specific TERMINATED Sec_NSI data object from DB
@app.route('/sec_nsi/<sec_nsi_uuid>', methods=['DELETE'])
def delete_sec_nsi(sec_nsi_uuid):
  config_sys.logger.info('Request to delete Sec NSI received.')
  response = nsi_mngr.remove_sec_nsi(sec_nsi_uuid)
  return response[0], response[1]

# Triggers a Sec_NSI termination
@app.route('/sec_nsi/terminate/<sec_nsi_uuid>', methods=['POST'])
def terminate_sec_nsi(sec_nsi_uuid):
  config_sys.logger.info('Request to terminate Sec NSI received.')
  #TODO: Validate uuid existance
  config_sys.executor.submit(nsi_mngr.terminate_sec_nsi, sec_nsi_uuid)

  response = {}
  response['log'] = "Request accepted, terminating the E2E Network Slice."
  return response, 200



################################### MAIN SERVER FUNCTION ###################################
if __name__ == '__main__':
  # Initializes the system logs
  config_sys.init_logging()
  
  # Prepare configuration settings
  config_sys.logger.info('Environment variables set.')
  config_sys.init_environment()
  
  # Launches the threadpool with  5 workers
  config_sys.logger.info('Thread pool created with ' + str(os.environ.get("WORKERS")) + ' workers')
  config_sys.init_thread_pool(int(os.environ.get("WORKERS")))

  # Run main server thread
  config_sys.logger.info('Secure Network Slcies 4 SSLA service READY.')
  app.run(debug=False, host='0.0.0.0', port=os.environ.get("SERVICE_PORT"))
