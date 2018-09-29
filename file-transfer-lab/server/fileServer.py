#! /usr/bin/env python3

import sys
sys.path.append("../") 
sys.path.append('../../lib') # params

import re, socket, params

# Check for server listen port
try:
    port = sys.argv[0]
except IndexError:
    port = "50001"

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', int(port)),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
)

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

sock, addr = lsock.accept()

print("connection rec'd from", addr)


from framedSock import framedSend, framedReceive


# Get mssg
fileName = ''
mssg = ''
while True:
    payload = framedReceive(sock, debug)
    if debug: print("rec'd: ", payload)
    if not payload:
        break
    mssg += payload.decode('utf-8').replace("\\n", "\n")
    print('mssg inside loop: ' + mssg)
    if(not fileName):
        fileName = mssg.split(" ", 1)[0]
        fileNameLen = len(fileName)
        mssg = mssg[fileNameLen + 1:]
    payload += b"!"             # make emphatic!
    framedSend(sock, payload, debug)
    
print('mssg outside loop: ' + mssg)
f = open(fileName, "w")
f.write(mssg)
f.close()
sock.close()
lsock.close()