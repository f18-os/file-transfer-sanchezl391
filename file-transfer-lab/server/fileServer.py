#! /usr/bin/env python3

import sys
sys.path.append("../") 
sys.path.append('../../lib') # params

import re, socket, params, os.path

# Check for server listen port
try:
    listenPort = sys.argv[0]
except IndexError:
    listenPort = int("50001")
debug = 0

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

# Listens for infinitely many connections
while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    # Create a child process for handling client. 
    if not os.fork(): # os.fork() == 0 when it is a child process
        print("new child process handling connection from", addr)
        fileName = ''
        mssg = ''
        while True: # Loops until whole message is received in 100 byte pieces.
            payload = framedReceive(sock, debug)
            if debug: print("rec'd: ", payload)
            if not payload:
                break
            mssg += payload.decode('utf-8')
            if(not fileName): # Get file name
                fileName = mssg.split(" ", 1)[0]
                fileNameLen = len(fileName)
                mssg = mssg[fileNameLen + 1:]
            payload += b"!"             # make emphatic!
            framedSend(sock, payload, debug)

        # Creating file on the server with contents of message
        if os.path.isfile(fileName):
            print("The file already exists on the server! Another file will not be created.")
        else:
            if fileName:    
                f = open(fileName, "w")
                f.write(mssg)
                f.close()
            else:
                print('The file you are trying to transfer is empty. Cancelling transfer.')