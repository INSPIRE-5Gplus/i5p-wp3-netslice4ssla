#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

CONTENT_HEADER_XML = {'Content-Type':'application/xml'}
CONTENT_HEADER_JSON = {'Content-Type':'application/json'}

## Security Orchestrator API Options ##
# Add Domain (POST /domains) --> # NOTE: NOT NECESSARY
# Update Domain (PUT /domains/{domainId}) --> # NOTE: NOT NECESSARY
# Remove Domain (DELETE /domains/{domainId}) --> # NOTE: NOT NECESSARY

# Retrieve Domains ID LIST (GET /domains)
def get_domains():
    so_ip = os.environ.get("SO_IP")
    so_port = os.environ.get("SO_PORT")
    url = "http://"+ str(so_ip) + ":" + str(so_port) +"/domains"
    response = requests.get(url, headers=CONTENT_HEADER_JSON)
    if response.status_code != 200:
        return [], response.status_code
    else:
        #TODO: process the response.text from XML to JSON
        domains_json = []

    return domains_json, 201

# Retrieve Domain (GET /domains/{domainId})
def get_domain(domain_id):
    so_ip = os.environ.get("SO_IP")
    so_port = os.environ.get("SO_PORT")
    url = "http://"+ str(so_ip) + ":" + str(so_port) +"/domains/"+str(domain_id)
    response = requests.get(url, headers=CONTENT_HEADER_JSON)
    if response.status_code != 200:
        return [], response.status_code
    else:
        #TODO: process the response.text from XML to JSON
        ssla_json = []

    return ssla_json, 201

# Request New Policy Enforcement (POST /domains/{domainId}/policy-enforcements)
"""
expected body request:
    {
        "policyType: "string",
        "policyContent": "string",
        "ssla": "string"
    }
"""
def request_policy(domain_id, policy_data):
    # policy_data must be a string with an XML format
    data_dumps = json.dumps(policy_data)

    so_ip = os.environ.get("SO_IP")
    so_port = os.environ.get("SO_PORT")
    url = "http://"+ str(so_ip) + ":" + str(so_port) +"/domains/"+str(domain_id)+"/policy-enforcements"
    response = requests.post(url, headers=CONTENT_HEADER_XML, data=data_dumps)     

    if response.status_code != 200:
        return [], response.status_code
    else:
        #TODO: process the response.text from XML to JSON
        ssla_json = []

    return ssla_json, 201

# Retrieve Policy Enforcements IDs list of all domains (GET /domains/{domainId}/policy-enforcements)
def get_policyenforcementsID():
    response = get_domains()
    if resposne.status_code != 200:
        msg = 'SEC_NSI element not found.'
        code = 404
        return {'msg':msg}, code
    
    domains_id_list = response[0]
    policies_id_list = []
    for domain_id_item in domains_id_list:
        so_ip = os.environ.get("SO_IP")
        so_port = os.environ.get("SO_PORT")
        url = "http://"+ str(so_ip) + ":" + str(so_port) +"/domains/"+str(domain_id_item)+"/policy-enforcements"
        response = requests.get(url, headers=CONTENT_HEADER_JSON)
        if response.status_code != 200:
            return [], response.status_code
        else:
            domain_policies = {}
            domain_policies["domain_id"] = domain_id_item
            domain_policies["policy-enforcements"] = response[0]
            policies_id_list.append(domain_policies)

    return policies_id_list, 201

# Retrieve Policy Enforcement Info from specific domain (GET /domains/{domainId}/policy-enforcements/{enforcementId})
def get_policy_enforcement(domain_id, enforced_policy_id):
    so_ip = os.environ.get("SO_IP")
    so_port = os.environ.get("SO_PORT")
    url = "http://"+ str(so_ip) + ":" + str(so_port) +"/domains/"+str(domain_id)+"/policy-enforcements/"+str(enforced_policy_id)
    response = requests.get(url, headers=CONTENT_HEADER_JSON)
    if response.status_code != 200:
        return [], response.status_code
    else:
        return response[0], 201

# Undo Policy Enforcement (DELETE /domains/{domainId}/policy-enforcements/{enforcementId})
def request_policy(domain_id, enforcedpolicy_id):
    so_ip = os.environ.get("SO_IP")
    so_port = os.environ.get("SO_PORT")
    url = "http://"+ str(so_ip) + ":" + str(so_port) +"/domains/"+str(domain_id)+"/policy-enforcements/"+str(enforcedpolicy_id)
    response = requests.delete(url, headers=CONTENT_HEADER_JSON)     

    if response.status_code != 200:
        return [], response.status_code
    else:
        #TODO: process the response.text from XML to JSON
        ssla_json = []

    return ssla_json, 201
