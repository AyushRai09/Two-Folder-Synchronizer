import socket,os,datetime
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

def replyToCalledHashVerifyFromClient(filename, sentFileMonth, sentFileDay, sentFileTime, filehash):
        filearg="cksum" + " " + filename
        b=os.popen(filearg).read()
        b=b.split() #b[0] contains the hashValue of the file at the server.
        filearg="ls -l" + " " + filename
        lsResult=os.popen(filearg).read()
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
            if(arr[i][8]==filename):
                timestamp1=arr[i][5] + " " + arr[i][6] + " " + arr[i][7] + " " + "2017"
                timestamp2=sentFileMonth + " " + sentFileDay + " " + sentFileTime + " " + "2017"
                print "timestamp1:",timestamp1, "timestamp2:",timestamp2
                t1 = datetime.datetime.strptime(timestamp1, "%b %d %H:%M %Y")
                t2 = datetime.datetime.strptime(timestamp2, "%b %d %H:%M %Y")

                if(max(t1,t2)==t1):#Server's file is the latest file.
                    string=arr[i][8] + " " + arr[i][5] + " " + arr[i][6] + " " + arr[i][7]
                elif(max(t1,t2)==t2):#Client's file is the latest file.
                    string=filename+" " +sentFileMonth + " " + sentFileDay + " " + sentFileTime
                break
            i=i+1

        # while(i<100):
        #     if(arr[i][8]!=0 and arr[i][8]==filename and arr[i][5]!=0 and  arr[i][6]!=0 and arr[i][7]!=0):
        #         string=string + arr[i][8] + " " + arr[i][5] + " " + arr[i][6] + " " + arr[i][7] + " "
        #     i=i+1
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

    if(len(data)==7):
        if(data[5]=='hash' and data[6]=='verify'):
            replyToCalledHashVerifyFromClient(data[0],data[1],data[2],data[3],data[4])

    if(data[0]=='download' and data[1]=='TCP' and len(data)==3):
        DownloadRequestFromClientTCP(data[2])

    if(data[0]=='download' and data[1]=='UDP' and len(data)==3):
        DownloadRequestFromClientUDP(data[2])

s.shutdown(socket.SHUT_RDWR)
s.close()
