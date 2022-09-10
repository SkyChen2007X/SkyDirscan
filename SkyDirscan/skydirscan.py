help = '''
Author: Sky_Chen

Name: SkyDirScan

usage: skydirscan.py [-h] [-url URL] [-timeout TIMEOUT] [-thread THREAD]
                     [-status STATUS] [-file FILE] [-proxy PROXY]

A tool to scan the dir from the target

optional arguments:
  -h, --help            show this help message and exit
  -url URL, -u URL      The url to scan
  -timeout TIMEOUT      Set the timeout
  -thread THREAD        Set the thread(max 1000)
  -status STATUS, -s STATUS
                        Set the right status
  -file FILE, -f FILE   An option for your dictionary
  -proxy PROXY, -p PROXY
                        Set the proxies
'''

import argparse
import os
from sys import exit
from colorama import init, Fore
from libs.scan import Scan

def main():
    init(autoreset = True)
    
    icon = '''

 (           (                              
 )\ )   )    )\ )                           
(()/(( /((  (()/( (  (             )        
 /(_))\())\ )/(_)))\ )(  (   (  ( /(  (     
(_))((_)(()/(_))_((_|()\ )\  )\ )(_)) )\ )  
/ __| |(_)(_))   \(_)((_|(_)((_|(_)_ _(_/(  
\__ \ / / || | |) | | '_(_-< _|/ _` | ' \)) 
|___/_\_\\_,  |___/|_|_| /__|__|\__,_|_||_|  
         |__/                               
                                                                               

Author: Sky Chen
Name: SkyDirscan
        '''


    print(Fore.GREEN + icon)
    temp_path = __file__.split('\\')
    temp_path.pop()
    path = '/'.join(temp_path)
    
    
    p = argparse.ArgumentParser(description = 'A tool to scan the dir from the target')
    p.add_argument('-url','-u', type = str, help = 'The url to scan')
    p.add_argument('-timeout', type = int, help = 'Set the timeout')
    p.add_argument('-thread', type = int, help = 'Set the thread(max 1000)')
    p.add_argument('-status', '-s', type = int, help = 'Set the right status')
    p.add_argument('-file', '-f', type = str, help = 'An option for your dictionary')
    p.add_argument('-proxy', '-p', type = str, help = 'Set the proxies')
    args = p.parse_args()
    
    url = args.url
    timeout = args.timeout
    thread = args.thread
    status = args.status
    file = args.file
    proxy = args.proxy

    scan = Scan(help, path)
    scan.check_options(url, thread, file, timeout, proxy, status)
    scan.scan()

if __name__ == '__main__':
    main()
    














        
