import socket,os

def callLsOnClient(command):
    conn.send(command)
    lsResult=conn.recv(1024)
    print lsResult

def hashVerifyOnClient(filename, command):
        filearg=filename
        filearg="cksum"+" " + filename
        hashValue=os.popen(filearg).read()
        command=command + " " + hashValue
        conn.send(command)
        result=conn.recv(1024)
        print result

def DownloadRequestFromClient(filename):
        f = open(filename,'rb')
        l = f.read(1024)
        while (l):
           conn.send(l)
           print('Sent ',repr(l))
           l = f.read(1024)
        f.close()
        print('Done sending')

port = 60000
s = socket.socket()
host = ""

s.bind((host, port))
s.listen(5)

print 'Server listening....'

conn, addr = s.accept()
while True:
    command = raw_input("prompt:$ ")

    arg=command.split()
    # print "arg:",arg[0]
    # print 'Got connection from',addr
    # data = conn.recv(1024)
    # data=data.split()
    # print data
    # print('Server received', repr(data))

    if(arg[0] == 'index'):
        callLsOnClient(command)

    elif(arg[0] =='hash' and arg[1] =='verify'):
        hashVerifyOnClient(arg[2],command)

    else:
        DownloadRequestFromClient(arg[0])

    # conn.send('Thank you for connecting')
    # conn.close()
s.close()
