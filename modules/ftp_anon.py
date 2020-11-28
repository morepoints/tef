#!/usr/bin/env python3
from ftplib import FTP
import tef
import re

def info():
  search_dict = {
    'name':'Anonymous FTP Login',
    'description':'Anonymous FTP Login checker',     
    'author':'morepoints'
  }
  return search_dict

def options():
  options_dict = {
    'host':['','Target host, see \'How to use tef\' in README.md for syntax options'],
    'port':[21,'Remote port to connect'],
    'threads':['','Number of threads'],
    'timeout':['3','Timeout in seconds'],
    'verbose':['false','Output verbosity']
  }
  return options_dict

def run(dict):
  try:
    dir = []
    output = []
    with FTP() as ftp:
      ftp.connect(host=dict['host'], port=dict['port'], timeout=int(dict['timeout']))
      ftp.login()
      ftp.dir(dir.append)
      if dir:
        output.append('ftp://' + dict['host'] + ' anon')
        for line in dir:
          line = re.sub(r'[\x00-\x1f\x7f-\x9f]', '?', line)
          output.append(line)
        output.append('')
        print('\n'.join(output))
        print()
        dict['output'] = '\n'.join(output)
        dict['username'] = 'anonymous'
        dict['password'] = 'anonymous@'
        tef.write_database(dict)
        tef.write_creds(dict)

  except Exception as error:
    if dict['verbose'].lower() in ['true']:
      print("{} {} : {}".format(tef.minus(),dict['host'], error))

