# Socket Programming
## Simple Socket Server and Client
Client communicates with an echo server using Python's socket module. Data is passed over the
network to the server from the client, and the server echoes back the original message.

## Requirements
The server-client pair was written using Python 3. The following modules were used, but should be
part of any standard Python installation:
```
    math
    socket
```

## Using the System
The server should be initialized first by calling it through the Python interpreter.
```
    $ python3 server.py
```
This will set up the server, and it will begin running in the background.

Once the server is running, a connection can be established to it using the client Python script.
```
    $ python3 client.py
```
If a connection is successfully established, text can be typed into the console, which will be
passed to the server and echoed back to the client. To shutdown the client, "quit" can be typed into
the text prompt.

Shutting down the server will require issuing a keyboard interrupt using CTRL+C. The server may not
shut down immediately because the `recv` call locks it, but the next time a client tries to connect,
the program will stop.

## Modifying IPs and Ports
The IP and port values that the system uses are hard-coded into the scripts. Each file has a `HOST`
and `PORT` constant at the top of the file that can be modified before running them to change where
the server and client interact.
