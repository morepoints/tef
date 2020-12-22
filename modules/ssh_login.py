#!/usr/bin/env python3
from ftplib import FTP
import paramiko
import tef

def info():
  search_dict = {
    'name':'SSH Login',
    'description':'SSH Login credential validator',
    'author':'morepoints'
  }
  return search_dict

def options():
  options_dict = {
    'host':['','Target host, see \'How to use tef\' in README.md for syntax options'],
    'port':[22,'Remote port to connect'],
    'threads':['','Number of threads'],
    'timeout':['3','Timeout in seconds'],
    'username':['anonymous','Login username'],
    'password':['anonymous@','Login password'],
    'verbose':['false','Output verbosity']
  }
  return options_dict

def run(dict):
  try:
    print(dict)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=dict['host'],port=dict['port'],username=dict['username'],password=dict['password'],timeout=dict['timeout'])
    ssh.close()
    print(tef.plus() + " Login valid - {} : {}".format(dict['username'], dict['password']))
    print()
    tef.write_database(dict)
    tef.write_creds(dict)

  except Exception as error:
    if dict['verbose'].lower() in ['true']:
      print("{} {} : {}".format(tef.minus(),dict['host'], error))
    ssh.close()
    