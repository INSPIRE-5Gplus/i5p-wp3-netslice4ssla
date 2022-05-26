import os, sys, logging, json, argparse, time, datetime, requests, uuid
from xml.dom.minidom import *


ssla_doc = parse("./data_objects/specs-SLATemplate-5G-Mobile-Comms.xml")

# GET SSLA NAME
ssla_name = ssla_doc.getElementsByTagName("wsag:Name")[0]
print(ssla_name.firstChild.data)

capabilities_list = ssla_doc.getElementsByTagName("specs:capability")
for capability in capabilities_list:
    cap_id = capability.getAttribute("id")
    print("id: %s" % cap_id)

mspl_id = str(uuid.uuid4())
print(mspl_id)
mspl_id = mspl_id.replace('-', '')
print(mspl_id)
mspl_id = "mspl_"+mspl_id
print(mspl_id)