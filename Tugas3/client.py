import socket
from threading import Thread
import os
from pathlib import Path

host = '127.0.0.1'
port = 9000
BUFFERSIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (host,port)
s.connect(server_address)
clientpath = './ClientFolder/'

print "1.Download"
print "2.Upload"

inputmenu = raw_input()
s.send(inputmenu)
d = s.recv(BUFFERSIZE)
if d[:4] == 'down':
    print "Input server file path (Cancel : $q)"
    filename = raw_input()
    s.send(filename)
    d = s.recv(BUFFERSIZE)
    if d[:6] == "EXISTS":
        filesize = long(d[6:])
        message = raw_input("File exist, "+str(filesize)+" Bytes, download? (Y/N)")
        if message == 'Y' or message == 'y':
            s.send('OK')
            filepath = Path(filename)
            namafile = filepath.name
            nama=os.path.join(clientpath,namafile)
            f = open(nama,'wb')
            data = s.recv(BUFFERSIZE)
            totalRecv = len(data)
            f.write(data)
            while totalRecv < filesize:
                data = s.recv(BUFFERSIZE)
                totalRecv += len(data)
                f.write(data)
        print "download success"

    else:
        print "file or directory not found"
if d[:4] == 'up':
    print "Input client file path (Cancel : $q)"
    filename = raw_input()
    filepath = Path(filename)
    namafile = filepath.name
    nama=os.path.join(clientpath,namafile)
    if os.path.isfile(nama):
        print "File is exist"
        # sock.send("EXISTS " + str(os.path.getsize(nama)))
        # userResponse = sock.recv(BUFFERSIZE)
        # if userResponse[:2] == 'OK':
        #     with open(nama,'rb') as f:
        #         bytesToSend = f.read(BUFFERSIZE)
        #         sock.send(bytesToSend)
        #         while bytesToSend != "":
        #             bytesToSend = f.read(BUFFERSIZE)
        #             sock.send(bytesToSend)
    else:
        print "File or path not found"
        s.close()
    s.close()