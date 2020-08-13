#!/usr/bin/python
import socket

RHOST = "192.168.56.101"    # mind to change that :-)
RPORT = 31337               # mind to change that :-)

# establish a TCP connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

# say hello
buf = ""
buf += "Hello, Python Script here"
buf += "\n"

# send the message via socket
s.send(buf)

# print out our message
print "Sent: {0}".format(buf)

# receive what shall be received from the socket
data = s.recv(1024)

# print out what was received
print "Received: {0}".format(data)
