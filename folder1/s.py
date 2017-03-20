import socket,os
foo=0
arr=[[foo for i in range(100)] for j in range(100)]
# def callLsOnServer(command):
#     conn.send(command)
#     lsResult=conn.recv(1024)
#     lsResult=lsResult.split('\n')
#     i=0
#     del(lsResult[len(lsResult)-1]) #delte the last null character.
#     print "filename", "Time last modified"
#     for iterator in lsResult:
#         if(iterator.find('total')==-1):
#             arr[i]=iterator.split()
#             print arr[i][8], arr[i][5], arr[i][6], arr[i][7]
#             i=i+1
#
# def hashVerifyOnServer(filename, command):
#         filearg=filename
#         filearg="cksum"+" " + filename
#         hashValue=os.popen(filearg).read()
#         command=command + " " + hashValue
#         conn.send(command)
#         result=conn.recv(1024)
#         if(result=="No changes made to the file."):
#             print result
#         else:
#             result=result.split()
#             print "The file was modified since last access:"
#             print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
#             i=0
#             while(i<len(result)):
#                 print result[i], result[i+1], result[i+2], result[i+3]
#                 i=i+4
#         return
#
# def DownloadRequestFromServer(filename):
#         f = open(filename,'rb')
#         l = f.read(1024)
#         while (l):
#            conn.send(l)
#            print('Sent ',repr(l))
#            l = f.read(1024)
#         f.close()
#         print('Done sending')

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
        if(int(b[0])==int(filehash)):
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


def downloadFile(data):
        f=open('testdata.txt', 'wb')
        print 'file opened'
        print('data=%s', (data))
        if not data:
            return
        f.write(data)
        f.close()

port = 60000
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = ""


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

    else:
        downloadFile(originalData)

    # print "arg:",arg[0]
    # print 'Got connection from',addr
    # data = conn.recv(1024)
    # data=data.split()
    # print data
    # print('Server received', repr(data))

    # if(arg[0] == 'index'):
    #     callLsOnClient(command)
    #
    # elif(arg[0] =='hash' and arg[1] =='verify'):
    #     hashVerifyOnClient(arg[2],command)
    #
    # else:
    #     DownloadRequestFromClient(arg[0])

    # conn.send('Thank you for connecting')
    # conn.close()
s.shutdown(socket.SHUT_RDWR)
s.close()
