#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

from config_files import config_system as config_sys

# POLICY FRAMEWORK EMULATED

CONTENT_HEADER = {'Content-Type':'application/xml'}

policies_list = [
    {
        "ssla-capability":["5G_E2E_TRAFFIC_CONFIDENTIALITY_AND_INTEGRITY_PROTECTION"],
        "name": "Channel_Protection",
        "id": "mspl_9f1a88b4fc67421b98de270d5a63d35a",
        "monitoring-name": "Network_traffic_analysis",
        "monitoring-id":"mspl_eef61525d1594412bdcef34a4bfb7fc9"
    },
    {
        "ssla-capability":["5G_SYSTEM_ANTI_DDOS_PROTECTION"],
        "name": "Channel_Protection",
        "id": "mspl_9f1a88b4fc67421b98de270d5a63d35a",
        "monitoring-name": "Network_traffic_analysis",
        "monitoring-id":"mspl_eef61525d1594412bdcef34a4bfb7fc9"
    },
    {
        "ssla-capability":["DETECTION_OF_CRYPTOCURRENCY_MINING_IN_5G_TRAFFIC"],
        "name": "DDos_attack_protection",
        "id": "mspl_zzf61525d1594412bdcef34a4bfb7fc7",
        "monitoring-name": "Network_traffic_analysis",
        "monitoring-id":"mspl_aef61525d1594412bdcef34a4bfb7fc7"
    }
]

"""
    pf_mngr_ip = os.environ.get("PF_IP")
    pf_mngr_port = os.environ.get("PF_PORT")
    url = "http://"+ str(pf_mngr_ip) + ":" + str(pf_mngr_port) +"/policy/"+str(policy_id)
    response = requests.get(url, headers=CONTENT_HEADER)
    if response.status_code != 200:
        return [], response.status_code
    else:
        #TODO: process the response.text from XML to JSON
        policy = []
    return policy, 201
"""

# Retrieve policies based on the ssla capabilities
# NOTE if two capabilities have the same policy associated, that policy is returned once associated to both cpabilities
def get_policies_by_sla(ssla_caps):
    config_sys.logger.info('POLICY-FRAMEWORK: Retrieving Policis associated to the SSLA capabilities requested.')
    temp_list = []
    selected_policies = []
    #config_sys.logger.info('POLICY-FRAMEWORK: policies_list' + str(policies_list))
    for policy_item in policies_list:
        for cap_item in ssla_caps:
            if cap_item in policy_item["ssla-capability"]:
                temp_list.append(policy_item)

    #config_sys.logger.info('POLICY-FRAMEWORK: temp_list' + str(temp_list))
    for temp_item in temp_list:
        if selected_policies == []:
            selected_policies.append(temp_item)
        else:
            matched_policy = False
            for pol_ref_item in selected_policies:
                if (temp_item["id"] == pol_ref_item["id"] and temp_item["monitoring-id"] == pol_ref_item["monitoring-id"]):
                    updated_cap_list = pol_ref_item["ssla-capability"]
                    updated_cap_list.append(temp_item["ssla-capability"][0])
                    pol_ref_item["ssla-capability"] = updated_cap_list
                    matched_policy = True
            
            if matched_policy == False:
                selected_policies.append(temp_item)
        
    #config_sys.logger.info('POLICY-FRAMEWORK: selected_policies' + str(selected_policies))
    return selected_policies, 201

