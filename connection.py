import ftplib
import thread
import time
import Queue
import sys
import os
from datetime import datetime

class Ftp:
    #lala
    def __init__(self, host,  account,  password):
        self.host = host
        self.account = account
        self.password = password

    def connect(self):
        return ftplib.FTP(self.host,  self.account,  self.password)

def getLastTimeFileOnServer(serverPath):
    return connect.sendcmd("MDTM "+"/" + serverPath.replace("\\", "/")).split(" ")[-1]

def getLastTimeFileOnLocal(localPath):
    return datetime.utcfromtimestamp(os.path.getmtime(localPath)).isoformat(" ").replace("-", "").replace(":",  "").replace(" ",  "").split(".")[0]
    
def getFileServerPermission(serverPath):
    return 0

def doesFileExistsOnServer(file, serverPath,  localPath):
    try:   
        ## Traitement si existe en fichier
        if connect.size(serverPath) != os.path.getsize(localPath) :
            connect.cwd(serverPath.replace("/" + serverPath.split("/")[-1],  "/")) 
            connect.storbinary('STOR '+file, open( localPath , 'rb'))
            print "le fichier " + localPath + " a ete mis a jour (taille du fichier)"
            
        if getLastTimeFileOnLocal(localPath) > getLastTimeFileOnServer(serverPath) :
            connect.cwd(serverPath.replace("/" + serverPath.split("/")[-1],  "/")) 
            connect.storbinary('STOR '+file, open( localPath , 'rb'))
            print "le fichier " + localPath + " a ete mis a jour (date derniere modification)"
           
    except: 
        ## Traitement si existe en repertoire ou n'existe pas
        try:  
            ## Traitement si existe en repertoire
            connect.cwd(serverPath)
            connect.cwd("..")
        except:
            ## Traitement si le fichier n'existe pas
            #print  "acces au dossier " + serverPath.replace("/" + serverPath.split("/")[-1],  "/")
           # print "acces au dossier" + serverPath
            connect.cwd( serverPath.replace("/" + serverPath.split("/")[-1],  "/")) 
            connect.storbinary('STOR '+file, open( localPath , 'rb'))
            print "le fichier " + localPath + " a ete cree"

def doesDirectoryExistsOnServer(dir):
        try:  
            ## Traitement si existe en repertoire
            connect.cwd(dir) 
            #print "acces au repertoire FTP " + dir
           # print connect.pwd()
            
        except:
            ## Traitement si n'existe pas

            #on accede au dossier parent
            connect.cwd(dir.replace( "/" + dir.split("/")[-1],  ""))
            print connect.pwd()
            #on cree le nouveau dossier
            connect.mkd(dir.split("/")[-1])
            print "creation du dossier " + dir.split("/")[-1]

           
           
def createTree(path):

#  doesFileExistsOnServer(connect.cwd(sys.argv[5])[0])  
    print os.listdir(path)
    for file in os.listdir(path) :
        tempDir = getLocalFullPath(path,  file)

        if os.path.isdir(tempDir) :
            print "\n ------DOSSIER " + path + "------" 

            serverDirPath =getServerPath(tempDir)
            doesDirectoryExistsOnServer(serverDirPath)
            createTree(tempDir)
        else :
            serverDirPath =getServerPath(path)
            serverFilePath = getServerPath(tempDir)
            doesDirectoryExistsOnServer(serverDirPath)
            doesFileExistsOnServer(file, serverFilePath,  tempDir)


def getServerPath(path):
    return  "/"+ (sys.argv[5] +path.split(sys.argv[5])[-1]).replace("\\", "/")

def concatPath(currentPath,  file):
    return "/" + currentPath + "/" + file

def getLocalFullPath(path,  file):
    return path + "\\" + file
    
def checkForDeletedThings(currentLocalFolder,  currentServerPath):

    files = []
    content = connect.retrlines("NLST",files.append)
#    print connect.nlst();
        

    for file in files :
        if file != ".." and file != "." :
            try:  
            ## Traitement si existe en repertoire
                connect.cwd(file)
                checkForDeletedThings(setLocalPathToChild(currentLocalFolder,  file), setServerPathToChild(currentServerPath,  file)  )
                if os.path.isdir(currentLocalFolder+"\\"+file) :
                    print currentLocalFolder+"\\"+ file + " est present localement"
                else :
                    #print"deleting" +  currentPath + "/" + file
                    print "suppression du dossier " + file
                    connect.rmd(file)
                    print "dossier " + file + " supprime"
                    #deleteFolderContent(file)
                
            except:
                if os.path.isfile(currentLocalFolder+"\\"+file)== False :
                    connect.delete(file)
                    print "fichier " + file + " supprime"
                ## Traitement si n'existe pas
            #on accede au dossier parent
            # connect.cwd(dir.replace( "/" + dir.split("/")[-1],  ""))
            
    connect.cwd("..")
            

def setServerPathToChild(currentServerPath,  child):
    return currentServerPath + "/" + child

def setServerPathToFather(currentServerPath):
    return currentPath.rstrip("/" + currentPath.split("/")[-1])

def setLocalPathToFather(currentPath):
    return currentPath.rstrip("\\" + currentPath.split("\\")[-1])
    
def setLocalPathToChild(currentPath,  child):
    return currentPath +"\\" + child


    
def deleteFile(fileName):
    element = raw_input(fileName) # vous indiquez dans la console le fichier, ex. : fichier.py
    delete = connect.delete(element) ## cest la fonction en elle-meme
    



if __name__ == '__main__':
    
    if os.path.isdir(sys.argv[4]) : 
        print "le repertoire : " + sys.argv[4] + " existe"
        maConnection = Ftp(sys.argv[1],  sys.argv[2], sys.argv[3] )
        
        
        connect = maConnection.connect()
       # print connect.retrlines('LIST')
        connect.cwd(sys.argv[5])
        #createTree(sys.argv[4])
        checkForDeletedThings(sys.argv[4],  "/"+sys.argv[5])
    else :
        print "le repertoire : " + sys.argv[4] + " n\'existe pas, operation annulee"





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
