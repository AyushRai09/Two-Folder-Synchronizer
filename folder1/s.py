import socket,os
foo=0
arr=[[foo for i in range(100)] for j in range(100)]

def replyToCalledLsFromClient():
        lsResult=os.popen('ls -l').read()
        conn.send(str(lsResult))
        lsResult=lsResult.split('\n')
        i=0
        del(lsResult[len(lsResult)-1]) #delte the last null character.
        for iterator in lsResult:
            if(iterator.find('total')==-1):
                arr[i]=iterator.split()
                i=i+1
        return

def replyToCalledHashVerifyFromClient(filename, filehash):
        filearg=filename
        filearg="cksum" + " " + filearg
        b=os.popen(filearg).read()
        b=b.split()
        # print "b:",b
        if(len(b)==0): #case when there is no file which the user has asked to verify the hash for.
            conn.send("No such file present.")
        elif(int(b[0])==int(filehash)):
            conn.send("No changes made to the file.")
        else:
            lsResult=os.popen('ls -l').read()
            lsResult=lsResult.split('\n')
            i=0
            del(lsResult[len(lsResult)-1]) #delte the last null character.
            for iterator in lsResult:
                if(iterator.find('total')==-1):
                    arr[i]=iterator.split()
                    i=i+1
            string=""
            i=0
            while(i<100):
                if(arr[i][8]!=0 and arr[i][8]==filename and arr[i][5]!=0 and  arr[i][6]!=0 and arr[i][7]!=0):
                    string=string + arr[i][8] + " " + arr[i][5] + " " + arr[i][6] + " " + arr[i][7] + " "
                i=i+1
            conn.send(string)
        return


def DownloadRequestFromClientTCP(filename):
        f = open(filename,'rb')
        l = f.read(1024)
        while (l):
           conn.send(l)
           print('Sent ',repr(l))
           l = f.read(1024)
        f.close()
        print('Done sending')

def DownloadRequestFromClientUDP(filename):
        f = open(filename,'rb')
        l = f.read(1024)
        while (l):
           s2.sendto(l,(host,port2))
           print('Sent ',repr(l))
           l = f.read(1024)
        f.close()
        print('Done sending')

port = 60000
port2=50000
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = ""

s2=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


s.bind((host, port))
s.listen(5)

print 'Server listening....'

conn, addr = s.accept()
while True:
    print 'receiving.......'
    data=conn.recv(1024)
    originalData=data
    data=data.split()
    print "data:",data
    if(data[0] == 'index'):
        replyToCalledLsFromClient()

    elif(data[0]=='hash' and data[1]=='verify'):
        replyToCalledHashVerifyFromClient(data[2],data[3])

    elif(data[0]=='download' and data[1]=='TCP' and len(data)==3):
        DownloadRequestFromClientTCP(data[2])

    elif(data[0]=='download' and data[1]=='UDP' and len(data)==3):
        DownloadRequestFromClientUDP(data[2])

s.shutdown(socket.SHUT_RDWR)
s.close()
