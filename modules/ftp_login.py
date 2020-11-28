#!/usr/bin/env python3
from ftplib import FTP
import tef

def info():
  search_dict = {
    'name':'FTP Login',
    'description':'FTP Login credential validator',
    'author':'morepoints'
  }
  return search_dict

def options():
  options_dict = {
    'host':['','Target host, see \'How to use tef\' in README.md for syntax options'],
    'port':[21,'Remote port to connect'],
    'threads':['','Number of threads'],
    'timeout':['3','Timeout in seconds'],
    'username':['anonymous','Login username'],
    'password':['anonymous@','Login password'],
    'verbose':['false','Output verbosity']
  }
  return options_dict

def run(dict):
  try:
    with FTP(host=dict['host'], port=dict['port'], user=dict['username'],passwd=dict['password']) as ftp:
      ftp.connect(host=dict['host'], port=int(dict['port']), timeout=int(dict['timeout']))
      ftp.login()
      print("{} Login valid - {} : {}".format(tef.plus(), dict['username'], dict['password']))
      print()
      tef.write_database(dict)
      tef.write_creds(dict)

  except Exception as error:
    if dict['verbose'].lower() in ['true']:
      print("{} {} : {}".format(tef.minus(),dict['host'], error))