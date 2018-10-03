#! /usr/bin/env python3

import sys
sys.path.append('../../lib') # params
sys.path.append('../') # framedSock
import socket, re, params, os.path, base64

from framedSock import framedSend, framedReceive

# check for server's address and port arguments
try:
    serverHost = sys.argv[0]
    serverPort = int(sys.argv[1])
    inputFileName = sys.argv[2]
except IndexError:
    serverHost = "127.0.0.1"
    serverPort = int("50000")
    inputFileName = "test.txt"

debug = 0

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


try:
    f = open(inputFileName, "r")
    originalMssg = f.read(100) # read 100 bytes from file at a time
    if(not len(originalMssg)):
        print("The file you are trying to transfer is empty. Cancelling transfer.")
    else:
        mssg = inputFileName + ' ' + originalMssg
        mssgBytes = mssg.encode()
        while True: # Send bytes in 100 byte pieces until there is no more to send
            if mssg == '':
                break
            framedSend(s, mssgBytes, debug) # send mssg
            print("received:", framedReceive(s, debug))
            mssg = f.read(100)
            mssgBytes = mssg.encode()

        f.close()
except FileNotFoundError:
    print('Error. You did not specify a file to transfer or it wasnt found')
