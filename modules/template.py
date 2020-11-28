#!/usr/bin/env python3
import tef

def info(): # Required function. General module information that will be used for info and search functions. See 'How to use tef' in README.md for more info
    search_dict = {
        'name':'TEF module template',
        'description':'This is a more verbose description of the module.',
        'author':'author name'
    }
    return search_dict

def options(): # Required function. Variables you want to use in your module. See 'How to use tef' in README.md for more info
    options_dict = {
        'host':['','Target host, see \'How to use tef\' in README.md for syntax options'],
        'port':[2, 'This is a port'],
        'threads':['','Number of threads'],
        'test_option':['','This is a test option'],
        'verbose':['false','Output verbosity']
    }
    return options_dict

def run(dict): # Required function. Main code block that will be executed. See 'How to use tef' in README.md for more info
    output = []
    try:
        print('Hello World!')
        print('The host for the module is {}'.format(dict['host']))
        print('{} Oh no!'.format(tef.minus()))
        print('{} Hurray!'.format(tef.plus()))
        print('Someone put {} for the test option, saving it to module output'.format(dict['test_option']))
        output.append(dict['test_option'])
        print('Writing test_option string to database...')
        dict['output'] = '\n'.join(output)
        tef.write_database(dict)

        '''
        If you want to write the returned information to the database:

        tef.write_database(dict)
        tef.write_creds(dict)
        '''
    except Exception as error:
        if dict['verbose'].lower() in ['true']:
            print("{} {} : {}".format(tef.minus(),dict['host'], error))