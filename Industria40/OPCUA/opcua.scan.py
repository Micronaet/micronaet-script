#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pdb
from opcua import Client
# from opcua.tools import endpoint_to_strings

def print_node(node,level=0):
    try:
        space = '  ' * level
        print(space, ' ---> Data:', node, node.get_value())
        data_value = node.get_data_value()
        for detail in data_value.ua_types:
            detail_name = detail[0]
            print(
                space, 
                '      ---> Detail:', 
                detail_name, 
                data_value.__getattribute__(detail_name),
                )
        
    except:
        print(space, ' | Structure', node)
        for child_node in node.get_children():
            print_node(child_node, level=level+1)
           

uri = "opc.tcp://192.168.1.186:4840"

client = Client(uri)
client.connect()

# -----------------------------------------------------------------------------
# A. Fast information:
# -----------------------------------------------------------------------------
check_is_allarm = client.get_node("ns=6;s=::AsGlobalPV:Allarmi.Presente")
print('Is Allarm', check_is_allarm.get_data_value().Value._value)
check_is_working = client.get_node(
    "ns=6;s=::AsGlobalPV:PezzoPLC_InLavoro.CaricaInLavoroOK")
print('Is Working', check_is_working.get_data_value().Value._value)
pdb.set_trace()
sys.exit()
      
# -----------------------------------------------------------------------------
# Browse node:
# -----------------------------------------------------------------------------
# Some start:
root_node = client.get_root_node()
global_node = client.get_node("ns=6;s=::AsGlobalPV")
working_node = client.get_node("ns=6;s=::AsGlobalPV:AttrezzaturaInLavoro")
piece_working_node = client.get_node("ns=6;s=::AsGlobalPV:PezzoPLC_InLavoro")
type_node = client.get_node("ns=0;i=24")

# Setup and browse:
start_node = piece_working_node  # TODO Changeme
print_node(start_node)
client.disconnect()
sys.exit()

node = client.get_node("ns=6;s=::AsGlobalPV:Allarmi.Codice")
print(node.get_node_class())
print(node.get_browse_name())
print(node.get_display_name())
print(node.get_description())
print(node.get_data_type())
pdb.set_trace()
client.disconnect()
sys.exit()


# node =  client.get_node("ns=6;s=::AsGlobalPV:Allarmi.Presente")
node =  client.get_node("ns=6;s=::AsGlobalPV:Allarmi.Contatore")
print(node.get_value())
pdb.set_trace()
node =  client.get_node("ns=6;s=::AsGlobalPV:Allarmi")

# node = client.get_node("ns=6;s=::AsGlobalPV:VersionePLC")
# print(node.get_value())
client.disconnect()
sys.exit()


