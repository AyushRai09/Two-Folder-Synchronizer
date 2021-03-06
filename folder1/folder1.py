import socket,os,datetime
import time
from threading import Thread
import threading
foo=0
arr=[[foo for i in range(100)] for j in range(100)]
array=[[0 for i in range (100)] for j in range(100)]
global modified_files
class Serverthread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
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

        def replyToCalledHashVerifyFromClient(filename):
                filearg="cksum" + " " + filename
                b=os.popen(filearg).read()
                b=b.split() #b[0] contains the hashValue of the file at the server.
                filearg="ls -l" + " " + filename
                lsResult=os.popen(filearg).read()
                lsResult=lsResult.split()
                string=""

                if len(lsResult):
                    string=lsResult[8] + " " + lsResult[5] + " " + lsResult[6] + " " + lsResult[7] + " " + b[0]
                    # timestamp1=lsResult[5] + " " + lsResult[6] + " " + lsResult[7] + " " + "2017"
                    # timestamp2=sentFileMonth + " " + sentFileDay + " " + sentFileTime + " " + "2017"
                    # print "timestamp1:",timestamp1, "timestamp2:",timestamp2
                    # t1 = datetime.datetime.strptime(timestamp1, "%b %d %H:%M %Y")
                    # t2 = datetime.datetime.strptime(timestamp2, "%b %d %H:%M %Y")
                    #
                    # if(max(t1,t2)==t1):#Server's file is the latest file.
                    # elif(max(t1,t2)==t2):#Client's file is the latest file.
                    #     string=filename+" " +sentFileMonth + " " + sentFileDay + " " + sentFileTime + " " + filehash

                conn.send(string)
                return


        def DownloadRequestFromClientTCP(filename):
                print 'Done sending', filename
                f = open(filename,'rb')
                l = f.read(1024)
                while (l):
                   conn.send(l)
                #    print('Sent ',repr(l))
                   l = f.read(1024)
                f.close()

        def DownloadRequestFromClientUDP(filename):
                f = open(filename,'rb')
                l = f.read(1024)
                while (l):
                   s2.sendto(l,(host,port2))
                #    print('Sent ',repr(l))
                   l = f.read(1024)
                f.close()
                print('Done sending')
        def sendFilePermission(filename):
                filearg=os.popen("stat -c \"%A %a %N\"" + " " + filename).read()
                conn.send(filearg)
                return

        port = 60000
        port2=50000
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = ""

        s2=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


        s.bind((host, port))
        s.listen(5)

        # print 'Server listening....'

        conn, addr = s.accept()
        while True:
            # print 'receiving.......'
            data=conn.recv(1024)
            originalData=data
            data=data.split()
            # print "data:",data
            if(data[0]=='permission' and len(data)==2):
                sendFilePermission(data[1])

            if(data[0] == 'index'):
                replyToCalledLsFromClient()

            if(len(data)==3):
                if(data[1]=='hash' and data[2]=='verify'):
                    replyToCalledHashVerifyFromClient(data[0])

            if(data[0]=='download' and data[1]=='TCP' and len(data)==3):
                DownloadRequestFromClientTCP(data[2])

            if(data[0]=='download' and data[1]=='UDP' and len(data)==3):
                DownloadRequestFromClientUDP(data[2])

        s.shutdown(socket.SHUT_RDWR)
        s.close()

