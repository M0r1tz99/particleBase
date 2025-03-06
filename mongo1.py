import pymongo
import pandas as pd
import numpy as np
import sys
import os
import shutil
from datetime import datetime
import socket
import logging

logging.basicConfig(level=logging.INFO)

hostname=socket.gethostname() # AGCO laptop hostname: EARANENG865XTV3

# Import own "moritzfunctions" library - depends on directory and if run on cluster or local windows PC (assuming here that linux is on cluster)
if sys.platform == "win32":
    hpc_flag = False
    if hostname == "Lars":
        sys.path.append(os.path.normpath(r'D:\OneDrive - AGCO Corp\Desktop\Diploma Thesis\Python\moritzfunctions')) 
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

#%% NiceGUI

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

# Fetch data from the collection
data = list(collection.find())[0]["crop 1 / wheat"]



# # Function to recursively build the tree structure
# def build_tree(data):
#     nodes = []
#     for key, value in data.items():
#         node = {'id': key, 'label': key}
#         if isinstance(value, dict):
#             node['children'] = build_tree(value)
#         else:
#             node['label'] = f"{key}: {value}"
#         nodes.append(node)
#     return nodes


# Function to recursively build the tree structure up to a certain depth
def build_tree(data, depth=2, current_depth=0):
    nodes = []
    for key, value in data.items():
        node = {'id': key, 'label': key}
        if isinstance(value, dict) and current_depth < depth:
            node['children'] = build_tree(value, depth, current_depth + 1)
        nodes.append(node)
    return nodes




# Function to convert the dictionary to the NiceGUI tree format
def convert_to_tree_format(data, depth=2, current_depth=0):
    nodes = []
    for key, value in data.items():
        node = {'id': key, 'label': key}
        if isinstance(value, dict) and current_depth < depth:
            node['children'] = convert_to_tree_format(value, depth, current_depth + 1)
        nodes.append(node)
    return nodes

# # Function to convert the dictionary to the NiceGUI tree format
# def convert_to_tree_format(data, path='', depth=2, current_depth=0):
#     nodes = []
#     for key, value in data.items():
#         node_path = f"{path}/{key}" if path else key
#         node = {'id': key.split('/')[-1], 'path': node_path}
#         if isinstance(value, dict) and current_depth < depth:
#             node['children'] = convert_to_tree_format(value, node_path, depth, current_depth + 1)
#         if isinstance(value, str) and current_depth < depth:
#             node['children'] = [{'id': f'{value}'}]
#         nodes.append(node)
#     return nodes

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


# Function to update the right column dynamically
def update_dynamic_right_column(tree_element):
    target_key = tree_element.value
    path, value_to_display = find_key_path_and_value(data, target_key, path='')

    # ui.clear()
    if isinstance(value_to_display, str):
        with ui.row():
            ui.label(value_to_display)
    elif isinstance(value_to_display, dict):
        with ui.row():
            nodes = convert_to_tree_format(value_to_display, depth=2)
            ui.tree(nodes=nodes, label_key='id').expand()

# Function to get data by path
def get_data_by_path(data, path):
    keys = path.split('/')
    for key in keys:
        if key in data:
            data = data[key]
        else:
            return {}
    return data



# Function to display details of the selected item
def display_details(details):
    # ui.clear('details')
    
    ui.notify(f'Trying to show details for {details}')
    
    with ui.column(id='details'):
        for key, value in details.items():
            if isinstance(value, dict):
                ui.label(f"{key}:")
                for sub_key, sub_value in value.items():
                    ui.label(f"  {sub_key}: {sub_value}")
            else:
                ui.label(f"{key}: {value}")





particle_sim_dataset_list = find_key_value_pairs(data, "particle_simulation_dataset")     

#%% NiceGUI application
@ui.page('/')
def main_page():
    ui.label('Particle simulation data base demo').style('font-size: 24px; font-weight: bold;')
    
    # with ui.left_drawer().classes('bg-blue-100') as left_drawer:
    
    # # tree.on_select(lambda e: display_details(get_data_by_path(data, e.value)))  # Get data by path
    # tree.on_select(lambda e: update_dynamic_right_column(e))
    # tree.on_select(lambda e: ui.notify(f'{e}, {dir(e)}'))

    


    
    
    
    # Create header with tabs
    with ui.header().classes(replace='row items-center') as header:
        ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
        with ui.tabs() as tabs:
            for dataset in particle_sim_dataset_list:
                ui.tab(dataset[0])
    
    with ui.footer(value=False) as footer:
        ui.label('Footer')
    
    with ui.left_drawer().classes('bg-blue-100') as left_drawer:
        ui.label('Side menu')
        ui.label('Data Base Tree')
        
        nodes = convert_to_tree_format(data, depth=4)
        tree = ui.tree(nodes=nodes, node_key='id').expand()
        
        ui.input('filter').bind_value_to(tree, 'filter')
        with ui.row():
            ui.button('+ all', on_click=tree.expand)
            ui.button('- all', on_click=tree.collapse)
    
    
    # Create tab panels dynamically
    with ui.tab_panels(tabs, value=particle_sim_dataset_list[0]).classes('w-full'):
        for dataset in particle_sim_dataset_list:
            with ui.tab_panel(dataset[0]):
                nodes = convert_to_tree_format(dataset[1], depth=10)
                tree = ui.tree(nodes=nodes, node_key='id').expand()


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

