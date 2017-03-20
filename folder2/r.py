import socket,os
foo=0
arr=[[foo for i in range(100)] for j in range(100)]
def replyToCalledLsFromServer():
        lsResult=os.popen('ls -l').read()
        s.send(str(lsResult))
        lsResult=lsResult.split('\n')
        i=0
        del(lsResult[len(lsResult)-1]) #delte the last null character.
        for iterator in lsResult:
            if(iterator.find('total')==-1):
                arr[i]=iterator.split()
                i=i+1
        return

def replyToCalledHashVerifyFromServer(filename, filehash):
        filearg=filename
        filearg="cksum" + " " + filearg
        b=os.popen(filearg).read()
        b=b.split()
        print "b:", b,"filehash:",filehash
        if(int(b[0])==int(filehash)):
            s.send("No changes made to the file.")
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
                    # print arr[i][8], arr[i][5], arr[i][6], arr[i][7]
                    string=string + arr[i][8] + " " + arr[i][5] + " " + arr[i][6] + " " + arr[i][7] + " "
                i=i+1
            s.send(string)
        return


def downloadFile(data):
        f=open('testdata', 'wb')
        print 'file opened'
        print('data=%s', (data))
        if not data:
            return
        f.write(data)
        f.close()

s = socket.socket()
host = ""
port = 60000

s.connect((host, port))
# s.send("Hello server!")

while True:
    print('receiving data...')
    data = s.recv(1024)
    originalData=data
    data=data.split()
    print "data:",data
    if(data[0] == 'index'):
        replyToCalledLsFromServer()

    elif(data[0]=='hash' and data[1]=='verify'):
        replyToCalledHashVerifyFromServer(data[2],data[3])

    else:
        downloadFile(originalData)
print('Successfully get the file')
s.close()
print('connection closed')
