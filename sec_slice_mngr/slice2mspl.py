#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
import xml.etree.ElementTree as ET

from config_files import config_system as config_sys

def generateMSPL(e2e_nsi_json, policies_list):
    config_sys.logger.info('MSPL-GENERATOR: Generating the MSPL objct for the E2E SO.')
    # Level 0 (root): ITResourceOrchestration element
    omspl_id = str(uuid.uuid4())            #NOTE: where does this osmpl_id come from? DataServices?
    omspl_id = omspl_id.replace('-', '')
    omspl_id = "mspl_"+omspl_id
    ITResourceOrchestration_info = {
        'id':omspl_id,
        'xmlns':'http://modeliosoft/xsddesigner/a22bd60b-ee3d-425c-8618-beb6a854051a/ITResource.xsd',
	    'xmlns:xsi':'http://www.w3.org/2001/XMLSchema-instance',
	    'xsi:schemaLocation':'http://modeliosoft/xsddesigner/a22bd60b-ee3d-425c-8618-beb6a854051a/ITResource.xsd scheme\mspl.xsd',
        'sliceID':e2e_nsi_json['id'],             #NOTE why is this sliceID here???? is it necessary?
        'tenantID':'1'
    }
    root_mspl = ET.Element('ITResourceOrchestration', ITResourceOrchestration_info)

    # extracts specific information requried for the policies items
    slo_ids = []
    policies_ids = []
    for capability_item in e2e_nsi_json['security-sla']['capabilities']:
        policies_ids.append(capability_item['mspl_id'])
        for slo_item in capability_item['slos']:
            slo_ids.append(slo_item['SLO_ID'])      

    # prepares the deployment policies items for the MSPL
    for subnet_item in e2e_nsi_json['netslice-subnets']:
        root_mspl = deployment_mspl(root_mspl, subnet_item, omspl_id, e2e_nsi_json['id'], e2e_nsi_json['security-sla']['id'], slo_ids, policies_ids)
    
    # prepares the security policies items for the MSPL
    for capability_item in e2e_nsi_json['security-sla']['capabilities']:
        for policy_item in policies_list:
            if capability_item['capability-ssla'] == policy_item['capability-ssla']:
                root_mspl = security_mspl(root_mspl, capability_item, policy_item)
    
    #write to file
    tree = ET.ElementTree(indent(root_mspl))
    tree.write('MSPL_test.xml', xml_declaration=True, encoding='utf-8')

    return tree

def deployment_mspl(root_mspl, subnet_item, omspl_id, slice_id, ssla_id, slo_ids, policies_ids):
    #Level 1: ITResource sub-element
    ITResource_info = {
        'id':subnet_item['deployment-policy'],
        'orchestrationID':omspl_id,
        'tenantID':'1'
    }
    ITResource = ET.SubElement(root_mspl, 'ITResource', ITResource_info)

    # Level 2: configuration sub-element
    configuration = ET.SubElement(ITResource, 'configuration', {'xsi:type':'RuleSetConfiguration'})

    # Level 3: name sub-element
    conf_name = ET.SubElement(configuration, 'Name')
    conf_name.text = 'Conf0'
    
    # Level 3: capability sub-element
    capability = ET.SubElement(configuration, 'capability', {'xsi:type':'FiveGSecuritySlice'})
    # Level 4: capability information
    cap_name = ET.SubElement(capability, 'Name')
    cap_name.text = subnet_item['name']
    sliceID = ET.SubElement(capability, 'sliceID')
    sliceID.text = slice_id

    # Level 3: configurationRule sub-element
    configurationRule = ET.SubElement(configuration, 'configurationRule')
    # Level 4: configurationRule information and sub-elements
    rule_name = ET.SubElement(configurationRule, 'Name')
    rule_name.text = "Rule0"
    isCNF = ET.SubElement(configurationRule, 'isCNF')
    isCNF.text = 'false'
    configurationCondition = ET.SubElement(configurationRule, 'configurationCondition')
    isCNF = ET.SubElement(configurationCondition, 'isCNF')
    isCNF.text = 'false'
    configurationRuleAction = ET.SubElement(configurationRule, 'configurationRuleAction', {'xsi:type':'FiveGSecuritySliceAction'})
    fiveGSecuritySliceActionType = ET.SubElement(configurationRuleAction, 'fiveGSecuritySliceActionType')
    fiveGSecuritySliceActionType.text = 'DEPLOY'
    # Level 5: securedService information and sub-elements
    securedService = ET.SubElement(configurationRuleAction, 'securedService')
    service = ET.SubElement(securedService, 'service', {'id':subnet_item['id']})
    serv_name = ET.SubElement(service, 'name')
    serv_name.text = subnet_item['name']
    serv_type = ET.SubElement(service, 'type')
    serv_type.text = subnet_item['type']
    serv_domain = ET.SubElement(service, 'domainID')
    serv_domain.text = '3'                #NOTE: update with the domain infor from the Data Services.
    
    securityRequirements = ET.SubElement(securedService, 'securityRequirements', {'id':ssla_id}) #TODO: WHERE DOES THIS ID COME FROM? For now, we use the slice-id
    for sloid_item in slo_ids:
        sloID = ET.SubElement(securityRequirements, 'sloID')
        sloID.text = str(sloid_item)

    securityPolicies = ET.SubElement(securedService, 'securityPolicies')
    for policyid_item in policies_ids:
        msplID = ET.SubElement(securityPolicies, 'msplID')
        msplID.text = policyid_item

    return root_mspl

def security_mspl(root_mspl, capability_item, policy_item):
    #Level 1: ITResource sub-element
    ITResource_info = {
        'id':subnet_item['deployment-policy'],
        'orchestrationID':omspl_id,
        'tenantID':'1'
    }
    ITResource = ET.SubElement(root_mspl, 'ITResource', ITResource_info)

    
    return root_mspl

#pretty print method
def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem