import pymongo
import pandas as pd
import numpy as np
import sys
import os
import shutil
from datetime import datetime
import socket
import logging

from pprint import pprint

logging.basicConfig(level=logging.INFO)

hostname=socket.gethostname() # AGCO laptop hostname: EARANENG865XTV3

# Import own "moritzfunctions" library - depends on directory and if run on cluster or local windows PC (assuming here that linux is on cluster)
if sys.platform == "win32":
    hpc_flag = False
    if hostname == "Lars":
        sys.path.append(os.path.normpath(r'D:\OneDrive - AGCO Corp\Desktop\repos\straw\moritzfunctions')) 
    else:
        sys.path.append(os.path.normpath(r'C:\Users\ms11030\OneDrive - AGCO Corp\Desktop\repos\straw\moritzfunctions'))
else:
    hpc_flag = True
    # Setup for RAN CPU cluster "anika"
    if "agco" in hostname:
        sys.path.append(os.path.normpath(r'/home/nfs/mschaller/work/moritzfunctions/'))
    # Setup for TUD cluster "barnard"
    else:
        sys.path.append(os.path.normpath(r'/data/horse/ws/s1700951-conda_ws_1/moritzfunctions'))
    latex_flag = False # LaTex currently not supported on the Barnard HPC cluster
import moritzfunctions as mf

runtime_start = datetime.now()
print('=============================================================================')
try:
    script_name = os.path.basename(__file__)
except NameError:
    # Wenn __file__ not defined, set script_name
    script_name = "Unknown source file"
now = runtime_start.strftime('%d.%m.%Y, %H:%M:%S')
if hpc_flag:
    print(f"[{now}] Host {hostname} launched {script_name} on Linux.")
else:
    print(f"[{now}] Host {hostname} launched {script_name} on Windows.")
print('=============================================================================')




mongo_flag = False


if mongo_flag:
    
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    
    db = client["database"]
      
    collection = db["particleBase_demo"]
    
    
    
    
    # Daten in die Sammlung einfügen
    crops_dict = mf.load_list_from_json("crops_instance1.json")
    
    crops_dict_list = [crops_dict]
    
    dblist = client.list_database_names()
    
    # Check if the database exists
    dblist = client.list_database_names()
    if "database" in dblist:
        print("The database exists.")
        # Drop the existing collection
        collection.drop()
        print("Collection dropped.")
    
    # Insert new data into the collection
    collection.insert_many(crops_dict_list)
    print("New data inserted.")
    
    # a = list(collection.find())[0]["crop 1 / wheat"]

#% NiceGUI

def find_key_path_and_value(data, target_key, path=''):
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}/{key}" if path else key
            if key == target_key:
                return new_path, value
            result = find_key_path_and_value(value, target_key, new_path)
            if result:
                return result
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_path = f"{path}[{index}]"
            result = find_key_path_and_value(item, target_key, new_path)
            if result:
                return result
    return None, None

# Beispiel-Dictionary
data = {
    "phenoma": {
        "phenomen_1 / Rigid body simulation": {
            "general_info": {
                "general_solving_approach": "Bullet SDK utilized via pyBullet v. 3.25 Python API",
                "Other Specifications": None
            }
        },
        "phenomen_2 / Particle drag force": {
            "general_info": {
                "general_solving_approach": "Drag coefficient formulation by Clift et al.",
                "Projection method for particle area": "Custom Python implementation"
            }
        }
    },
    "phases": {
        "lagrangian_phases": {
            "lagrangian_phase_1 / Capsular chopped wheat straw": {
                "general_particle_data": {
                    "rho_p": 150
                }
            }
        }
    }
}



# Suche nach einem Key
key_to_find = "general_solving_approach"
path, value = find_key_path_and_value(data, key_to_find)
print(f"Key '{key_to_find}' found at: {path} with value: {value}")


def find_key_value_pairs(d, target_key):
    results = []

    def search_dict(d):
        if isinstance(d, dict):
            for key, value in d.items():
                if key == target_key:
                    results.append((key, value))
                if isinstance(value, dict):
                    search_dict(value)
                elif isinstance(value, list):
                    for item in value:
                        search_dict(item)

    search_dict(d)
    return results





from nicegui import ui
from pymongo import MongoClient

if mongo_flag:
    
    # Fetch data from the collection
    data = list(collection.find())[0]["crop 1 / wheat"]
    data["label"] = "wheat"

else:
    crops_dict = mf.load_list_from_json("crops_instance1.json")
    data = crops_dict["crop 1 / wheat"]
    data["label"] = "wheat"
    



#######


def dict_to_tree(data, label_key='label', node_key='id', max_depth=None):
    data = add_unique_ids_and_labels_to_dict(data)
    
    def convert(d, depth=0):
        if isinstance(d, dict):
            node = {node_key: d.get(node_key, ''), label_key: d.get(label_key, ''), 'children': []}
            if max_depth is None or depth < max_depth:
                
                for key, value in d.items():
                    if key not in [node_key, label_key]:
                        if isinstance(value, dict):
                            node['children'].append(convert(value, depth + 1))
                        # elif isinstance(value, list):
                        #     for item in value:
                        #         node['children'].append(convert(item, depth + 1))
                        
                        elif isinstance(value, (int, float, str, tuple, list)):
                            node['label']=f'{key}: {value}' # node['children'].append({node_key: '', label_key: f'{key}: {value}'})
                            # node['label']=f'{key}'
                            # node['children'].append({node_key: value[0], label_key: value[1]})
            return node
        return {}

    return [convert(data)]



# Function to find key path and value
def find_key_path_and_value(data, target_key, path=''):
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}/{key}" if path else key
            if key == target_key:
                return new_path, value
            result = find_key_path_and_value(value, target_key, new_path)
            if result:
                return result
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_path = f"{path}[{index}]"
            result = find_key_path_and_value(item, target_key, new_path)
            if result:
                return result
    return None, None






# # Function to display details of the selected item
# def display_details(details):
#     # ui.clear('details')
    
#     ui.notify(f'Trying to show details for {details}')
    
#     with ui.column(id='details'):
#         for key, value in details.items():
#             if isinstance(value, dict):
#                 ui.label(f"{key}:")
#                 for sub_key, sub_value in value.items():
#                     ui.label(f"  {sub_key}: {sub_value}")
#             else:
#                 ui.label(f"{key}: {value}")


def add_unique_ids_to_dict(d, start_id=1):
    current_id = start_id

    def assign_ids(d):
        nonlocal current_id
        if isinstance(d, dict):
            d['id'] = current_id
            current_id += 1
            for key, value in d.items():
                if isinstance(value, dict):
                    assign_ids(value)
                elif isinstance(value, list):
                    for item in value:
                        assign_ids(item)

    assign_ids(d)
    return d

def add_unique_ids_and_labels_to_dict(d, start_id=1):
    current_id = start_id

    def assign_ids_and_labels(d, parent_key=None):
        nonlocal current_id
        if isinstance(d, dict):
            d['id'] = current_id
            if parent_key is not None:
                d['label'] = parent_key
            current_id += 1
            for key, value in d.items():
                if isinstance(value, dict):
                    assign_ids_and_labels(value, key)
                # elif isinstance(value, list):
                #     for item in value:
                #         assign_ids_and_labels(item, key)
                
                # elif key not in ['id', 'label'] and isinstance(value, (int, float, str, tuple, list)):
                #     d[key] = (current_id, value)
                #     current_id += 1

    assign_ids_and_labels(d)
    return d

def remove_ids_and_labels_from_dict(d):
    def remove_keys(d):
        if isinstance(d, dict):
            d.pop('id', None)
            d.pop('label', None)
            for key, value in d.items():
                if isinstance(value, dict):
                    remove_keys(value)
                elif isinstance(value, list):
                    for item in value:
                        remove_keys(item)

    remove_keys(d)
    return d

def find_dict_element_by_id(d, target_id):
    if isinstance(d, dict):
        if d.get('id') == target_id:
            return d
        for key, value in d.items():
            if isinstance(value, dict):
                result = find_dict_element_by_id(value, target_id)
                if result is not None:
                    return result
            elif isinstance(value, list):
                for item in value:
                    result = find_dict_element_by_id(item, target_id)
                    if result is not None:
                        return result
    return None


