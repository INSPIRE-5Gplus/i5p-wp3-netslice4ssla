#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, uuid, requests
from flask.wrappers import Response
from flask import Flask, request, jsonify
from configparser import ConfigParser
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Lock

from config_files import config_system as config_sys
from mappers import ssla_mngr_mapper as ssla_mngr
from sec_slice_mngr import nsi_mngr


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

########################################### NST API #################################################
# NOTE: --> DO WE USE OSM or SONATA?
#       --> Do we consider an NST at this level (E2E) a set of NSTs at Domain level? If so, do we create NSTs o I simple show a list of "domain NSTs" to be selcted when deploying a SecNSI?

# gets all the NSTs
@app.route('/nst', methods=['GET'])
def get_all_nst():
  print("NST list: []")

# gets a specific NST
@app.route('/nst/<nst_uuid>', methods=['GET'])
def get_nst(nst_uuid):
  print("NST requested with uuid: " + str(nst_uuid))

########################################### NSI API #################################################
# Triggers a Secured NSI deployment
@app.route('/sec_nsi', methods=['POST'])
def deploy_sec_nsi():
  config_sys.logger.info('Request to deploy Sec NSI received.')
  incoming_request =  request.json
  #TODO: Validate selected NST and SSLA existance
  config_sys.executor.submit(nsi_mngr.deploy_sec_nsi, incoming_request)

# GETS all the secured NSI
@app.route('/sec_nsi', methods=['GET'])
def get_all_sec_nsi():
  config_sys.logger.info('Request to get all Sec NSI received.')
  response = nsi_mngr.get_sec_nsis()
  return response[0], response[1]

# GETS a specific secured NSI
@app.route('/sec_nsi/<sec_nsi_uuid>', methods=['GET'])
def get_sec_nsi(sec_nsi_uuid):
  config_sys.logger.info('Request to get Sec NSI received.')
  response = nsi_mngr.get_sec_nsi(sec_nsi_uuid)
  return response[0], response[1]

# Deletes a specific secured NSI data object from DB
@app.route('/sec_nsi/<sec_nsi_uuid>', methods=['DELETE'])
def delete_sec_nsi(sec_nsi_uuid):
  config_sys.logger.info('Request to delete Sec NSI received.')
  response = nsi_mngr.remove_sec_nsi(sec_nsi_uuid)
  return response[0], response[1]

# Triggers a Secured NSI termination
@app.route('/sec_nsi/terminate/<sec_nsi_uuid>', methods=['POST'])
def terminate_sec_nsi(sec_nsi_uuid):
  config_sys.logger.info('Request to terminate Sec NSI received.')
  #TODO: Validate uuid existance
  config_sys.executor.submit(nsi_mngr.terminate_sec_nsi, sec_nsi_uuid)


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
  config_sys.logger.info(' <-- Secure Network Slcies 4 SSLA service is READY. -->')
  app.run(debug=False, host='localhost', port=os.environ.get("SERVICE_PORT"))
