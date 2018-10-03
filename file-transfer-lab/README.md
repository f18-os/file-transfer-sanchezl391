# TCP Text File Transfer
## What this program does and how it works
This program has a server(fileServer.py), client(fileClient.py), and proxy(stammerProxy.py). The client sends a text file from the client to the server in 100 byte increments. For every client, a child process will handle the connection and trasferring of data. The proxy can be used to simulate stammering of bytes and redirecting data from one address to another.
The server must be started before the client because the client will attempt to connect to the server. 
## Server
### Commands
#### Starting up Server:
- Starting server with specified port:
`$ python3 fileServer.py 50001 `
- By Default, if a port argument is not given then it is defaulted to port=50001
## Client
### Commands
#### Starting up Client:
- `$ python3 fileClient.py 127.0.0.1 50000 test.txt `
- By Default, if address, port, and file arguments are not given, then they are defaulted to address=127.0.0.1, port=50000, test.txt


