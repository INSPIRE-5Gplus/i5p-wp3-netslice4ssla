#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

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

# Retrieve policies based on the ssla capabilities
# NOTE if two capabilities have the same policy associated, that policy is returned once associated to both cpabilities
def get_policies_by_sla(ssla_caps):
    temp_list = []
    selected_policies = []
    for policy_item in policies_list:
        for cap_item in ssla_caps:
            if cap_item in policy_item["ssla-capability"]:
                temp_list.append(policy_item)

    for temp_item in temp_list:
        if selected_policies == []:
            selected_policies.append(temp_item)
        else:
            for pol_ref_item in selected_policies:
                if (temp_item["id"] == pol_ref_item["id"] and temp_item["monitoring-id"] == pol_ref_item["monitoring-id"]):
                    updated_cap_list = pol_ref_item["ssla-capability"]
                    updated_cap_list.append(temp_item["ssla-capability"][0])
                    pol_ref_item["ssla-capability"] = updated_cap_list
        
    return selected_policies, 201

