import ftplib
import thread
import time
import Queue
import sys

class Ftp:
    #lala
    def __init__(self, host,  account,  password):
        self.host = host
        self.account = account
        self.password = password

    def connect(self):
        return ftplib.FTP(self.host,  self.account,  self.password)
    
    def sendFile(self, addresse):
        file = open(addresse, 'rb')
        name = "renamed file"
        connect.storbinary('STOR ' + "name",  file)
        file.close()
        
if __name__ == '__main__':
    print "hello"
    maConnection = Ftp(sys.argv[1],  sys.argv[2], sys.argv[3] )
    print "hello"
    connect = maConnection.connect()

    
   # maConnection.sendFile("C:\Users\ISEN\Desktop\pompozob.txt")
    connect.retrlines('LIST')


 #Define a function for the thread
def envoiFichierSurFtp( connection,  filePath):
   connection.connect()
   connection.sendFile(filePath)
   print "file " + filePath + " sent"

## Create two threads as follows
#try:
#    thread.start_new_thread(envoiFichierSurFtp,  (maConnection,  "C:\Users\ISEN\Desktop\pompozob.txt" ) )
##    thread.start_new_thread( print_time, ("Thread-1", 2, ) )
##    thread.start_new_thread( print_time, ("Thread-2", 4 ) )
#except:
#   print "Error: unable to start thread"
#
#while 1:
#   pass
