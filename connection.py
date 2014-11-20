import ftplib
import thread
import time
import sys
import os
import string
import logging
from datetime import datetime




class Ftp:
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

#verifie si un fichier est present sur le serveur, si il nexiste pas ou qui le fichier sur le serveur nest pas a jour, le programme le cree ou le remplace par la derniere version
def doesFileExistsOnServer(file, serverPath,  localPath):
    try:   
        ## Traitement si existe en fichier
        if connect.size(serverPath) != os.path.getsize(localPath) :
            connect.cwd(serverPath.replace("/" + serverPath.split("/")[-1],  "/")) 
            connect.storbinary('STOR '+file, open( localPath , 'rb'))
            logging.info(" le fichier " + localPath + " a ete mis a jour (taille du fichier)")
            
        if getLastTimeFileOnLocal(localPath) > getLastTimeFileOnServer(serverPath) :
            connect.cwd(serverPath.replace("/" + serverPath.split("/")[-1],  "/")) 
            connect.storbinary('STOR '+file, open( localPath , 'rb'))
            logging.info(" le fichier " + localPath + " a ete mis a jour (date derniere modification)")
           
    except: 
        ## Traitement si existe en repertoire ou n'existe pas
        try:  
            ## Traitement si existe en repertoire
            connect.cwd(serverPath)
            connect.cwd("..")
        except:
            ## Traitement si le fichier n'existe pas
            connect.cwd( serverPath.replace("/" + serverPath.split("/")[-1],  "/")) 
            connect.storbinary('STOR '+file, open( localPath , 'rb'))
            logging.info(" le fichier " + localPath + " a ete cree")

#verifie si un dossier existe sur le dossier courant du serveur, si il nexiste pas, on le cree
def doesDirectoryExistsOnServer(dir):
        try:  
            ## Traitement si existe en repertoire
            connect.cwd(dir) 
            
        except:
            ## Traitement si n'existe pas
            #on accede au dossier parent
            connect.cwd(dir.replace( "/" + dir.split("/")[-1],  ""))
            print connect.pwd()
            #on cree le nouveau dossier
            connect.mkd(dir.split("/")[-1])
            logging.info(" creation du dossier " + dir.split("/")[-1])
            

def isAscii(s):
    for c in s:
        if c not in string.ascii_letters and c not in string.punctuation and c not in string.digits and c not in string.whitespace:
            return False
    return True
    
#permet lajout de fichiers et leurs mise a jour
def createTree(path):

    for file in os.listdir(path) :
        if isAscii(file) == False:
            logging.error("\n nom de fichier ou dossier invalide, le programme va s'arreter")
            sys.exit(0) 
        
        tempDir = setLocalPathToChild(path,  file)

        if os.path.isdir(tempDir) :
            serverDirPath =getServerPath(tempDir)
            doesDirectoryExistsOnServer(serverDirPath)
            createTree(tempDir)
        else :
            serverDirPath =getServerPath(path)
            serverFilePath = getServerPath(tempDir)
            #doesDirectoryExistsOnServer(serverDirPath)
            doesFileExistsOnServer(file, serverFilePath,  tempDir)

#permet dobtenir le path du server correspondant au path local
def getServerPath(path):
    return  (sys.argv[5] +path.split(sys.argv[5].rsplit("/")[-1])[-1]).replace("\\", "/")

    
 #verifie si un fichier local a ete supprime ou non, localement et modifie le FTP en consequence   
def checkForDeletedThings(currentLocalFolder,  currentServerPath):

    files = []
    connect.retrlines("NLST",files.append)

    for file in files :
        if file != ".." and file != "." :
            try:  
            ## Traitement si existe en repertoire
                connect.cwd(file)
                checkForDeletedThings(setLocalPathToChild(currentLocalFolder,  file), setServerPathToChild(currentServerPath,  file)  )
                if os.path.isdir(currentLocalFolder+"\\"+file) :
                    logging.debug(" le dossier "+currentLocalFolder+"\\"+ file + " est present localement")
                else :
                    connect.rmd(file)
                    logging.info(" dossier " + file + " supprime")
                
            except:
                if os.path.isfile(currentLocalFolder+"\\"+file)== False :
                    connect.delete(file)
                    logging.info(" fichier " + file + " supprime")
                else:
                    logging.debug(" le fichier "+currentLocalFolder+"\\"+ file + " est present localement")
                ## Traitement si n'existe pas

    #on accede au dossier parent            
    connect.cwd("..")
            
#permet de concatener le Serverpath actuel avec un sous dossier quil contient
def setServerPathToChild(currentServerPath,  child):
    return currentServerPath + "/" + child
    
#permet de concatener le path actuel avec un sous dossier quil contient
def setLocalPathToChild(currentPath,  child):
    return currentPath +"\\" + child


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
   
    print "\n -----DEBUT-----"
    if os.path.isdir(sys.argv[4]) : 
        logging.info( " le dossier a synchronise " + sys.argv[4] + " est present localement")
        maConnection = Ftp(sys.argv[1],  sys.argv[2], sys.argv[3] )
        connect = maConnection.connect()
        
        
        try :
            connect.cwd(sys.argv[5])
            logging.info(" le dossier de destination de la synchronisation " + sys.argv[5] + " est present le serveur")
        except :
            connect.mkd(sys.argv[5])
            logging.info(" creation du dossier de synchronisation " + sys.argv[5] + " sur le serveur")
            
        print "\n --------CREATION ET MISE A JOUR DES FICHIERS ET DOSSIERS--------"
        createTree(sys.argv[4])
        connect.cwd(sys.argv[5])
        print "\n --------VERIFICATION DE LA SUPPRESSION DE FICHIERS--------"
        checkForDeletedThings(sys.argv[4],  sys.argv[5])
    else :
        logging.info( " le dossier a synchronise " + sys.argv[4] + " n\'existe pas, operation annulee")
    
    print "\n --------FIN--------"
    

    
