import socket
from threading import Thread
import os
from pathlib import Path

host = '127.0.0.1'
port = 9000
BUFFERSIZE = 1024
serverpath = './ServerFolder/'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

def retCon():
    s.listen(5)
    print "Waiting for connection"
    while True:
        connection, addr = s.accept()
        print "Connected to "+str(addr[0])+":"+str(addr[1])
        data = connection.recv(BUFFERSIZE)
        print data[:5]
        if data[:2] == '1':
            thread = Thread(target = DownloadFile,args = ("retrThread",connection))
            thread.start()
        if data[:2] == '2':
            thread = Thread(target = UploadFile,args = ("retrThread",connection))
            thread.start()
    s.close()

def DownloadFile(name, sock):
    sock.send('down')
    filename = sock.recv(BUFFERSIZE)
    filepath = Path(filename)
    nama=os.path.join(serverpath,filename)
    if os.path.isfile(nama):
        print "File is exist"
        sock.send("EXISTS " + str(os.path.getsize(nama)))
        userResponse = sock.recv(BUFFERSIZE)
        if userResponse[:2] == 'OK':
            with open(nama,'rb') as f:
                bytesToSend = f.read(BUFFERSIZE)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(BUFFERSIZE)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR")
        sock.close()
    sock.close()

def UploadFile(name, sock):
    sock.send('up')
    dirname = sock.recv(BUFFERSIZE)
    nama=os.path.join(serverpath,dirname)
    if os.path.exists(nama):
        print "File is exist"
        sock.send('OK')
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
        sock.send("ERR")
        sock.close()
    sock.close()

def main():
    while True:
        retCon()

if __name__ == '__main__':
    main()