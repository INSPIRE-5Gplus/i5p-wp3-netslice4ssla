#!/usr/local/bin/python3.4

import os, sys, logging, json, argparse, time, datetime, requests, uuid
import xml.etree.ElementTree as ET

from config_files import config_system as config_sys

def generateMSPL(e2e_nsi_json) :
    config_sys.logger.info('MSPL-GENERATOR: Generating the MSPL objct for the E2E SO.')
    # Level 0 (root): ITResourceOrchestration element
    ITResourceOrchestration_info = {
        'id':e2e_nsi_json['deployment-policy'],
        'xmlns':'http://modeliosoft/xsddesigner/a22bd60b-ee3d-425c-8618-beb6a854051a/ITResource.xsd',
	    'xmlns:xsi':'http://www.w3.org/2001/XMLSchema-instance',
	    'xsi:schemaLocation':'http://modeliosoft/xsddesigner/a22bd60b-ee3d-425c-8618-beb6a854051a/ITResource.xsd scheme\mspl.xsd'
    }
    root = ET.Element('ITResourceOrchestration', ITResourceOrchestration_info)

    #Level 1: ITResource sub-element
    itresource_id = str(uuid.uuid4())
    itresource_id = itresource_id.replace('-', '')
    itresource_id = "mspl_"+itresource_id
    ITResource_info = {
        'id':itresource_id,
        'orchestrationID':e2e_nsi_json['deployment-policy'],
        'tenantID':'1'
    }
    ITResource = ET.SubElement(root, 'ITResource', ITResource_info)

    # Level 2: configuration sub-element
    configuration = ET.SubElement(ITResource, 'configuration', {'xsi:type':'RuleSetConfiguration'})

    # Level 3: name sub-element
    conf_name = ET.SubElement(configuration, 'Name')
    conf_name.text = 'Conf0'
    
    # Level 3: capability sub-element
    capability = ET.SubElement(configuration, 'capability', {'xsi:type':'FiveGSecuritySlice'})
    # Level 4: capability information
    cap_name = ET.SubElement(capability, 'Name')
    cap_name.text = e2e_nsi_json['name']
    sliceID = ET.SubElement(capability, 'sliceID')
    sliceID.text = e2e_nsi_json['id']

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
    # Level 5: configurationRuleAction information and sub-elements
    configurationRuleAction = ET.SubElement(configurationRule, 'configurationRuleAction', {'xsi:type':'FiveGSecuritySliceAction'})
    fiveGSecuritySliceActionType = ET.SubElement(configurationRuleAction, 'fiveGSecuritySliceActionType')
    fiveGSecuritySliceActionType.text = 'DEPLOY'
    # Level 6: securedService information and sub-elements
    securedService = ET.SubElement(configurationRuleAction, 'securedService')
    for subnet_item in e2e_nsi_json['netslice-subnets']:
        service = ET.SubElement(securedService, 'service', {'id':subnet_item['id']})
        serv_name = ET.SubElement(service, 'name')
        serv_name.text = subnet_item['name']
        serv_type = ET.SubElement(service, 'type')
        serv_type.text = subnet_item['type']
    #TODO: ASK ABOUT THIS ID, WHERE SHOULD IT COME FROM? SSLA? For now, we use the slice-id
    securityRequirements = ET.SubElement(securedService, 'securityRequirements', {'id':e2e_nsi_json['id']})
    for secreq_item in e2e_nsi_json['security-sla']['security-requirements']:
        sloID = ET.SubElement(securityRequirements, 'sloID')
        sloID.text = secreq_item['sloID']

    securityPolicies = ET.SubElement(securedService, 'securityPolicies')
    for policy_item in e2e_nsi_json['security-sla']['mapped-policies']:
        msplID = ET.SubElement(securityPolicies, 'msplID')
        msplID.text = policy_item['policy-id']

    #write to file
    tree = ET.ElementTree(indent(root))
    tree.write('MSPL_test.xml', xml_declaration=True, encoding='utf-8')

    return tree


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