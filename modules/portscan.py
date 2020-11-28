#!/usr/bin/env python3
import tef
import socket
import time

def info(): 
    search_dict = {
        'name':'TCP/UDP port scanner',
        'description':'This is a simple TCP/UDP port scanner',
        'author':'morepoints'
    }
    return search_dict

def options(): 
    options_dict = {
        'host':['','Target host, see \'How to use tef\' in README.md for syntax options'],
        'ports':['', 'Port or port range. Commas and dashes allowed for ranges'],
        'threads':['','Number of threads'],
        'protocol':['tcp','IP protocol'],
        'verbose':['false','Output verbosity']
    }
    return options_dict

def run(dict):
    sock_type = ''
    ports = dict['ports']
    try:
        if dict['protocol'].lower() in ['tcp']:
            sock_type = socket.SOCK_STREAM
        elif dict['protocol'].lower() in ['udp']:
            sock_type = socket.SOCK_DGRAM
        
        if ',' in ports:
            comma_split = ports.split(',')
            a = []
            for numbers in comma_split:
                if '-' in numbers:
                    t = numbers.split('-')
                    if 0 <= int(t[0]) < int(t[1]) <= 65535:
                        pass
                    else:
                        raise ValueError('invalid port value')
                    a += range(int(t[0]), int(t[1]) +1)
                else:
                    a.append(int(numbers))
                ports = set(a)
        elif '-' in ports:
            a = []
            t = ports.split('-')
            if 0 <= int(t[0]) < int(t[1]) <= 65535:
                pass
            else:
                raise ValueError('invalid port value')
            a += range(int(t[0]), int(t[1]) +1)
            ports = set(a)
        else:
            ports = set([int(dict['ports'])]) # Typing lul

        print(ports)
        for port in ports:
            print(port)
            time.sleep(.5)
            with socket.socket(socket.AF_INET, sock_type) as s:
                result = s.connect_ex((dict['host'], port))
                if result == 0:
                    print('{} {} : {} OPEN'.format(tef.plus(), dict['host'], port))

    except KeyboardInterrupt:
        return

    except Exception as error:        
        if dict['verbose'].lower() in ['true']:
            print("{} {} : {}".format(tef.minus(),dict['host'], error))