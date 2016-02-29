#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from datetime import datetime
import socket
import sys
import getopt
import logging


class InternetAccess:
    REMOTE_SERVER = "www.google.com"

    @classmethod
    def is_connected(cls, server=None):
        try:
            if isinstance(server, list):
                hosts = []
                for srv in server:
                    host = socket.gethostbyname(srv)
                    s = socket.create_connection((host, 80), 2)
                    s.close()
                    hosts.append(srv)
                return True, 'CONNECTED {}'.format(hosts)
            else:
                host = socket.gethostbyname(cls.REMOTE_SERVER)
            s = socket.create_connection((host, 80), 2)
            s.close()
            return True, 'CONNECTED'
        except Exception as e:
            return False, e


def logger_conf():
    FORMAT = ''


if __name__ == '__main__':
    usage = '''
Check your connection!
============================
-h                              Help commands
-l  --loop                      Loop or not (Default: false)
-s  --sleep <sleep time>        Time to sleep betwen attempts (Default: 5s)
-d  --domains <single/list>     String of domains to be checked.
                                Domains must be separated by a semi-colon (;)
                                and must be a string. (Default: www.google.com)
-f  --log-file                  Log all messages to a file. User absolute path.
                                (Default: no log file)
'''

    options = 'hld:s:f:'
    long_options = ['help', 'loop', 'domains', 'sleep', 'log-file']
    try:
        opts, args = getopt.getopt(sys.argv[1:], options, long_options)
    except getopt.GetoptError as err:
        print(err)
        print(usage)
        sys.exit(2)

    loop = False
    log = False
    servers = None
    sleep_time = 5

    for opt, arg in opts:
        if opt in ('-l', '--loop'):
            loop = True
        elif opt in ("-h", "--help"):
            print(usage)
            sys.exit()
        elif opt in ("-d", "--domains"):
            if arg[-1] != ';':
                servers = arg.split(';')
            else:
                servers = arg[:-1].split(';')
        elif opt in ("-s", "--sleep"):
            sleep_time = int(arg)
        elif opt in ("-f", "--log-file"):
            log = True
            log_file = arg
        else:
            assert False, "unhandled option"

    if log:
        logging.basicConfig(format='[%(asctime)s][%(levelname)s]: %(message)s',
                            filename=log_file, level=logging.DEBUG,
                            datefmt='%Y/%m/%d %H:%M:%S')
    else:
        logging.basicConfig(format='[%(asctime)s][%(levelname)s]: %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S',
                            level=logging.INFO)

    while True:
        result, msg = InternetAccess.is_connected(servers)
        if result:
            logging.info(msg)
        else:
            logging.warning(msg)
        if not loop:
            break
        else:
            sleep(sleep_time)
