import ftplib
import thread
import time
import Queue
import sys
import os

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
        
        
        
        #La fonction os.walk(path) cree un generateur de triplets (root, dirs, files) dans l'arborescence de path. 
#Un triplet est genere par repertoire visite. root represente le chemin d'acces du repertoire
#visite. dirs est la liste des sous-repertoires du repertoire root et files est la liste des fichiers du
#repertoire root. 
def walkTroughLocalDirectory(path):  
    size = 0  
    print "nombre de fichier total dans le dossier =  %s" % len(os.listdir(path))
    for root, dirs, files in os.walk(path):  
        for fic in files:  
            size += os.path.getsize(os.path.join(root, fic)) 
    return size 
  

def doesLocalFolderExists(path):
    current_dir = os.path.dirname(path)
    print current_dir
    
def walkThroughServer(connect,  path):
#acces au repertoire
#FONCTIONNE COMME UN SERVEUR LINUX 

    connect.cwd(path)
    print connect.pwd()
    rep = connect.dir() # on recupere le listing
    
def synchroFTP(connect,  localPath, serverPath):
    for root, dirs, files in os.walk(localPath):  
        for fichier in files:
            
            #envoiFichierSurFtp(connect,  filePath)
            filePath = root + "\\"+ fichier
            print filePath
           
    
    
if __name__ == '__main__':

    if os.path.isdir(sys.argv[5]) : 
        print "le repertoire : " + sys.argv[5] + " existe"
        maConnection = Ftp(sys.argv[1],  sys.argv[2], sys.argv[3] )
        print walkTroughLocalDirectory(sys.argv[4])
        connect = maConnection.connect()
    else :
        print "le repertoire : " + sys.argv[5] + " n\'existe pas, operation annulee"

    synchroFTP(connect, sys.argv[4],   "python")
   # maConnection.sendFile("C:\Users\ISEN\Desktop\pompozob.txt")
   # tableau =  connect.retrlines('LIST')
    #connect.dir('LIST')
    #print tableau[(0, 0)]
    


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
