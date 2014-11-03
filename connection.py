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
    print "---CONTENU DU REPERTOIRE FTP---"
    print connect.pwd()
    connect.retrlines('LIST')

def doesFileExistsOnServer(file, fileName):
    try:   
        ## Traitement si existe en fichier
        connect.size(fileName) 
    except: 
        ## Traitement si existe en repertoire ou n'existe pas
        try:  
            ## Traitement si existe en repertoire
            connect.cwd(fileName) 
            connect.cwd("..")
        except:
            ## Traitement si n'existe pas
            connect.storbinary('STOR '+file, open(fileName, 'rb'))

def doesDirectoryExistsOnServer(dir):
        try:  
            ## Traitement si existe en repertoire
            connect.cwd(dir) 
            connect.cwd("..")
        except:
            ## Traitement si n'existe pas
            connect.mkd(dir)

    
def synchroFTP(connect,  localPath, serverPath):
    connect.cwd(sys.argv[5])
    for root, dirs, files in os.walk(localPath):  
        for fichier in files:
           
            #envoiFichierSurFtp(connect,  filePath)
            filePath = root + "\\"+ fichier #probleme : ecris tous les fichiers dans le dossier root
            #print filePath
            #print dirs
            
            tempDir = dirs
            serverPath = filePath.split(localPath +"\\")
            print serverPath[-1]
            
            doesFileExistsOnServer(fichier, filePath)
            
        for dir in dirs:
            doesDirectoryExistsOnServer(dir)
#            try:  
#                connect.cwd(serverPath[-1])
#                connect.cwd("..")	 
#                   
#            except: 
#                print " creation du repertoire" + serverPath[-1]
#                connect.mkd(serverPath[-1])
#                connect.cwd(serverPath[-1])
                    

                
            # Traitement si c'est un fichier 
            
            


#            serverPath = filePath.split(localPath +"\\")
#            print serverPath[-1]

           
    
    
if __name__ == '__main__':

    if os.path.isdir(sys.argv[4]) : 
        print "le repertoire : " + sys.argv[4] + " existe"
        maConnection = Ftp(sys.argv[1],  sys.argv[2], sys.argv[3] )
        
        
        connect = maConnection.connect()
        synchroFTP(connect, sys.argv[4],  sys.argv[5])
        walkThroughServer(connect,sys.argv[5] )
    else :
        print "le repertoire : " + sys.argv[4] + " n\'existe pas, operation annulee"

    
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
