#!/usr/bin/env python3
'''
Commands:
creds      Display credentials in database
db         Display database items
exit       Exit application
help       Display help information
info       Display additional module information
options    Display module options
run        Execute module
search     Search modules
set        Set option value
setg       Set global option value
unset      Unset option value
unsetg     Unset global option value
use        Select module for use
workspace  Workspace information

Use the help command with any of these commands for additional information

'''
import importlib
import time
import colorama
import pathlib
import readline
import sqlite3
import ipaddress
import concurrent.futures
import traceback
import os
import prettytable
import re
import string
import random
import sys

dict = {}
global_dict = {}
lib = False
os.chdir(pathlib.Path(__file__).parent)
# TODO MAKE AUTOCOMPLETE BETTER
CMD = [
    'creds',
    'db',
    'exit',
    'help',
    'info',
    'options',
    'run',
    'search',
    'set',
    'setg',
    'unset',
    'unsetg',
    'use',
    'workspace'    
    ]
for path in pathlib.Path(pathlib.Path() / 'modules').rglob('*.py'):
    module = str(path)[8:-3].replace('/','.')
    CMD.append(module)
global_dict['threads'] = [1, '']
cmd_input = ''
current_module = ''
threads = []

def completer(text, state):
    # TODO make this gooderer
    options = [ cmd for cmd in CMD if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None
readline.parse_and_bind('tab: complete')
readline.set_completer(completer)
    
def creds():
    '''
    Creds usage:
    creds - lists first 100 creds in datatbase
    creds [options] - sets different filter parameters, can use * for wildcard values
        -H host
        -n max number of rows to return
        -p port
        -P password
        -R set hosts to host option in current module
        -s column to sort by
        -u user
                
    '''
    try:
        if len(cmd_input) < 2:
            if pathlib.Path(pathlib.Path.home() / '.tef/databases/{}.db'.format(dict['database'])).is_file():
                with sqlite3.connect(pathlib.Path.home() / '.tef/databases/{}.db'.format(dict['database'])) as connection:
                    with connection as cursor:
                        creds = cursor.execute("SELECT host,port,protocol,username,password,notes FROM creds limit 100")
                        creds_table = prettytable.from_db_cursor(creds)
                        creds_table.align['host'] = 'l'
                        creds_table.max_width = os.get_terminal_size()[0]-60
                        creds_table[0]
                        print(creds_table)
                        print('No filters set, listing first 100 credentials, type "help creds" for more options')
                        print()
        
        else:
            query_list = []
            flags = cmd_input
            count = 0
            sort = 'host'
            query = "SELECT host,port,protocol,username,password,notes FROM creds "
            
            if '-H' in flags:
                host = flags[flags.index('-H')+1]
                host = host.replace('*','%')
                if count < 1:
                    query += 'WHERE host like ? '
                    query_list.append(host)
                count += 1

            if '-u' in flags:
                user = flags[flags.index('-u')+1]
                user = user.replace('*','%')
                if count < 1:
                    query += 'WHERE username like ? '
                    query_list.append(user)
                else:
                    query += 'and username like ? '
                    query_list.append(user)
                count += 1

            if '-p' in flags:
                port = flags[flags.index('-p')+1]
                if count < 1:
                    query += 'WHERE port = ? '
                    query_list.append(port)
                else:
                    query += 'and port = ? '
                    query_list.append(port)
                count += 1
                
            if '-P' in flags:
                password = flags[flags.index('-P')+1]
                password = password.replace('*','%')
                if count < 1:
                    query += 'WHERE password like ? '
                    query_list.append(password)
                else:
                    query += 'and password like ? '
                    query_list.append(password)
                count += 1

            if '-s' in flags:
                sort = flags[flags.index('-s')+1]

            if '-n' in flags:
                query += 'LIMIT ? '
                query_list.append(flags[flags.index('-n')+1])

            if pathlib.Path(pathlib.Path.home() / '.tef/databases/{}.db'.format(dict['database'])).is_file():
                with sqlite3.connect(pathlib.Path.home() / '.tef/databases/{}.db'.format(dict['database'])) as connection:
                    with connection as cursor:
                        result = cursor.execute(query, query_list)
                        
                        if '-R' in flags:
                            count = 0
                            alphanum = string.ascii_letters + string.digits
                            random_filename = ''.join((random.choice(alphanum) for i in range(8)))
                            with open('/tmp/{}'.format(random_filename),'x') as host_file:
                                for rows in result:
                                    host_file.write('{}\n'.format(rows[0]))
                                    count += 1
                                dict['host'][0] = 'file:/tmp/{}'.format(random_filename)
                                print('{} hosts saved to file /tmp/{}'.format(count, random_filename))
                               
                        
                        else:
                            creds_table = prettytable.from_db_cursor(result)
                            creds_table.align['host'] = 'l'
                            creds_table.max_width = os.get_terminal_size()[0]-60
                            creds_table.sortby = sort
                            creds_table[0]
                            print(creds_table)
    except KeyError:
        print('{} No module selected'.format(minus()))

    except IndexError as error:
        print('{} No results found'.format(minus()))                        
    
    except ValueError as error:
        raise ValueError(error)

    except Exception as error:
        raise Exception(error)

def db():
    """
    DB usage:
    db - lists first 100 results in datatbase
    db [options] - sets different filter parameters, can use * for wildcard values
        -H host
        -m module
        -n max number of rows to return
        -o output
        -p port
        -R set hosts to host option in current module
        -s column to sort by
                
    """
    try:
        if len(cmd_input) < 2:
            if pathlib.Path(pathlib.Path.home() / '.tef/databases/{}.db'.format(dict['database'])).is_file():
                with sqlite3.connect(pathlib.Path.home() / '.tef/databases/{}.db'.format(dict['database'])) as connection:
                    with connection as cursor:
                        creds = cursor.execute("SELECT host,port,protocol,module,output FROM module_data limit 100")
                        db_table = prettytable.from_db_cursor(creds)
                        db_table.align['host'] = 'l'
                        db_table.align['output'] = 'l'
                        db_table.max_width = os.get_terminal_size()[0]-60
                        db_table[0]
                        print(db_table)
                        print('No filters set, listing first 100 results, see db -h for more options')
                        print()
        
        else:
            query_list = []
            flags = cmd_input
            count = 0
            sort = 'host'
            query = "SELECT host,port,protocol,module,output FROM module_data "
            
            if '-h' in flags:
                print(__doc__)
                return

            if '-H' in flags:
                host = flags[flags.index('-H')+1]
                host = host.replace('*','%')
                if count < 1:
                    query += 'WHERE host like ? '
                    query_list.append(host)
                count += 1

            if '-p' in flags:
                port = flags[flags.index('-p')+1]
                if count < 1:
                    query += 'WHERE port = ? '
                    query_list.append(port)
                else:
                    query += 'and port = ? '
                    query_list.append(port)
                count += 1
            
            if '-m' in flags:
                module = flags[flags.index('-m')+1]
                module = module.replace('*','%')
                if count < 1:
                    query += 'WHERE module like ? '
                    query_list.append(module)
                else:
                    query += 'and module like ? '
                    query_list.append(module)
                count += 1
            
            if '-o' in flags:
                output = flags[flags.index('-o')+1]
                output = output.replace('*','%')
                if count < 1:
                    query += 'WHERE output like ? '
                    query_list.append(output)
                else:
                    query += 'and output like ? '
                    query_list.append(output)
                count += 1
                
            if '-s' in flags:
                sort = flags[flags.index('-s')+1]

            if '-n' in flags:
                query += 'LIMIT ? '
                query_list.append(flags[flags.index('-n')+1])

            if pathlib.Path(pathlib.Path.home() / '.tef/databases/{}.db'.format(dict['database'])).is_file():
                with sqlite3.connect(pathlib.Path.home() / '.tef/databases/{}.db'.format(dict['database'])) as connection:
                    with connection as cursor:
                        result = cursor.execute(query, query_list)
                        if '-R' in flags:
                            count = 0
                            alphanum = string.ascii_letters + string.digits
                            random_filename = ''.join((random.choice(alphanum) for i in range(8)))
                            with open('/tmp/{}'.format(random_filename),'x') as host_file:
                                for rows in result:
                                    host_file.write('{}\n'.format(rows[0]))
                                    count += 1
                                dict['host'][0] = 'file:/tmp/{}'.format(random_filename)
                                print('{} hosts saved to file /tmp/{}'.format(count, random_filename))
                                
                        else:
                            db_table = prettytable.from_db_cursor(result)
                            db_table.align['host'] = 'l'
                            db_table.align['output'] = 'l'
                            db_table.max_width = os.get_terminal_size()[0]-60
                            db_table.sortby = sort
                            db_table[0]
                            print(db_table)
    except KeyError:
        print('{} No module selected'.format(minus()))

    except IndexError as error:
        print('{} No results found'.format(minus()))  

    except ValueError as error:
        raise ValueError(error)

    except Exception as error:
        raise Exception(error)

def help():
    try:
        if len(cmd_input) < 2:
            print(__doc__)

        elif cmd_input[1].lower() in ['creds']:
            print(creds.__doc__)

        elif cmd_input[1].lower() in ['db']:
            print(db.__doc__)

        elif cmd_input[1].lower() in ['exit']:
            print(exit.__doc__)

        elif cmd_input[1].lower() in ['info']:
            print(info.__doc__)             

        elif cmd_input[1].lower() in ['options']:
            print(options.__doc__)

        elif cmd_input[1].lower() in ['run']:
            print(run.__doc__)

        elif cmd_input[1].lower() in ['search']:
            print(search.__doc__)

        elif cmd_input[1].lower() in ['set']:
            print(set_option.__doc__)

        elif cmd_input[1].lower() in ['setg']:
            print(setg_option.__doc__)

        elif cmd_input[1].lower() in ['unset']:
            print(unset_option.__doc__)

        elif cmd_input[1].lower() in ['unsetg']:
            print(unsetg_option.__doc__)

        elif cmd_input[1].lower() in ['use']:
            print(use.__doc__)

        elif cmd_input[1].lower() in ['workspace']:
            print(workspace.__doc__)

    
    except Exception as error:
        raise Exception(error)

def info():
    """

    Print additional module info from current module's info() function

    """
    global lib
    try:
        info_table = prettytable.PrettyTable()
        info_table.field_names = ['Key', 'Value']
        info_table.align['Key'] = 'l'
        info_table.align['Value'] = 'l'
        info_table.max_width = os.get_terminal_size()[0]-60

        info_dict = lib.info()
    
        if not lib:
            print('{} No module defined'.format(minus()))
        else:
            print('Module Information:')
            for keys in info_dict:
                info_table.add_row([keys, info_dict[keys]])
            print('{}'.format(info_table))

            print()
            print('Module Options:')
            options()
    except Exception as error:
        print(error)
        print(minus() + ' Module does not have additional info')

def init_database():
    if pathlib.Path(pathlib.Path.home() / '.tef/databases/{}.db'.format(dict['database'])).is_file():
        print('Loading database for workspace: {}'.format(dict['database']))
    
    else:
        print('Database not found, creating database for workspace: {}'.format(dict['database']))
        pathlib.Path(str(pathlib.Path.home())+'/.tef/databases').mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(pathlib.Path.home() / '.tef/databases/{}.db'.format(dict['database'])) as connection:
                with connection as cursor:
                    sqlite_create_table_query = '''CREATE TABLE module_data(
                                            id INTEGER PRIMARY KEY,
                                            host TEXT NOT NULL,
                                            port INTEGER,
                                            protocol TEXT,
                                            module TEXT NOT NULL, 
                                            output TEXT);'''
                    cursor.execute(sqlite_create_table_query)
                    
                    sqlite_create_table_query = '''CREATE TABLE creds(
                                            id INTEGER PRIMARY KEY,
                                            host TEXT NOT NULL,
                                            port INTEGER,
                                            protocol TEXT,
                                            username TEXT, 
                                            password TEXT,
                                            notes TEXT);'''
                    cursor.execute(sqlite_create_table_query)                    

def minus():
    return colorama.Fore.RED + '[-]' + colorama.Fore.RESET

def plus():
    return colorama.Fore.GREEN + '[+]' + colorama.Fore.RESET

def use():
    """
    Use usage:
    use "module" - Sets module to current module by name
    use "index" - Sets module to current module by search index

    Use search command for a list of modules  
    """
    global current_module
    global dict
    global lib
    try:
        if len(cmd_input) < 2:
            print(use.__doc__)
        
        else:
            if cmd_input[1].isdigit():
                lib = importlib.import_module('modules.' + module_list[int(cmd_input[1])-1])
                lib = importlib.reload(lib)
                cmd_input[1] = module_list[int(cmd_input[1])-1]
                current_module = '(' + cmd_input[1] + ') '

            else:
                lib = importlib.import_module('modules.' + cmd_input[1])
                lib = importlib.reload(lib)
                current_module = '(' + cmd_input[1] + ') '

            print(plus() + ' Module ' + cmd_input[1] + ' loaded')
            dict = {**dict,**lib.options()}
            temp_dict = {}
            for key in sorted(dict):
                temp_dict[key] = dict[key]
            dict = temp_dict.copy()
            dict['module'] = cmd_input[1].lower()
            for key in dict:
                if key in global_dict:
                    dict[key][0] = global_dict[key][0]
    except:
        print(minus() + ' Module not found')

def options():
    """
    Prints a list of options and their current values for the current module
    """
    global lib
    options_table = prettytable.PrettyTable()    
    options_table.field_names = ['Option', 'Value', 'Description']
    options_table.align['Option'] = 'l'
    options_table.align['Description'] = 'l'
    if not lib:
        print('{} No module defined'.format(minus()))
    else:        
        for key in dict:
            if key in lib.options():
                options_table.add_row([key,dict[key][0],dict[key][1]])
        print('\n{}\n'.format(options_table))

def run(dict):
    """
    Executes the current module using set options
    """
    global run_tasks
    hosts = []
    host = dict['host']
    try:
        hosts = host.split('.')

        if 'file' in host:
            temp_list = open(host[5:],'r')
            for host in temp_list:
                host = host.strip()
                dict['host'] = host
                spawn_threads(dict)
        
        else:
            for x in range(0, 4):    
                if ',' in hosts[x]:
                    num = hosts[x].split(',')
                    a = []
                    for numbers in num:
                        if '-' in numbers:
                            t = numbers.split('-')
                            a += range(int(t[0]), int(t[1]) +1)
                        else:
                            a.append(int(numbers))
                    hosts[x] = a
                elif '-' in hosts[x]:
                    a = []
                    t = hosts[x].split('-')
                    a += range(int(t[0]), int(t[1]) +1)
                    hosts[x] = a         

            for x in range(0, 4):
                if '*' in hosts[x]:
                    hosts[x] = list(range(1,256))

            for x in range(0, 4):
                if type(hosts[x]) is not list:
                    hosts[x] = [hosts[x]]
            
            for a in hosts[0]:
                for b in hosts[1]:
                    for c in hosts[2]:
                        for d in hosts[3]:
                            ip = '{}.{}.{}.{}'.format(a,b,c,d)
                            if run_tasks:
                                dict['host'] = ip
                                spawn_threads(dict)
                            else:
                                return

    except KeyboardInterrupt:        
        print('\n{} Stopping module...'.format(minus()))
        run_tasks = False
        executor.shutdown()

    except RuntimeError as error:
        raise RuntimeError(error)
    
    except Exception as error:
        raise('Error: {}'.format(error))

def search():
    # TODO add search tags for name, description, author, etc
    """
    Search usage:
    search "search term" - Search modules for search term
    """  
    global module_list
    rows = 0
    search_table = prettytable.PrettyTable()
    search_table.field_names = ['Index', 'Module', 'Name']
    search_table.align['Module'] = 'l'
    search_table.align['Name'] = 'l'
    module_list = []
    search_dict_base = {'name':''}

    if len(cmd_input) < 2:
        print(search.__doc__)

        for path in pathlib.Path(pathlib.Path() / 'modules').rglob('*.py'):
            search_result_duplicate = False                                         
            module = str(path)[8:-3].replace('/','.')
            lib_info = importlib.import_module('modules.{}'.format(module))
            lib_info = importlib.reload(lib_info)
            search_dict = {**search_dict_base, **lib_info.info()} 

            for key in search_dict:
                if not search_result_duplicate:
                    search_result_duplicate = True
                    module_list.append(module)
                    search_table.add_row([len(module_list), module, search_dict['name']])
                    rows += 1
        if rows > 0:
            print(search_table)
        else:
            print(minus() + ' No results found')
        

    else:
        for path in pathlib.Path(pathlib.Path() / 'modules').rglob('*.py'):
            search_result_duplicate = False                                         
            module = str(path)[8:-3].replace('/','.')
            lib_info = importlib.import_module('modules.' + module)
            search_dict = {**search_dict_base, **lib_info.info()} 
            for search_term in cmd_input[1:]:
                for key in search_dict:
                    if search_term.lower() in search_dict[key].lower() and not search_result_duplicate:
                        search_result_duplicate = True
                        module_list.append(module)
                        search_table.add_row([len(module_list), module, search_dict['name']])
                        rows += 1
        if rows > 0:
            print(search_table)
        else:
            print(minus() + ' No results found')

def set_option():
    """
    set usage:
    set "option" "value" - Set the value of an option
    """
    if len(cmd_input) < 3:
        print(set_option.__doc__)
        
        if lib:
            print('Current options:')
            options()
    else:
        dict[cmd_input[1]][0] = cmd_input[2]
        print('{} set to {}'.format(cmd_input[1],cmd_input[2]))

def setg_option():
    """
    setg usage:
    setg "option" "value" - Set the global value of an option
    """
    global_options_table = prettytable.PrettyTable()    
    global_options_table.field_names = ['Option', 'Value']
    global_options_table.align['Option'] = 'l'
    global_options_table.align['Description'] = 'l'
    
    if len(cmd_input) < 3:
        print(setg_option.__doc__)        

        if lib:
            print('Current global options:')
            for key in global_dict:
                global_options_table.add_row([key,global_dict[key][0]])
            print('\n{}\n'.format(global_options_table))
    else:
        global_dict[cmd_input[1]] = ['','']
        global_dict[cmd_input[1]][0] = cmd_input[2]
        dict[cmd_input[1]][0] = cmd_input[2]
        print('{} set to {}'.format(cmd_input[1],cmd_input[2]))

def spawn_threads(dict):
    global threads
    global run_tasks

    try:
        temp_dict = dict.copy()       
        threads.append(executor.submit(lib.run,temp_dict))
        if len(threads) >= int(dict['threads']):
            for module_dict in concurrent.futures.as_completed(threads):
                threads.remove(module_dict)
         
    except KeyboardInterrupt:        
        print('\n{} Stopping module...'.format(minus()))
        run_tasks = False
        executor.shutdown()

    except RuntimeError as error:
        raise RuntimeError(error)

    except Exception as error:
        raise Exception(error)

def unset_option():
    """
    unset usage:
    unset "option" - Set the option to the default value
    """
    try:
        if len(cmd_input) < 2:
            print(unset_option.__doc__)

            if lib:
                print('Current options:')
                options()
        else:
            lib_dict = lib.options()
            dict[cmd_input[1]] = lib_dict[cmd_input[1]]
            print('{} set to default value'.format(cmd_input[1]))
    except KeyError:
        raise KeyError('option {} doesn\'t exist'.format(cmd_input[1]))

def unsetg_option():
    """
    unsetg usage:
    unsetg "option" - Remove global option
    """
    if len(cmd_input) < 2:
        print(unsetg_option.__doc__)
    else:
        if global_dict[cmd_input[1]]:
            global_dict.pop(cmd_input[1])
            print('Global option ' + cmd_input[1] + ' removed')
        else:
            print('{} option {} doesn\'t exist'.format(minus(),dict[cmd_input[1]]))
    
def validate_dict(dict):
    try:
        if 'port' in dict:
            dict['port'] = int(dict['port'])
            if not (0 <= int(dict['port']) <= 65535):
                raise ValueError('invalid value for port')         
    except ValueError:
        raise ValueError('invalid value for port')

    try:
        if 'timeout' in dict:
            dict['timeout'] = int(dict['timeout'])
            if dict['timeout'] <= 0:
                raise ValueError('invalid value for timeout')         
    except ValueError:
        raise ValueError('invalid value for timeout')

    try:
        if 'threads' in dict:
            dict['threads'] = int(dict['threads'])
            if dict['threads'] <= 0:
                raise ValueError('invalid value for threads')         
    except ValueError:
        raise ValueError('invalid value for threads')
        
def validate_hosts(dict):
    hosts = []
    if not dict['host']:
        raise ValueError('invalid host value')
    host = dict['host']
    try:
        hosts = host.split('.')

        if 'file' in host:
            temp_list = open(host[5:],'r')
            for host in temp_list:
                host = host.strip()
                ipaddress.ip_address(host)
        
        else:
            for x in range(0, 4):    
                if ',' in hosts[x]:
                    num = hosts[x].split(',')
                    a = []
                    for numbers in num:
                        if '-' in numbers:
                            t = numbers.split('-')
                            if 0 <= int(t[0]) < int(t[1]) <= 255:
                                pass
                            else:
                                raise ValueError('invalid host value')
                            a += range(int(t[0]), int(t[1]) +1)
                        else:
                            a.append(int(numbers))
                    hosts[x] = a
                elif '-' in hosts[x]:
                    a = []
                    t = hosts[x].split('-')
                    if 0 <= int(t[0]) < int(t[1]) <= 255:
                        pass
                    else:
                        raise ValueError('invalid host value')
                    a += range(int(t[0]), int(t[1]) +1)
                    hosts[x] = a         

            for x in range(0, 4):
                if '*' in hosts[x]:
                    hosts[x] = list(range(1,256))

            for x in range(0, 4):
                if type(hosts[x]) is not list:
                    hosts[x] = [int(hosts[x])]

    except:
        raise ValueError('invalid host value')

def workspace():
    """
    Workspace usage:
    workspace -l - List all workspaces
    workspace -u X - Set active workspace to X
    workspace -a X - Create workspace with name X
    workspace -d X - Delete workspace with name X

    Note: Workspace names may only contain alphanumeric characters
    """
    
    workspace_table = prettytable.PrettyTable()
    workspace_table.field_names = ['Workspace']
    workspace_table.align['Workspace'] = 'l'
    
    try:
        if len(cmd_input) < 2:
            print(workspace.__doc__)            

        elif cmd_input[1] in ['-l']:
            for file in pathlib.Path(pathlib.Path.home() / '.tef' / 'databases').iterdir():
                workspace_table.add_row([file.name.split('.')[0]])
            print(workspace_table)
        
        elif cmd_input[1] in ['-a']:
            dict['database'] = cmd_input[2]
            dict['database'] = re.sub(r'\W+', '', dict['database'])
            init_database()

        elif cmd_input[1] in ['-d']:
            dict['database'] = cmd_input[2]
            dict['database'] = re.sub(r'\W+', '', dict['database'])
            file = pathlib.Path(pathlib.Path.home() / '.tef/databases/{}.db'.format(dict['database']))
            if file.exists():
                response = input('Are you sure you want to remove workspace {}? (y/N) '.format(cmd_input[2]))
                if response in ['y','yes']:
                    file.unlink()
                    print('Workspace {} deleted'.format(dict['database']))
            else:
                print('{} Workspace {} not found.'.format(minus(),cmd_input[2]))

        elif cmd_input[1] in ['-u']:
            tmp_database = cmd_input[2]
            tmp_database = re.sub(r'\W+', '', tmp_database)
            file = pathlib.Path(pathlib.Path.home() / '.tef/databases/{}.db'.format(tmp_database))
            if file.exists():
                dict['database'] = cmd_input[2]
            else:
                print('{} Workspace {} not found.'.format(minus(),tmp_database))
        
        else:
            print('Invalid workspace option')
    
    except IndexError:
        raise IndexError('missing value for {}'.format(cmd_input[1]))

def write_creds(dict):
    database_dict_base = {'host':'','port':'','protocol':'','username':'','password':'','notes':''}
    database_dict = {**database_dict_base, **dict}
    try:
        with sqlite3.connect(pathlib.Path.home() / '.tef/databases/{}.db'.format(dict['database'])) as connection:
            with connection as cursor:
                cursor.execute("REPLACE INTO creds (host, port, protocol, username, password, notes) values (?,?,?,?,?,?)", (database_dict['host'], database_dict['port'], database_dict['protocol'], database_dict['username'], database_dict['password'], database_dict['notes']))
        
    except Exception as e:
        print('Database error: {}'.format(e))

def write_database(dict):
    database_dict_base = {'host':'','port':'','protocol':'','module':'','output':''}
    database_dict = {**database_dict_base, **dict}
    try:
        with sqlite3.connect(pathlib.Path.home() / '.tef/databases/{}.db'.format(dict['database'])) as connection:
            with connection as cursor:
                cursor.execute("REPLACE INTO module_data (host, port, protocol, module, output) values (?,?,?,?,?)", (database_dict['host'], database_dict['port'], database_dict['protocol'], database_dict['module'], database_dict['output']))
            
    except Exception as e:
        print('Database error: {}'.format(e))

if __name__ == '__main__':
    if len(sys.argv) > 1:        
        if(sys.argv[1] in ['-c']):
            config = {}
            config_file = open(sys.argv[2],'r')
            for line in config_file:
                item = line.split('\t')
                config[item[0]] = item[1].strip()
            
            dict = config
            print(dict)
            init_database()     
            lib = importlib.import_module('modules.' + dict['module'])
            validate_dict(dict)
            validate_hosts(dict)
            with concurrent.futures.ThreadPoolExecutor(max_workers=int(dict['threads'])) as executor:
                run(dict)
            exit()
    try:
        pathlib.Path(str(pathlib.Path.home())+'/.tef').mkdir(parents=True, exist_ok=True)
        histfile = str(pathlib.Path.home()) + '/.tef/history'
        open(histfile,'a')
        readline.read_history_file(histfile)
        dict['database'] = 'default'
        init_database()
    except Exception as e:
        print('Error: {}'.format(e))
    
    

    while True:
        try:
            cmd_input = input('{}{} : tef > '.format(current_module,dict['database']))
            cmd_input = cmd_input.split()
            run_tasks = True

            if not cmd_input:
                pass

            elif cmd_input[0].lower() in ['creds']:
                creds()    

            elif cmd_input[0].lower() in ['db']:
                db()

            elif cmd_input[0].lower() in ['exit']:
                exit(0)

            elif cmd_input[0].lower() in ['help']:
                help()      

            elif cmd_input[0].lower() in ['info']:
                info()              

            elif cmd_input[0].lower() in ['options']:
                options()

            elif cmd_input[0].lower() in ['run']:
                if not lib:        
                    print('{} No module defined'.format(minus()))
                
                else:   
                    temp_dict = dict.copy()
                    for key in temp_dict:
                        if isinstance(temp_dict[key], list):
                            temp_dict[key] = temp_dict[key][0]
                    validate_dict(temp_dict)
                    validate_hosts(temp_dict)
                    with concurrent.futures.ThreadPoolExecutor(max_workers=int(temp_dict['threads'])) as executor:
                        run(temp_dict)   
                    threads = []

            elif cmd_input[0].lower() in ['search']:
                search()

            elif cmd_input[0].lower() in ['set']:
                set_option()

            elif cmd_input[0].lower() in ['setg']:
                setg_option()

            elif cmd_input[0].lower() in ['unset']:
                unset_option()

            elif cmd_input[0].lower() in ['unsetg']:
                unsetg_option()

            elif cmd_input[0].lower() in ['use']:
                use()

            elif cmd_input[0].lower() in ['workspace']:
                workspace() 

            else:
                print('Unknown command: ' + cmd_input[0].lower())

            readline.write_history_file(histfile)

        except KeyboardInterrupt as error:
            print('\n{} Type exit to quit'.format(minus()))

        except ValueError as error:
            print(minus() + ' ValueError: {}'.format(error))

        except RuntimeError as error:
            print(minus() + ' RuntimeError: {}'.format(error))
        
        except KeyError as error:
            print(minus() + ' KeyError: {}'.format(error))

        except IndexError as error:
            print(minus() + ' IndexError: {}'.format(error))

        except Exception as error:
            print(minus() + '   Error: {}'.format(error))
            print(traceback.print_exc())