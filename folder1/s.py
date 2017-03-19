import socket,os

port = 60000
s = socket.socket()
host = ""

s.bind((host, port))
s.listen(5)

print 'Server listening....'

while True:
    command = raw_input("prompt:$ ")

    arg=command.split()
    print "arg:",arg[0]
    conn, addr = s.accept()
    print 'Got connection from',addr
    data = conn.recv(1024)
    data=data.split()
    print data
    print('Server received', repr(data))

    if(arg[0] == 'index'):
        conn.send(command)
        lsResult=conn.recv(1024)
        print lsResult

    elif(arg[0] =='hash' and arg[1] =='verify'):
        filearg=arg[2]
        filearg="cksum"+" " + filearg
        b=os.popen(filearg).read()
        command=command + " " + b
        conn.send(command)
        result=conn.recv(1024)
        print result

    else:
        print "arg in the else condition:",arg
        f = open(arg[0],'rb')
        l = f.read(1024)
        while (l):
           conn.send(l)
           print('Sent ',repr(l))
           l = f.read(1024)
        f.close()

        print('Done sending')
    conn.send('Thank you for connecting')
    conn.close()
s.close()