particle_sim_dataset_list = find_key_value_pairs(data, "particle_simulation_dataset")     

# for dataset in particle_sim_dataset_list:
    

# test = conv_dict2tree(data, depth=10,)
test1 = dict_to_tree(data, max_depth=10)
test2 = dict_to_tree(particle_sim_dataset_list[0][1], max_depth=10)
# each element in the tree shall have an unique id
mf.save_list_to_json(test1, "test1.json", overwrite_flag=True)
mf.save_list_to_json(test2, "test2.json", overwrite_flag=True)

s = find_dict_element_by_id(test2[0], 30)



#%% NiceGUI application
@ui.page('/')
def main_page():
    # ui.label('Particle simulation data base demo').style('font-size: 24px; font-weight: bold;')
    
    # Create header with tabs
    with ui.header().classes(replace='row items-center') as header:
        ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
        with ui.tabs() as tabs:
            for dataset in particle_sim_dataset_list:
                ui.tab(dataset[1]["general_info"]["short_string"])
    
    # with ui.footer(value=False) as footer:
    #     ui.label('Footer')
    
    #### Side menu
    with ui.left_drawer().classes('bg-blue-100') as left_drawer:

        ui.label('Data base tree').style('font-weight: bold;')
        
        nodes = dict_to_tree(data, max_depth=6)
        tree = ui.tree(nodes=nodes, node_key='id', label_key='label').expand()
        
        tree.on_select(lambda e: ui.notify(f'Clicked element {e}')) 
        
        # # Event-Handler für Tree-Element-Auswahl
        # tree.on_select(lambda e: show_details(e.value))
        
        ui.input('filter').bind_value_to(tree, 'filter')
        with ui.row():
            ui.button('+ all', on_click=tree.expand)
            ui.button('- all', on_click=tree.collapse)
    
    
    # Create tab content panels dynamically
    with ui.tab_panels(tabs, value=particle_sim_dataset_list[0][1]["general_info"]["short_string"]).classes('w-full'):
        for dataset in particle_sim_dataset_list:
            with ui.tab_panel(dataset[1]["general_info"]["short_string"]) as tab_panel:
                nodes = dict_to_tree(dataset[1], max_depth=30)  # dataset[1]
                tree = ui.tree(nodes=nodes, node_key='id', label_key='label').expand()
                ui.input('filter').bind_value_to(tree, 'filter')
                with ui.row():
                    ui.button('+ all', on_click=tree.expand)
                    ui.button('- all', on_click=tree.collapse)
                

                
                # Funktion zum Anzeigen der Details
                def show_details(element_id):
                    element = find_dict_element_by_id(data, element_id)
                    
                    detail_frame = ui.row()
                    
                    if element:
                        with detail_frame:
                            # ui.label(f'Details for ID {element_id}').style('font-weight: bold;')
                            for key, value in element.items():
                                ui.label(f'{key}: {value}')
                                
                            ui.button('Clear', on_click=detail_frame.clear)

                
                # Event-Handler für Tree-Element-Auswahl
                tree.on_select(lambda e: ui.notify(f'Clicked element {e}')) 
                tree.on_select(lambda e: show_details(e.value))
                


                

# Detail-Frame erstellen


# Funktion zum Anzeigen der Details
    


# Start NiceGUI server
ui.run()





# #!/usr/bin/env python3
# from nicegui import ui

# with ui.header().classes(replace='row items-center') as header:
#     ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
#     with ui.tabs() as tabs:
#         ui.tab('A')
#         ui.tab('B')
#         ui.tab('C')

# with ui.footer(value=False) as footer:
#     ui.label('Footer')

# with ui.left_drawer().classes('bg-blue-100') as left_drawer:
#     ui.label('Side menu')

# with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
#     ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

# with ui.tab_panels(tabs, value='A').classes('w-full'):
#     with ui.tab_panel('A'):
#         ui.label('Content of A')
#     with ui.tab_panel('B'):
#         ui.label('Content of B')
#     with ui.tab_panel('C'):
#         ui.label('Content of C')

# ui.run()

