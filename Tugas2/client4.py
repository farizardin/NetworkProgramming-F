import socket
import time
import os

SERVER_IP="127.0.0.1"
SERVER_PORT= 10000

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

ditulis=0
folder="./folderclient4/"
sock.sendto("REQ",(SERVER_IP,SERVER_PORT))
print 'Melakukan Request ke Server'

while True:
  data,addr=sock.recvfrom(1024)
  if data[:5] == "START":
    namafile=data[6:].replace(" ","")
    nama=os.path.join(folder,namafile)
    fp=open(nama,'wb+')
    ditulis=0
    print "Receive "+namafile
  elif data[:3]=="END":
    print >> namafile+" Received"
    fp.close()
  elif data[:5]=="CLOSE":
    print "Close Connection"
    break
  else:
    fp.write(data)
    ditulis=ditulis+len(data)
print "All request done"