# TCP Text File Transfer
## What this program does and how it works
This program has a server, client, and proxy. The client sends a text file from the client to the server in 100 byte increments. The proxy can be used to simulate stammering of bytes and redirecting data.
The server must be started before the client because the client will attempt to connect to the server. 
## Server
### Commands
#### Starting up Server:
By Default, if port is not given then it is defaulted to port=50001
Starting server with specified port:
`$ python3 fileServer.py 50001 `
## Client
### Commands
#### Starting up Client:
By Default, if address, port, and file are not given, then they are defaulted to address=127.0.0.1, port=50000, test.txt
`$ python3 fileClient.py 127.0.0.1 50000 test.txt `

