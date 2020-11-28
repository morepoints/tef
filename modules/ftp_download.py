#!/usr/bin/env python3
from ftplib import FTP
from pathlib import Path
import io
import traceback
import tef

def info():
  search_dict = {
    'name':'FTP File Download',
    'description':'Downloads a specified FTP file',
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
    'file':['','File name/path to download'],
    'verbose':['false','Output verbosity']
  }
  return options_dict

def run(dict):
  try:
    temp = io.BytesIO()
    with FTP() as ftp:
      ftp.connect(host=dict['host'], port=dict['port'], timeout=int(dict['timeout']))
      with temp as file:
        ftp.login()
        ftp.retrbinary('RETR ' + dict['file'], file.write)
        if file:
          p = Path.home() / '.tef' / 'loot' / dict['host']
          f = False
          if Path.is_file(p / Path(dict['file']).name):
            count = 1
            while not f:
              if Path.is_file(Path(str(p / Path(dict['file']).name) + '.' + str(count))):
                f = False
                count += 1
              else:
                f = str(p / Path(dict['file']).name) + '.' + str(count)          
          else:
            f  = p / Path(dict['file']).name
          if not p.is_dir():
            p.mkdir()
          download = open(f, 'wb')
          download.write(file.getvalue())
          download.close()
          print('File {} successfully downloaded to {}'.format(dict['file'], p / f))
        else:
          print('File {} empty or does not exist'.format(dict['file']))

  except Exception as error:
    if dict['verbose'].lower() in ['true']:
      print('{} {} : {}'.format(tef.minus(),dict['host'],error))
