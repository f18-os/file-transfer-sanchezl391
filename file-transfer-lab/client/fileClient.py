#! /usr/bin/env python3

import sys
sys.path.append('../../lib') # params
sys.path.append('../') # framedSock
import socket, re, params, os.path, base64

from framedSock import framedSend, framedReceive

# check for server's address and port arguments
try:
    address = sys.argv[0]
    port = sys.argv[1]
    inputFileName = sys.argv[2]
except IndexError:
    address = "127.0.0.1"
    port = "50001"
    inputFileName = "test.txt"

switchesVarDefaults = (
    (('-s', '--server'), 'server', address  + ':' + port),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

f = open(inputFileName, "r")

mssg = inputFileName + ' ' + f.read(100)
mssgBytes = mssg.encode("unicode_escape")
while True:
    try:
        if mssg == '':
            break
        framedSend(s, mssgBytes, debug)
        print("received:", framedReceive(s, debug))
        mssg = f.read(100)
        mssgBytes = mssg.encode("unicode_escape")
        
    except IndexError:
        print("Error")
        exit(1)

f.close()