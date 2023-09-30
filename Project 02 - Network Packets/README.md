# Network Packets
## Network Communication Using Packets and Headers
Client and server communicate over a network using packets that are composed of both a header and
payload. This builds on the concepts introduced as part of the
[socket program](<../Project 01 - Socket Programming/>).

## Requirements
The server and client require Python 3 to be ran. The following modules were used, but these
should already be a part of a standard Python installation.
```
    argparse (client only)
    math
    socket
    struct
```

## Using the System
The server can be initialized by simply calling the Python interpreter from the command line.
```
    $ python3 server.py
```
A message should be printed once it is set up and running.

The client takes a number of arguments, with some of them being required.
```
    python3 client --version <header_version> --header_length <header_length> --service_type <service_type_enum> --payload <transmission_data> [options]
    Options:
        --host          IP address of target remote server
        --port          communication port for server
    Service Type Options:
        1               payload is a 4-byte integer
        2               payload is a 4-byte float
        3               payload is a variable-length string
```
Any argument not listed under "Options" is requred for the program to function properly.

The client should send the payload provided to it, receive the echo from the server, and then exit.
The server is designed to run without interruption, and shutting it down requires issuing a keyboard
interrupt using CTRL+C. If this does not immediately shut it down, the next time a client tries to
connect will cause the connection to fail and the server to stop. This is due to the `recv` call
locking the server.
