import socket,os

s = socket.socket()
host = ""
port = 60000

s.connect((host, port))
s.send("Hello server!")

while True:
    print('receiving data...')
    data = s.recv(1024)
    data=data.split()
    print "data",data

    if(data[0] == 'index'):
        lsResult=os.listdir('.')
        s.send(str(lsResult))
        break

    elif(data[0]=='hash' and data[1]=='verify'):
        filearg=data[2]
        filearg="cksum" + " " + filearg
        b=os.popen(filearg).read()
        if(b==data[3]):
            s.send("True")
        else:
            s.send("False")
        break
    else:
        f=open('testdata', 'wb')
        print 'file opened'
        print('data=%s', (data))
        if not data:
            break
            # write data to a file
        f.write(str(data))

        f.close()
print('Successfully get the file')
s.close()
print('connection closed')
