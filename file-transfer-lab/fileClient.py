#! /usr/bin/env python3

# Echo client program
import socket, sys, re, params, os.path, base64

from framedSock import framedSend, framedReceive

# check for server's address and port arguments
try:
    address = sys.argv[0]
    port = sys.argv[1]
    inputFileName = sys.argv[2]
except IndexError:
    address = "127.0.0.1"
    port = "50001"
    inputFileName = "pdf.pdf"

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

# Read from a file
# with open(inputFileName) as f:
#     read_data = f.read()
f = open("pdf.pdf", "rb")
# mssgInBytes = f.read()
# stringBytes = bytearray(string, 'utf8')

# Send mssg
# Control Flow of transfer
# mssg = inputFileName + ' ' + read_data
# for i in range(200):
#     mssg+='a'

# print('Sending ' + mssg)

# byteMssg = bytearray(mssg, "utf8")

# while(True):
#     try:
#         tmpMssg = mssgInBytes[0:100] 
#         framedSend(s, tmpMssg, debug)
#         mssgInBytes = mssgInBytes[100:] # reducing # of bytes
#         print("received:", framedReceive(s, debug))
#     except IndexError:
#         exit(1)
mssgInBytes = f.read(100)
while(mssgInBytes):
    try:
        print('in loops')
        framedSend(s, mssgInBytes, debug)
        # print("received:", framedReceive(s, debug))
        mssgInBytes = f.read(100)
    except IndexError:
        exit(1)
    