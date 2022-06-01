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
                root_mspl = security_mspl(root_mspl, capability_item, policy_item, omspl_id)
    
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
    
    for domain_item in subnet_item['domains']:
        serv_domain = ET.SubElement(service, 'domainID')
        serv_domain.text = str(domain_item)
    
    securityRequirements = ET.SubElement(securedService, 'securityRequirements', {'id':ssla_id}) #TODO: WHERE DOES THIS ID COME FROM? For now, we use the slice-id
    for sloid_item in slo_ids:
        sloID = ET.SubElement(securityRequirements, 'sloID')
        sloID.text = str(sloid_item)

    securityPolicies = ET.SubElement(securedService, 'securityPolicies')
    for policyid_item in policies_ids:
        msplID = ET.SubElement(securityPolicies, 'msplID')
        msplID.text = policyid_item

    return root_mspl

def security_mspl(root_mspl, capability_item, policy_item, omspl_id):
    #Level 1: ITResource sub-element
    ITResource_info = {
        'id':capability_item['mspl_id'],
        'orchestrationID':omspl_id,
        'tenantID':'1'
    }
    ITResource = ET.SubElement(root_mspl, 'ITResource', ITResource_info)

    #### Level 2 - configuration tag
    configuration = ET.SubElement(ITResource, 'configuration', {'xsi:type':policy_item['policy']['configuration']['type']})
    # Level 3 - configuration tag
    conf_name = ET.SubElement(configuration, 'Name')
    conf_name.text = 'Conf0'
    capability = ET.SubElement(configuration, 'capability')
    cap_name = ET.SubElement(capability, 'Name')
    cap_name.text = policy_item['capability-ssla']
    configurationRule = ET.SubElement(configuration, 'configurationRule')
    # Level 4+ - configuration tag
    configurationRule_name = ET.SubElement(configurationRule, 'Name')
    configurationRule_name.text = "Rule0"
    configurationRule_isCNF = ET.SubElement(configurationRule, 'isCNF')
    configurationRule_isCNF.text = 'false'
    
    externalData = ET.SubElement(configurationRule, 'externalData', {'xsi:type':policy_item['policy']['configuration']['configurationRule']['externalData']['type']})
    externalData_value = ET.SubElement(externalData, 'value')
    externalData_value.text = policy_item['policy']['configuration']['configurationRule']['externalData']['value']
    
    configurationRuleAction = ET.SubElement(configurationRule, 'configurationRuleAction', {'xsi:type':policy_item['policy']['configuration']['configurationRule']['configurationRuleAction']['type']})
    if policy_item['policy']['configuration']['configurationRule']['configurationRuleAction']['type'] == 'DataProtectionAction':
        technology = ET.SubElement(configurationRuleAction, 'technology')
        technology.text = policy_item['policy']['configuration']['configurationRule']['configurationRuleAction']['technology']
        technologyActionParameters = ET.SubElement(configurationRuleAction, 'technologyActionParameters')
        for techActionParam_item in policy_item['policy']['configuration']['configurationRule']['configurationRuleAction']['technologyActionParameters']:
            technologyParameter = ET.SubElement(technologyActionParameters, 'technologyParameter', {'xsi:type':techActionParam_item['type']})
            localEndpoint = ET.SubElement(technologyParameter, 'localEndpoint')
            localEndpoint.text = techActionParam_item['localEndpoint']
            remoteEndpoint = ET.SubElement(technologyParameter, 'remoteEndpoint')
            remoteEndpoint.text = techActionParam_item['remoteEndpoint']
        for techActionSecProp_item in policy_item['policy']['configuration']['configurationRule']['configurationRuleAction']['technologyActionSecurityProperty']:
            technologyActionSecurityProperty = ET.SubElement(configurationRuleAction, 'technologyActionSecurityProperty', {'xsi:type':techActionSecProp_item['type']})
            for key_item in techActionSecProp_item.keys():
                if key_item != 'type':
                    techActionSecProp_element = ET.SubElement(technologyActionSecurityProperty, key_item)
                    techActionSecProp_element.text = techActionSecProp_item[key_item]
    elif policy_item['policy']['configuration']['configurationRule']['configurationRuleAction']['type'] == 'MonitoringAction':
        monitoringActionType = ET.SubElement(configurationRuleAction, 'monitoringActionType')
        monitoringActionType.text = policy_item['policy']['configuration']['configurationRule']['configurationRuleAction']['monitoringActionType']
        if policy_item['policy']['configuration']['configurationRule']['configurationRuleAction']['aditionalMonitoringParameters'] != []:
            aditionalMonitoringParameters = ET.SubElement(configurationRuleAction, 'aditionalMonitoringParameters')
            for adMoniParam_item in policy_item['policy']['configuration']['configurationRule']['configurationRuleAction']['aditionalMonitoringParameters']:
                for key_item in adMoniParam_item.keys():
                    if key_item != 'type':
                        adMoniParam_item_element = ET.SubElement(aditionalMonitoringParameters, key_item)
                        adMoniParam_item_element.text = adMoniParam_item[key_item]
    else:
        config_sys.logger.info('MSPL (Security): ERROR WITH A configurationRuleAction TYPE')

    configurationCondition = ET.SubElement(configurationRule, 'configurationCondition', {'xsi:type':policy_item['policy']['configuration']['configurationRule']['configurationCondition']['type']})
    configurationCondition_isCNF = ET.SubElement(configurationCondition, 'isCNF')
    configurationCondition_isCNF.text = "false"
    if policy_item['policy']['configuration']['configurationRule']['configurationCondition']['type'] == 'MonitoringConfigurationConditions':
        monitoringConfigurationCondition = ET.SubElement(configurationCondition, 'monitoringConfigurationCondition')
        isCNF = ET.SubElement(monitoringConfigurationCondition, 'isCNF')
        isCNF.text = "true"
        packetFilterCondition = ET.SubElement(monitoringConfigurationCondition, 'packetFilterCondition')
        for key_item in policy_item['policy']['configuration']['configurationRule']['configurationCondition']['monitoringConfigurationCondition']['packetFilterCondition'].keys():
            if key_item != 'type':
                packetFilterCondition_element = ET.SubElement(packetFilterCondition, key_item)
                packetFilterCondition_element.text = policy_item['policy']['configuration']['configurationRule']['configurationCondition']['monitoringConfigurationCondition']['packetFilterCondition'][key_item]
        
        if 'channelProtected' in policy_item['policy']['configuration']['configurationRule']['configurationCondition']['monitoringConfigurationCondition'].keys():
            channelProtected = ET.SubElement(monitoringConfigurationCondition, 'channelProtected')
            channelProtected.text = policy_item['policy']['configuration']['configurationRule']['configurationCondition']['monitoringConfigurationCondition']['channelProtected']
        
        maxCount = ET.SubElement(monitoringConfigurationCondition, 'maxCount')     
        isCNF =    ET.SubElement(maxCount, 'isCNF')
        isCNF.text = policy_item['policy']['configuration']['configurationRule']['configurationCondition']['monitoringConfigurationCondition']['maxCount']['isCNF']
        count =    ET.SubElement(maxCount, 'count')
        for key_item in policy_item['policy']['configuration']['configurationRule']['configurationCondition']['monitoringConfigurationCondition']['maxCount']['count'].keys():
            if key_item != 'type':
                count_element = ET.SubElement(count, key_item)
                count_element.text = policy_item['policy']['configuration']['configurationRule']['configurationCondition']['monitoringConfigurationCondition']['maxCount']['count'][key_item]

    #### Level 2 - priority tag
    if 'priority' in policy_item['policy']:
        priority = ET.SubElement(ITResource, 'priority')
        priority.text = policy_item['policy']['priority']
    
    #### Level 2 - dependencies tag
    if 'dependencies' in policy_item['policy'].keys():
        dependencies = ET.SubElement(ITResource, 'dependencies')
        # Level 3 - dependencies tag
        for dependency_item in policy_item['policy']['dependencies']:
            dependency = ET.SubElement(dependencies, 'dependency', {'xsi:type':dependency_item['type']})
            if 'eventID' in dependency_item.keys():
                eventID = ET.SubElement(dependency, 'eventID')
                eventID.text = dependency_item['eventID']
            configurationCondition = ET.SubElement(dependency, 'configurationCondition', {'xsi:type':dependency_item['configurationCondition']['type']})
            for key_item in dependency_item['configurationCondition'].keys():
                if key_item != 'type':
                    if key_item == 'packetFilterCondition':
                        configCond_element = ET.SubElement(configurationCondition, key_item)
                        for key_item_2 in dependency_item['configurationCondition']['packetFilterCondition'].keys():
                            pcktFlCond_element = ET.SubElement(configCond_element, key_item_2)
                            pcktFlCond_element.text = dependency_item['configurationCondition']['packetFilterCondition'][key_item_2]
                    else:
                        configCond_element = ET.SubElement(configurationCondition, key_item)
                        configCond_element.text = dependency_item['configurationCondition'][key_item]


    #### Level 2 - enforcementRequirements tag
    enforcementRequirements = ET.SubElement(ITResource, 'enforcementRequirements')
    enforcementDomains = ET.SubElement(enforcementRequirements, 'enforcementDomains')
    if capability_item['domains'] != []:
        for domain_item in capability_item['domains']:
            domainID = ET.SubElement(enforcementDomains, 'domainID')
            domainID.text = str(domain_item)

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