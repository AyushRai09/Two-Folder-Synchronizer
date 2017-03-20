import socket,os
foo=0
arr=[[foo for i in range(100)] for j in range(100)]
def callLsOnClient(command):
    conn.send(command)
    lsResult=conn.recv(1024)
    lsResult=lsResult.split('\n')
    i=0
    del(lsResult[len(lsResult)-1]) #delte the last null character.
    print "filename", "Time last modified"
    for iterator in lsResult:
        if(iterator.find('total')==-1):
            arr[i]=iterator.split()
            print arr[i][8], arr[i][5], arr[i][6], arr[i][7]
            i=i+1

def hashVerifyOnClient(filename, command):
        filearg=filename
        filearg="cksum"+" " + filename
        hashValue=os.popen(filearg).read()
        command=command + " " + hashValue
        conn.send(command)
        result=conn.recv(1024)
        if(result=="No changes made to the file."):
            print result
        else:
            result=result.split()
            print "The file was modified since last access:"
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            i=0
            while(i<len(result)):
                print result[i], result[i+1], result[i+2], result[i+3]
                i=i+4
        return

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

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
s.shutdown(socket.SHUT_RDWR)
s.close()
