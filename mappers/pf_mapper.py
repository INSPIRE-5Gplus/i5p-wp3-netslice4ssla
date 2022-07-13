#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid

from config_files import config_system as config_sys

# POLICY FRAMEWORK EMULATED

CONTENT_HEADER = {'Content-Type':'application/xml'}

# TODO: ADD the capabilities-policies for the SSLA 2 
policies_list = [
    {
        "capability-ssla":"Channel_Protection",
        "capability-name": "E2E traffic confidentiality, integrity and authenticity protection",
        "slos":[
            {
                "SLO_ID": 1,
                "metric": "5G_TRAFFIC_ENCRYPTION_ALGORITHM",
                "SLO": "AES_128_GCM",
                "capability": "Channel_Protection"
            },
            {
                "SLO_ID": 2,
                "metric": "5G_TRAFFIC_INTEGRITY_PROTECTION_ALGORITHM",
                "SLO": "SHA256",
                "capability": "IPSec_protocol"
            },
            {
                "SLO_ID": 0,
                "metric": "5G_TRAFFIC_ORIGIN_AUTHENTICATION_MECHANISM",
                "SLO": "PSK",
                "capability": "DTLS_protocol"
            }
        ],
        "policy":[
            {
                "slice":["5GCore"],
                "slos": [1,2],
                "configuration":{
                    "type": "RuleSetConfiguration",
                    "name": "Conf0",
                    "configurationRule":{
                        "name": "Rule0",
                        "isCNF": "false",
                        "configurationRuleAction":{
                            "type": "DataProtectionAction",
                            "technology": "None",
                            "technologyActionParameters":[
                                {
                                    "key_TAP":"technologyParameter",
                                    "type": "GenericChannelProtectionTechnologyParameter",
                                    "localEndpoint": "[UE]",
                                    "remoteEndpoint":"[5GService]"
                                }
                            ],
                            "technologyActionSecurityProperty":[
                                {
                                    "type":"Confidentiality",
                                    "encryptionAlgorithm": "AES-CBC",
                                    "keySize": "128",
                                    "mode": "GCM"
                                },
                                {
                                    "type":"Integrity",
                                    "integrityAlgorithm": "SHA256"
                                }
                            ]
                        },
                        "configurationCondition":{
                            "type": "DataProtectionCondition",
                            "isCNF": "false"
                        },
                        "externalData":{
                            "type": "Priority",
                            "value": "0"
                        }
                    }
                },
                "priority":"1000",
                "dependencies":[
                    {
                        "type": "EventDependency",
                        "eventID": "VNF-READY",
                        "configurationCondition":{
                            "type": "FilteringConfigurationCondition",
                            "isCNF": "false",
                            "packetFilterCondition":{
                                "SourceAddress": "[5GService]"
                            }
                        }
                    }
                ]
            },
            {
                "slice":["5GIoTBroker"],
                "slos": [0,1,2],
                "configuration":{
                    "type": "RuleSetConfiguration",
                    "name": "Conf0",
                    "configurationRule":{
                        "name": "Rule0",
                        "isCNF": "false",
                        "configurationRuleAction": {
                            "type": "DataProtectionAction",
                            "technology": "None",
                            "technologyActionParameters":[
                                {
                                    "key_TAP":"technologyParameter",
                                    "type": "GenericChannelProtectionTechnologyParameter",
                                    "localEndpoint": "[5GCore]",
                                    "remoteEndpoint":"[5GIoTBroker]"
                                },
                                {
                                    "key_TAP":"authenticationParameters",
                                    "psKey_value": "[generated random string]",
                                    "remote_id":"user1"
                                }
                            ],
                            "technologyActionSecurityProperty":[
                                {
                                    "type":"Authentication",
                                    "peerAuthenticationMechanism": "[preshared_key]"
                                },
                                {
                                    "type":"Confidentiality",
                                    "encryptionAlgorithm": "AES",
                                    "keySize": "128",
                                    "mode": "GCM"
                                },
                                {
                                    "type":"Integrity",
                                    "integrityAlgorithm": "SHA256"
                                }
                            ]
                        },
                        "configurationCondition":{
                            "type": "DataProtectionCondition",
                            "isCNF": "false"
                        },
                        "externalData":{
                            "type": "Priority",
                            "value": "0"
                        }
                    }
                },
                "priority":"1000",
                "dependencies":[
                    {
                        "type": "EventDependency",
                        "eventID": "SLICE-READY",
                        "configurationCondition":{
                            "type": "FilteringConfigurationCondition",
                            "isCNF": "false",
                            "packetFilterCondition":{
                                "SourceAddress": "[5GIoTBroker]"
                            }
                        }
                    }
                ]
            }
        ]
    },
    {
        "capability-ssla":"Proof_of_Transit",
        "capability-name": "Proof of Transit",
        "slos":[
            {
                "SLO_ID": 5,
                "metric": "PROOF_OF_TRANSIT_THROUGHPUT",
                "SLO": "1",
                "capability": "Proof_of_Transit"
            }
        ],
        "policy":[
            {
                "slice":["5GCore"],
                "slos": [5],
                "configuration":{
                    "type": "RuleSetConfiguration",
                    "name": "Conf0",
                    "configurationRule":{
                        "name": "Rule0",
                        "isCNF": "false",
                        "configurationRuleAction": {
                            "type": "MonitoringAction",
                            "monitoringActionType": "SECURITY_ANALYSIS",
                            "aditionalMonitoringParameters":[]
                        },
                        "configurationCondition":{
                            "type": "MonitoringConfigurationConditions",
                            "isCNF": "false",
                            "monitoringConfigurationCondition":{
                                "isCNF": "true",
                                "packetFilterCondition": {
                                    "SourceAddress": "[UE]",
                                    "DestinationAddress": "[5GService]",
                                },
                                "channelProtected": "false",
                                "maxCount":{
                                    "isCNF": "false",
                                    "count": {
                                        "measureUnit": "BYTE",
                                        "value": "1",
                                        "per": "SECOND"
                                    }
                                }
                            }
                        },
                        "externalData":{
                            "type": "Priority",
                            "value": "500"
                        }
                    }
                },
                "dependencies":[
                    {
                        "type": "PolicyDependency",
                        "configurationCondition":{
                            "type": "PolicyDependencyCondition",
                            "isCNF": "false",
                            "policyID": "Channel_Protection",
                            "status": "ENFORCED"
                        }
                    }
                ]
            }
        ]
    },
    {
        "capability-ssla":"Network_traffic_analysis",
        "capability-name": "CRYPTOCURRENCY MINING DETECTION IN 5G NETWORK TRAFFIC",
        "slos":[
            {
                "SLO_ID": 3,
                "metric": "NETWORK_TRAFFIC_ANALYSIS_THROUGHPUT",
                "SLO": "1 BYTE/SECOND",
                "capability": "Network_traffic_analysis"
            }
        ],
        "policy":[
            {
                "slice":["5GCore", "5GIoTBroker"],
                "slos": [3],
                "configuration":{
                    "type": "RuleSetConfiguration",
                    "name": "Conf0",
                    "configurationRule":{
                        "name": "Rule0",
                        "isCNF": "false",
                        "configurationRuleAction": {
                            "type": "MonitoringAction",
                            "monitoringActionType": "BEHAVIORAL",
                            "aditionalMonitoringParameters":[
                                {
                                    "key": "behaviour",
                                    "value": "5GControlTraffic"
                                }
                            ]
                        },
                        "configurationCondition":{
                            "type": "MonitoringConfigurationConditions",
                            "isCNF": "false",
                            "monitoringConfigurationCondition":{
                                "isCNF": "true",
                                "packetFilterCondition": {
                                    "SourceAddress": "[5GService]",
                                    "bidirectional": "true"
                                },
                                "maxCount":{
                                    "isCNF": "false",
                                    "count": {
                                        "measureUnit": "BYTE",
                                        "value": "1",
                                        "per": "SECOND"
                                    }
                                }
                            }
                        },
                        "externalData":{
                            "type": "Priority",
                            "value": "500"
                        }
                    }
                },
                "dependencies":[
                    {
                        "type": "PolicyDependency",
                        "configurationCondition":{
                            "type": "PolicyDependencyCondition",
                            "isCNF": "false",
                            "policyID": "Channel_Protection",
                            "status": "ENFORCED"
                        }
                    }
                ]
            }
        ]
    },
    {
        "capability-ssla":"DDos_attack_protection",
        "capability-name": "5G SYSTEM DDOS DETECTION AND MITIGATION",
        "slos":[
            {
                "SLO_ID": 4,
                "metric": "ANTI_DDOS_PROTECTION_THROUGHPUT",
                "SLO": "500",
                "capability": "DDos_attack_protection"
            }
        ],
        "policy":
        [
            {
                "slice":["5GCore"],
                "slos": [4],
                "configuration":{
                    "type": "RuleSetConfiguration",
                    "name": "Conf0",
                    "configurationRule":{
                        "name": "Rule0",
                        "isCNF": "false",
                        "configurationRuleAction": {
                            "type": "MonitoringAction",
                            "monitoringActionType": "SECURITY_ANALYSIS",
                            "aditionalMonitoringParameters":[]
                        },
                        "configurationCondition":{
                            "type": "MonitoringConfigurationConditions",
                            "isCNF": "false",
                            "monitoringConfigurationCondition":{
                                "isCNF": "true",
                                "packetFilterCondition": {
                                    "SourceAddress": "[UE]",
                                    "DestinationAddress": "[5GService]",
                                },
                                "channelProtected": "false",
                                "maxCount":{
                                    "isCNF": "false",
                                    "count": {
                                        "measureUnit": "MBYTE",
                                        "value": "500",
                                        "per": "SECOND"
                                    }
                                }
                            }
                        },
                        "externalData":{
                            "type": "Priority",
                            "value": "500"
                        }
                    }
                }
            }
        ]
    }
]

# Retrieve policies based on the ssla capabilities
# NOTE if two capabilities have the same policy associated, that policy is returned once associated to both cpabilities
def get_policies_sla_capability(ssla_caps):
    config_sys.logger.info('POLICY-FRAMEWORK: Retrieving Policis associated to the SSLA capabilities requested.')
    selected_policies = []
    #config_sys.logger.info('POLICY-FRAMEWORK: policies_list' + str(policies_list))
    for policy_item in policies_list:
        for cap_item in ssla_caps:
            if cap_item == policy_item["capability-ssla"]:
                selected_policies.append(policy_item)

    #config_sys.logger.info('POLICY-FRAMEWORK: selected_policies' + str(selected_policies))
    return selected_policies, 201

