import os
import shutil
import sys
import argparse
from getpass import getpass
from sstash.sstash import SecureStash

class MachinatorError(Exception): pass

def store_machine(machine_name,stash_path):
    """
    Export a docker-machine from to the machines dir.
    Based on "machine-share":
    https://github.com/bhurlow/machine-share/blob/master/export.sh
    """

    home_path = os.path.expanduser('~')
    machine_path = os.path.join(home_path,'.docker','machine','machines',\
        machine_name)
    certs_path = os.path.join(home_path,'.docker','machine','certs')

    if not os.path.isdir(machine_path):
        raise MachinatorError('Machine {} does not exist. Aborting.'
                .format(machine_name))

    # Prompt user for stash password:
    password = getpass("Stash password:")
    ss = SecureStash(stash_path,password)

    ss.write_dir(['machines',machine_name,'certs'],certs_path)
    ss.write_dir(['machines',machine_name,'machine_info'],machine_path)

    # Adding domain_name, to be domain agnostic:
    # ss.write_value(['machines',machine_name,'machine_info','domain_name'],
    #         domain_name.encode('utf-8'))

    # Avoid dependence on machine by removing home dir dependant paths and
    # replacing them with a place holder:
    # TODO: Check if this is actually working.
    config_json_key = ['machines',machine_name,'machine_info','config.json']
    config_json_data = ss.read_value(config_json_key).decode('utf-8')
    config_json_data = config_json_data.replace(home_path,'{{HOME}}')
    ss.write_value(config_json_key,config_json_data.encode('utf-8'))


def load_machine(machine_name,stash_path):
    """
    Import a docker-machine from the machines dir.
    """
    home_path = os.path.expanduser('~')
    machine_path = os.path.join(home_path,'.docker','machine','machines',\
        machine_name)
    certs_path = os.path.join(home_path,'.docker','machine','certs')

    # Make sure that we don't already have this machine in the homedir
    # inventory:
    if os.path.isdir(machine_path):
        raise MachinatorError('Machine {} already exists. Aborting.'\
            .format(machine_name))

    # Prompt user for stash password:
    password = getpass("Stash password:")
    ss = SecureStash(stash_path,password)

    if machine_name not in ss.get_children(['machines']):
        raise MachinatorError('Machine {} does not exist in inventory. Aborting.\n'
                'Available machines: {}'\
                .format(machine_name, ss.get_children(['machines'])))

    ss.read_dir(['machines',machine_name,'machine_info'],machine_path)
    # Remove current set of certs if exists:
    try:
        shutil.rmtree(certs_path)
    except FileNotFoundError:
        pass
    ss.read_dir(['machines',machine_name,'certs'],certs_path)
    
    # Replace the {{HOME}} placeholder with the current machine's home dir:
    config_json_path = os.path.join(machine_path,'config.json')
    with open(config_json_path,'r') as fr:
        config_json_data = fr.read()
    config_json_data.replace('{{HOME}}',home_path)
    with open(config_json_path,'w') as fw:
        fw.write(config_json_data)


def store_cmd(args):
    store_machine(args.machine, args.stash_path)

def load_cmd(args):
    load_machine(args.machine, args.stash_path)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='help for subcommand')

    parser_load = subparsers.add_parser('load', help='Load a machine')
    parser_load.add_argument('machine', type=str, 
            help='Name of machine')
    parser_load.add_argument('stash_path', type=str, 
            help='path of stash file')
    parser_load.set_defaults(func=load_cmd)

    parser_store = subparsers.add_parser('store', help='Store a machine')
    parser_store.add_argument('machine', type=str, 
            help='Name of machine')
    parser_store.add_argument('stash_path', type=str, 
            help='path of stash file')
    parser_store.set_defaults(func=store_cmd)

    args = parser.parse_args()
    if not hasattr(args,'func'):
        parser.print_help()
        sys.exit(0)

    args.func(args)
    sys.exit(0)