class Clientthread(Thread):
    def __init__(self):
        # print "Hello"
        Thread.__init__(self)

    def run(self):
        def callLsOnServer(command):
            s.send(command)
            lsResult=s.recv(1024)
            lsResult=lsResult.split('\n')
            del(lsResult[len(lsResult)-1]) #delte the last null character.
            i=0
            for iterator in lsResult:
                if(iterator.find('total')==-1):
                    array[i]=iterator.split()
                    i=i+1

        def hashVerifyOnServer(filename):
                s.send(filename + " " + "hash" + " " + "verify")
                result=s.recv(1024)
                # filearg='ls -l' + " " + filename
                # lsResult=os.popen(filearg).read()
                # if len(lsResult):
                #     lsResult=lsResult.split()
                #     filearg="cksum"+" " + filename
                #     hashValue=os.popen(filearg).read()
                #     hashValue=hashValue.split()
                #     s.send(lsResult[8]+ " " + lsResult[5] + " " + lsResult[6]+ " " + lsResult[7] + " " + hashValue[0] + " " + "hash" + " " + "verify")
                #     return result
                # else:
                #     return 0
                if result:
                    return result
                else:
                    return 0

        def hashVerifyOnServerForAll():
            callLsOnServer("index")
            global modified_files
            modified_files=[]
            i=0
            k=0
            while(i<100):
                if(array[i][8]!=0 and array[i][5]!=0 and  array[i][6]!=0 and array[i][7]!=0):
                    result=hashVerifyOnServer(array[i][8])
                    if(result!=0):
                        if(len(result)):
                            result=result.split()
                            modified_files.append([])
                            modified_files[k].append(result[0]) #name
                            modified_files[k].append(result[1]) #month
                            modified_files[k].append(result[2]) #time
                            modified_files[k].append(result[3]) #date
                            modified_files[k].append(result[4]) #hashvalue
                            k=k+1
                i=i+1

            i=0
            # print "length:",len(modified_files)


        def autosynchronization():
            hashVerifyOnServerForAll()
            lsResult=os.popen('ls -l').read()
            lsResult=lsResult.split('\n')
            i=0
            del(lsResult[len(lsResult)-1]) #delte the last null character.
            for iterator in lsResult:
                if(iterator.find('total')==-1):
                    arr[i]=iterator.split()
                    i=i+1
            lengthOfArr=i
            i=0
            # print "modified_files:",modified_files

            while(i<len(modified_files)):
                j=0
                fileFoundOnClient=0
                while(j<lengthOfArr):
                    if(modified_files[i][0]==arr[j][8]):
                        fileFoundOnClient=1
                        timestamp1=modified_files[i][1] + " " + modified_files[i][2] + " " + modified_files[i][3] + " " + "2017"
                        timestamp2=arr[j][5] + " " + arr[j][6] + " " + arr[j][7] + " " + "2017"

                        t1 = datetime.datetime.strptime(timestamp1, "%b %d %H:%M %Y")
                        t2 = datetime.datetime.strptime(timestamp2, "%b %d %H:%M %Y")

                        if(t1>t2):#Server has the latest file.
                            # print "Timestamp download"
                            DownloadRequestFromServerTCP("download" + " " + "TCP" + " " + modified_files[i][0], modified_files[i][0])
                    j=j+1

                if(fileFoundOnClient==0):
                    # print "not found file on client download"
                    DownloadRequestFromServerTCP("download" + " " + "TCP" + " " + modified_files[i][0], modified_files[i][0])
                i=i+1
            threading.Timer(10,autosynchronization).start()

        def regexCheckerOnServer( pattern):
            callLsOnServer("index")
            i=0
            while(i<100):
                if(array[i][8]!=0 and array[i][5]!=0 and  array[i][6]!=0 and array[i][7]!=0):
                    m=re.search(pattern,array[i][8])
                    if m is None:
                        i=i+1
                        continue
                    else:
                        print array[i][8], array[i][5], array[i][6], array[i][7]
                i=i+1
            return
        def timeStampChecker( ts1Month,ts1Date,ts1Time,ts2Month,ts2Date,ts2Time):
            callLsOnServer("index")
            i=0
            while(i<100):
                if(array[i][8]!=0 and array[i][5]!=0 and  array[i][6]!=0 and array[i][7]!=0):
                    timestamp1=ts1Month + " " + ts1Date + " " + ts1Time + " " + "2017"
                    timestamp2=ts2Month + " " + ts2Date + " " + ts2Time + " " + "2017"
                    fileTimeStamp=array[i][5] + " " + array[i][6] + " " + array[i][7] + " " +"2017"

                    t1 = datetime.datetime.strptime(timestamp1, "%b %d %H:%M %Y")
                    t2 = datetime.datetime.strptime(timestamp2, "%b %d %H:%M %Y")
                    filet=datetime.datetime.strptime(fileTimeStamp,"%b %d %H:%M %Y")

                    if(max(t1,filet)==filet and max(filet,t2)==t2):
                        print array[i][8], array[i][5], array[i][6], array[i][7]
                i=i+1

        def DownloadRequestFromServerTCP( command, filename):
                s.send("permission"+ " " + filename)
                octalResult=s.recv(1024)
                octalResult=octalResult.split()
                s.send(command)
                f=open(filename, 'wb')
                while(True):
                    try:
                        s.settimeout(1.0)
                        data=s.recv(1024)
                        # print('data=%s',(data))
                    except:
                        break
                    f.write(data)
                s.settimeout(None)
                print "Done receiving ", filename
                os.system("chmod"+ " " + octalResult[1]+ " " + filename)


        def DownloadRequestFromServerUDP( command, filename):
                s.send(command)
                data,addressWaste=s2.recvfrom(1024)
                f=open(filename, 'wb')
                print 'file opened'
                # print('data=%s', (data))
                if not data:
                    return
                f.write(data)
                f.close()

        host = ""
        port = 30000
        port2= 20000
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
            if(command==""):
                continue
            if(arg[0] == 'index' and len(arg)==1):
                callLsOnServer(command)
                print "filename", "Time last modified"
                print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                i=0
                while(i<100):
                    if(array[i][8]!=0 and array[i][5]!=0 and  array[i][6]!=0 and array[i][7]!=0):
                        print array[i][8], array[i][5], array[i][6], array[i][7]
                    i=i+1

            elif(arg[0] =='hash' and arg[1] =='verify' and len(arg)==3):
                result=hashVerifyOnServer(arg[2])
                if(result!=0):
                    if(len(result)):
                        result=result.split()
                        print result[0], result[1], result[2], result[3], result[4]


            elif(arg[0]=='hash' and arg[1]=='checkall' and len(arg)==2):
                hashVerifyOnServerForAll()
                i=0
                # print "length:", len(modified_files)
                while(i<len(modified_files)):
                    print modified_files[i][0], modified_files[i][1], modified_files[i][2], modified_files[i][3], modified_files[i][4]
                    i=i+1

            elif(arg[0]=='index' and arg[1]=="regex" and len(arg)==3):
                regexCheckerOnServer(arg[2])

            elif(arg[0]=='index' and arg[1]=='shortlist' and len(arg)==8):
                timeStampChecker(arg[2],arg[3],arg[4],arg[5],arg[6],arg[7])

            elif(arg[0]=='download' and arg[1]=='TCP' and len(arg)==3):
                DownloadRequestFromServerTCP(arg[0]+ " " + arg[1]+ " " + arg[2], arg[2])

            elif(arg[0]=='download' and arg[1]=='UDP' and len(arg)==3):
                DownloadRequestFromServerUDP(arg[0]+ " " + arg[1]+ " " + arg[2], arg[2])

            elif(arg[0]=='start' and arg[1]=='autosync' and len(arg)==2):
                autosynchronization()
                print "Folder1 updated."

            else:
                print "Invalid Request."

        print('Successfully get the file')
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        print('connection closed')

if __name__ == '__main__':
   # Declare objects of Serverthread class
   myThreadOb1 = Serverthread()

   myThreadOb2 = Clientthread()

   # Start running the threads!
   myThreadOb1.start()
   time.sleep(10)
   myThreadOb2.start()

   # Wait for the threads to finish...
   myThreadOb1.join()
   myThreadOb2.join()

   print('Main Terminating...')
