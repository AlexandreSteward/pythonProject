#!/usr/bin/python
# -*- coding: Utf-8 -*-
import ftplib
import thread
import time
import Queue
import sys
import os
import string
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
            connect.cwd( serverPath.replace("/" + serverPath.split("/")[-1],  "/")) 
            connect.storbinary('STOR '+file, open( localPath , 'rb'))
            print "le fichier " + localPath + " a ete cree"

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
            print "creation du dossier " + dir.split("/")[-1]

def isAscii(s):
    for c in s:
        if c not in string.ascii_letters and c != " ":
            return False
    return True
    
#permet lajout de fichiers et leurs mise a jour
def createTree(path):
    
    print os.listdir(path)
    for file in os.listdir(path) :
        if isAscii(file) == False:
            print "\n nom de fichier ou dossier invalide, le programme va s'arreter"
            sys.exit(0) 
        
        tempDir = setLocalPathToChild(path,  file)

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
                    print currentLocalFolder+"\\"+ file + " est present localement"
                else :
                    print "suppression du dossier " + file
                    connect.rmd(file)
                    print "dossier " + file + " supprime"
                
            except:
                if os.path.isfile(currentLocalFolder+"\\"+file)== False :
                    connect.delete(file)
                    print "fichier " + file + " supprime"
                ## Traitement si n'existe pas

    #on accede au dossier parent            
    connect.cwd("..")
            
#permet de concatener le Serverpath actuel avec un sous dossier quil contient
def setServerPathToChild(currentServerPath,  child):
    return currentServerPath + "/" + child
    
#permet de concatener le path actuel avec un sous dossier quil contient
def setLocalPathToChild(currentPath,  child):
    return currentPath +"\\" + child

#def setServerPathToFather(currentServerPath):
#    return currentPath.rstrip("/" + currentPath.split("/")[-1])
#
#def setLocalPathToFather(currentPath):
#    return currentPath.rstrip("\\" + currentPath.split("\\")[-1])
 



if __name__ == '__main__':
    
    print "\n------TESTS------"
    
    print "getServerPath : " + getServerPath("C:\Users\ISEN\Google Drive\python\lalala\llflfzeazef")
    print "getServerPath : " +  getServerPath("C:\Users\ISEN\Google Drive\python\lalala\\")
    print "setServerPathToChild : " + setServerPathToChild("/python/lilaloum/pim/pam", "poum")
    print "setLocalPathToChild : " + setLocalPathToChild("C:\Users\ISEN\Google Drive\python", "lalala")
    
    print "\n -----DEBUT-----"
    if os.path.isdir(sys.argv[4]) : 
        print " le repertoire : >> " + sys.argv[4] + " << EXISTE"
        maConnection = Ftp(sys.argv[1],  sys.argv[2], sys.argv[3] )
        connect = maConnection.connect()
        
        
        try :
            connect.cwd(sys.argv[5])
        except :
            mkdir(sys.argv[5])
            
        print "\n --------CREATION ET MISE A JOUR DES FICHIERS ET DOSSIERS--------"
        createTree(sys.argv[4])
        connect.cwd(sys.argv[5])
        print "\n --------VERIFICATION DE LA SUPPRESSION DE FICHIERS--------"
        checkForDeletedThings(sys.argv[4],  sys.argv[5])
    else :
        print "le repertoire : " + sys.argv[4] + " n\'existe pas, operation annulee"
    
    print "\n --------FIN--------"
    

    





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
