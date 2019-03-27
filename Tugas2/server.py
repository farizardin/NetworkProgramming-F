from threading import Thread
import socket
import os
import time
import glob
from pathlib import Path

SERVER_IP="127.0.0.1"
SERVER_PORT = 10000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

SOURCE = "./serverfile/"
NAMAFILE = glob.glob("./serverfile/*.jpg")

def getRequest():
  print "Waiting for request"
  while True:
    data , addr =sock.recvfrom(1024)
    data_to_string = str(data)
    if(data_to_string[:3] == "REQ"):
      time.sleep(10)
      thread = Thread(target = setImage,args = (addr))
      thread.start()
      print "Sending file to "+str(addr[0])+":"+str(addr[1])

def setImage(ip , port):
  addr = (ip,port)
  for x in NAMAFILE:
    time.sleep(10)
    gambar = Path(x)
    namagambar = gambar.name
    kirim(namagambar,addr)
  sock.sendto("CLOSE".ljust(1024),addr)

def kirim(imgname,addr):
  nama=os.path.join(SOURCE, imgname)
  fp = open(nama,'rb')
  paket = fp.read()
  terkirim = 0
  fp.close()
  sock.sendto(("START "+imgname).ljust(1024),addr)
  panjangpkt = len(paket)
  iterasi = (panjangpkt/1024)
  for i in range(iterasi+1):
    data=[]
    if (i+1)*1024 > panjangpkt:
      data = paket[i*1024:panjangpkt]
      terkirim = terkirim+len(data)
      data.ljust(1024)
    else:
      data = paket[i*1024:(i+1)*1024]
      terkirim = terkirim+len(data)
    sock.sendto(data,addr)
  print "Sending "+str(imgname)+" from "+str(nama)+" to "+str(addr[0])+":"+str(addr[1])
  sock.sendto(("File has been sent "+ imgname).ljust(1024),addr)

while True:
  getRequest()