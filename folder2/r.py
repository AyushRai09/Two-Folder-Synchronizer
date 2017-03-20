import socket,os

def replyToCalledLsFromServer():
        lsResult=os.listdir('.')
        s.send(str(lsResult))
        return

def replyToCalledHashVerifyFromServer(filename, filehash):
        filearg=filename
        filearg="cksum" + " " + filearg
        b=os.popen(filearg).read()
        if(b==filehash):
            s.send("True")
        else:
            s.send("False")
def downloadFile(data):
        f=open('testdata', 'wb')
        print 'file opened'
        print('data=%s', (data))
        if not data:
            return
        f.write(str(data))
        f.close()

s = socket.socket()
host = ""
port = 60000

s.connect((host, port))
# s.send("Hello server!")

while True:
    print('receiving data...')
    data = s.recv(1024)
    data=data.split()
    if(data[0] == 'index'):
        replyToCalledLsFromServer()

    elif(data[0]=='hash' and data[1]=='verify'):
        replyToCalledHashVerifyFromServer(data[2],data[3])

    else:
        downloadFile(data)
print('Successfully get the file')
s.close()
print('connection closed')
