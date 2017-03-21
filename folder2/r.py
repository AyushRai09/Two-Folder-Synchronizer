import socket,os,re,datetime
foo=0
arr=[[foo for i in range(100)] for j in range(100)]

def callLsOnServer(command):
    s.send(command)
    lsResult=s.recv(1024)
    lsResult=lsResult.split('\n')
    del(lsResult[len(lsResult)-1]) #delte the last null character.
    i=0
    for iterator in lsResult:
        if(iterator.find('total')==-1):
            arr[i]=iterator.split()
            i=i+1

def hashVerifyOnServer(filename, command):
        filearg=filename
        filearg="cksum"+" " + filename
        hashValue=os.popen(filearg).read()
        command=command + " " + hashValue + '00'
        s.send(command)
        result=s.recv(1024)
        if(result=="No changes made to the file."):
            print result
        else:
            result=result.split()
            i=0
            while(i<len(result)):
                print result[i], result[i+1], result[i+2], result[i+3]
                i=i+4
        return

def regexCheckerOnServer(pattern):
    callLsOnServer("index")
    i=0
    while(i<100):
        if(arr[i][8]!=0 and arr[i][5]!=0 and  arr[i][6]!=0 and arr[i][7]!=0):
            m=re.search(pattern,arr[i][8])
            if m is None:
                i=i+1
                continue
            else:
                print arr[i][8], arr[i][5], arr[i][6], arr[i][7]
        i=i+1
    return
def timeStampChecker(ts1Month,ts1Date,ts1Time,ts2Month,ts2Date,ts2Time):
    callLsOnServer("index")
    i=0
    while(i<100):
        if(arr[i][8]!=0 and arr[i][5]!=0 and  arr[i][6]!=0 and arr[i][7]!=0):
            timestamp1=ts1Month + " " + ts1Date + " " + ts1Time + " " + "2017"
            timestamp2=ts2Month + " " + ts2Date + " " + ts2Time + " " + "2017"
            fileTimeStamp=arr[i][5] + " " + arr[i][6] + " " + arr[i][7] + " " +"2017"

            t1 = datetime.datetime.strptime(timestamp1, "%b %d %H:%M %Y")
            t2 = datetime.datetime.strptime(timestamp2, "%b %d %H:%M %Y")
            filet=datetime.datetime.strptime(fileTimeStamp,"%b %d %H:%M %Y")

            if(max(t1,filet)==filet and max(filet,t2)==t2):
                print arr[i][8], arr[i][5], arr[i][6], arr[i][7]
        i=i+1


def DownloadRequestFromServerTCP(command, filename):
        s.send(command)
        data=s.recv(1024)
        f=open(filename, 'wb')
        print 'file opened'
        print('data=%s', (data))
        if not data:
            return
        f.write(data)
        f.close()

def DownloadRequestFromServerUDP(command, filename):
        s.send(command)
        data,addressWaste=s2.recvfrom(1024)
        f=open(filename, 'wb')
        print 'file opened'
        print('data=%s', (data))
        if not data:
            return
        f.write(data)
        f.close()

host = ""
port = 60000
port2= 50000
s = socket.socket() # for TCP
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s2=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# s2.sendto(MESSAGE, (UDP_IP, UDP_PORT))


s.connect((host, port))
s2.bind((host,port2))
# s.send("Hello server!")

while True:
    command = raw_input("prompt:$ ")
    arg=command.split()
    # data = s.recv(1024)
    if(arg[0] == 'index' and len(arg)==1):
        callLsOnServer(command)
        print "filename", "Time last modified"
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        i=0
        while(i<100):
            if(arr[i][8]!=0 and arr[i][5]!=0 and  arr[i][6]!=0 and arr[i][7]!=0):
                print arr[i][8], arr[i][5], arr[i][6], arr[i][7]
            i=i+1

    elif(arg[0] =='hash' and arg[1] =='verify' and len(arg)==3):
        hashVerifyOnServer(arg[2],command)

    elif(arg[0]=='index' and arg[1]=="regex" and len(arg)==3):
        regexCheckerOnServer(arg[2])

    elif(arg[0]=='index' and arg[1]=='shortlist' and len(arg)==8):
        timeStampChecker(arg[2],arg[3],arg[4],arg[5],arg[6],arg[7])

    elif(arg[0]=='download' and arg[1]=='TCP' and len(arg)==3):
        DownloadRequestFromServerTCP(arg[0]+ " " + arg[1]+ " " + arg[2], arg[2])

    elif(arg[0]=='download' and arg[1]=='UDP' and len(arg)==3):
        DownloadRequestFromServerUDP(arg[0]+ " " + arg[1]+ " " + arg[2], arg[2])

    else:
        print "Invalid Request."

print('Successfully get the file')
s.shutdown(socket.SHUT_RDWR)
s.close()
print('connection closed')
