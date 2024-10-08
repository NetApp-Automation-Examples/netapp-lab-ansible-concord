from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError, AnsibleFilterError
from ansible.module_utils._text import to_text, to_native #, to_bytes, 

import string
import re   


######
# TODO: Double check we are properly handling strings / errors via 
# https://blog.artis3nal.com/2019-11-02-creating-a-custom-ansible-plugin/
######

# TODO: Full test coverage

def human_sort(list):
    """A poor man's natsort without needing to install that package"""
    return sorted(list, key=lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', s)])


def check_for_true_in_dict(dictionary, keys=[]): 
    """Given a list of keys, see if any of them exist in the dict and have a value of 'true'"""
    for key in keys:
        if key in dictionary and dictionary[key] == 'true':
            return True
    
    return False

def filter_root_aggrs(aggregate_info):
    """Filter out root aggregates from na_ontap_info's aggregate_info subset"""
    aggrs = {}
    for key, aggr in aggregate_info.items():
        if 'aggr_raid_attributes' not in aggr:
            raise AnsibleFilterError("You must pass the `aggregate_info` subset from na_ontap_info")
        
        if check_for_true_in_dict(aggr['aggr_raid_attributes'], ['is_root_aggregate']):
            continue

        aggrs[key] = aggr

    return aggrs


def filter_root_volumes(volume_info):
    """Filter out node/svm root volumes from na_ontap_info's volume_info subset"""
    volumes = {}
    for key, info in volume_info.items():
        if 'volume_state_attributes' not in info:
            raise AnsibleFilterError("You must pass the `volume_info` subset from na_ontap_info")

        if check_for_true_in_dict(info['volume_state_attributes'], ['is_vserver_root', 'is_node_root']):
            continue 

        volumes[key] = info
    
    return volumes


def calculate_least_utilized_aggr_name(aggregate_info):
    """Given na_ontap_info's aggregate_info subset, find the aggr with
    the most space available and return the aggr name
    """
    a = filter_root_aggrs(aggregate_info)
    if not a: 
        raise AnsibleFilterError("There are no non-root aggregates")

    # Build a dict of aggr name -> size available and return the max value
    space = {n: int(d['aggr_space_attributes']['size_available']) for n, d in a.items()}
    return max(space, key=lambda k: space[k])
    


def convert_list_of_short_port_names_to_full(net_port_info, ports=[]):
    """Given na_ontap_info's net_port_info subset, convert a list of short port 
    names to full port names, i.e [e0e, e0f] -> [node-01:e0e, node-01:e0f]
    """
    port_list = []
    for port, portinfo in net_port_info.items():
        if 'port' not in portinfo:
            raise AnsibleFilterError("You must pass the `net_port_info` subset from na_ontap_info")

        if portinfo['port'] in ports: 
            port_list.append(port)

    return port_list

def convert_rest_results_to_flat_list(
        rest_records, 
        remove_keys=['_links', 'uuid']):
    
    cli_list = []
    
    for row in rest_records:
        for key in remove_keys: 
            row.pop(key, None)

        if 'svm' in row:
            svm = row.pop('svm')
            row['svm'] = svm['name']
        
        if 'ip' in row:
            ip = row.pop('ip')
            row['ip'] = ip['address']+'/'+ip['netmask'] 

        if 'location' in row:
            location = row.pop('location')
            row['is_home'] = location['is_home']
            row['current'] = location['node']['name']+':'+location['port']['name'] 
            row['home'] = location['home_node']['name']+':'+location['home_port']['name']
        
        cli_list.append(row)

    return cli_list 

    



def build_list_of_svm_names(vserver_info, types=['data']):
    """Given na_ontap_info's vserver_info subset, return a list of svm names
    filtered by type.
    """
    svm_list = []
    for svm, info in vserver_info.items():
        if info['vserver_type'] in types: 
            svm_list.append(svm)

    return human_sort(svm_list)


def build_list_of_volume_names(volume_info, match=False, contains=False, root_volumes=False):
    """Given na_ontap_info's volume_info subset, return a list of volume names that meet the criteria"""
    volumes_list = []
    if not root_volumes:
        volume_info = filter_root_volumes(volume_info)

    for dummy, info in volume_info.items():
        name = info['volume_id_attributes']['name']
        # If match is set, skip ones that don't a) start with the match b) may simply just contain the match
        if match and (name.startswith(match) == False or name.rstrip(string.digits) != match):
            continue

        # If contains is set, just check that it contains the name
        if contains and name.contains(contains) == False: 
            continue

        volumes_list.append(name)
    
    return human_sort(volumes_list)


def calculate_volume_name_with_increment(volume_name, volume_info, increment=1): 
    """Given a volume name, filter na_ontap_info's 'volume_info' subset by matching 
    volumes to calculate the next increment, returning volume name + next increment
    """
    increments = [0]
    volume_list = build_list_of_volume_names(volume_info, match=volume_name) 
    if volume_list:
        increments = sorted([int(n.strip(volume_name)) for n in volume_list], reverse=True) 

    return(volume_name+str(increments[0]+int(increment))) 

# This is not sophisticated, may refactor if performance is an issue
def return_invalid_failover_groups(failover_groups, cluster_nodes):
    """Pass the ports from each failover group to validate_port_group() 
    to find and return invalid failover groups
    """
    invalid_failover_groups = []

    for group in failover_groups:
    
        if validate_port_group(group['targets'], cluster_nodes) == False:
            invalid_failover_groups.append(group)
                
    return invalid_failover_groups

# This is not sophisticated, may refactor if performance is an issue
def return_invalid_broadcast_domains(broadcast_domains, cluster_nodes):
    """Pass the ports from each broadcast domain to validate_port_group() 
    to find and return invalid broadcast domains
    """ 

    invalid_broadcast_domains = []

    for bd in broadcast_domains:
    
        if validate_port_group(bd['ports'], cluster_nodes) == False:
            invalid_broadcast_domains.append(bd)
                
    return invalid_broadcast_domains

def build_list_of_ha_pairs(cluster_nodes):
    """Given a list of cluster nodes from the REST API, return a simple list of ha pair names"""
    ha_pairs = []
    for node in cluster_nodes:
        ha_pair = [node['name']]

        for partner in node['ha']['partners']:
            ha_pair.append(partner['name'])
        
        sorted_ha_pair = human_sort(ha_pair)
        if sorted_ha_pair not in ha_pairs:
            ha_pairs.append(sorted_ha_pair)

    return sorted(ha_pairs)

def validate_port_group(ports_list, cluster_nodes):
    """Given a list of ports, only return True if there is at least one 
    port on every node in the cluster, and all vlan tags match"""

    ports = []
    nodes = []
    vlans = []

    # Iterate through each port in the ports list
    for target in ports_list:
        node, port = target.split(':')  # Split the port into node and port

        # Check for vlan tags and add to list
        vlan = port.split('-')
        if len(vlan) > 1:
            vlans.append(vlan[1])   
        
        ports.append(port)
        nodes.append(node)   
         
    # No vlans is fine. One vlan is fine. 
    # However if we have more than one vlan tag, we have a problem.
    # We also have a problem if some ports have a vlan tag and some don't
    unique_vlans = set(vlans)
    if len(unique_vlans) > 1 or (len(unique_vlans) == 1 and len(vlans) != len(ports)):
        return False   
    
    # If vlans are ok, make sure all nodes are reprensented
    if len(set(nodes)) == len(cluster_nodes):
        return True

    return False

def convert_ontap_version(version_dict):
    """Given an ONTAP version dict from ONTAP REST API 
    (i.e. NetApp Release 9.11.1P1: Tue Aug 09 13:13:19 UTC 2022) 
    return the version in 'x.x.x' i.e. '9.11.1.P1' format"""
    error_msg = "Expected ONTAP Version string should be in format similar to this: \
                'NetApp Release 9.11.1P1: Tue Aug 09 13:13:19 UTC 2022' but instead \
                got '"

    if isinstance(version_dict, dict) == False or 'full' not in version_dict:    
         raise AnsibleFilterError("You must pass a dict from ONTAP Rest API cluster cluster/nodes results with the `version` field")

    try: 
        # This was missing patch versions 
        #return str(version_dict['generation'])+'.'+str(version_dict['major'])+'.'+str(version_dict['minor'])
        version_string = version_dict['full'].split(':', 1)[0].replace('NetApp Release','').strip()

        # There should be several periods in the output, if there is not 
        # something is wrong, abort
        if "." not in version_string: 
            raise exception

        return version_string 

    except:
        raise AnsibleFilterError(error_msg+version_dict['full']+"'")

# Any python file you put in filter_plugins/ with this class structure 
# will get picked up by your playbooks. You just need to map each 
# function name you'll use in the playbook to a python function
class FilterModule(object):
    def filters(self):
        return {
            'human_sort': human_sort,
            'ontap_least_utilized_aggr': calculate_least_utilized_aggr_name,
            'ontap_full_port_names': convert_list_of_short_port_names_to_full,
            'ontap_svm_names': build_list_of_svm_names,
            'ontap_filter_root_volumes': filter_root_volumes, 
            'ontap_filter_root_aggrs': filter_root_aggrs,
            'ontap_volume_names': build_list_of_volume_names,
            'ontap_volume_name_increment': calculate_volume_name_with_increment,
            'ontap_find_invalid_failover_groups': return_invalid_failover_groups,
            'ontap_find_invalid_broadcast_domains': return_invalid_broadcast_domains,
            'ontap_ha_pairs': build_list_of_ha_pairs,
            'ontap_version': convert_ontap_version,
            'ontap_flatten_rest_results': convert_rest_results_to_flat_list,
        }
