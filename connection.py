import ftplib
import sys
import os
import string
import logging
import platform
from datetime import datetime

class Ftp:
    def __init__(self, host,  account,  password):
        self.host = host
        self.account = account
        self.password = password

    def connect(self):## permet la connexion au serveur ftp
        return ftplib.FTP(self.host,  self.account,  self.password)

def getLastTimeFileOnServer(serverPath):##recupere la date de derniere modification du fichier enregistrer sur le serveur au format aaaaMMjjhhmmss
    return connect.sendcmd("MDTM "+"/" + serverPath.replace("\\", "/")).split(" ")[-1]

def getLastTimeFileOnLocal(localPath):##recupere la date de derniere modification du fichier enregistrer en local aaaaMMjjhhmmss
    return datetime.utcfromtimestamp(os.path.getmtime(localPath)).isoformat(" ").replace("-", "").replace(":",  "").replace(" ",  "").split(".")[0]


##verifie si un fichier est present sur le serveur, si il nexiste pas ou qui le fichier sur le serveur nest pas a jour, le programme le cree ou le remplace par la derniere version
def doesFileExistsOnServer(file, serverPath,  localPath):
    try:  ## Traitement si existe en fichier 
        if connect.size(serverPath) != os.path.getsize(localPath) : ##lance exception si ce n'est pas un fichier
            connect.cwd(serverPath.replace("/" + serverPath.split("/")[-1],  "/")) 
            connect.storbinary('STOR '+file, open( localPath , 'rb'))
            logging.info(" le fichier " + localPath + " a ete mis a jour (taille du fichier)")
        
        if getLastTimeFileOnLocal(localPath) > getLastTimeFileOnServer(serverPath) :
            connect.cwd(serverPath.replace("/" + serverPath.split("/")[-1],  "/")) 
            connect.storbinary('STOR '+file, open( localPath , 'rb'))
            logging.info(" le fichier " + localPath + " a ete mis a jour (date derniere modification)")
           
    except: ## Traitement si existe en repertoire ou n'existe pas
        try:  ## Traitement si existe en repertoire
            connect.cwd(serverPath)##lance une exception si ce n'est pas un dossier (ici, signifie que le fichier n'existe pas)
            connect.cwd("..")
        except:## Traitement si le fichier n'existe pas
            print serverPath.rstrip(file)
            connect.cwd(serverPath.rstrip(file)) 
            ##connect.cwd( serverPath.replace("/" + serverPath.split("/")[-1],  "/").replace("//", "/")  )
            connect.storbinary('STOR '+file, open( localPath , 'rb'))##on cree le fichier sur le ftp
            logging.info(" le fichier " + localPath + " a ete cree")

##verifie si un dossier existe sur le dossier courant du serveur, si il nexiste pas, on le cree
def doesDirectoryExistsOnServer(dir, file):
        try:  ## Traitement si existe en repertoire
            connect.cwd(dir) ##lance une exeption si ce n'est pas un dossier (ici, signifie que le dossier n'existe pas)
            
        except:## Traitement si n'existe pas
            print dir.rstrip(file)
            connect.cwd(dir.rstrip(file))##on accede au dossier parent
            connect.mkd(dir.split("/")[-1]) ##on cree le nouveau dossier
            logging.info(" creation du dossier " + dir.split("/")[-1])
            

def isAscii(s):## verifie si une chaine est uniquement compose de caracteres ASCII
    for c in s:
        if c not in string.ascii_letters and c not in string.punctuation and c not in string.digits and c not in string.whitespace:
            return False
    return True
    
##permet l ajout de fichiers et leurs mise a jour
def browseLocalFolder(path):

    for file in os.listdir(path) : ##liste les dossiers et fichiers present dans le dossier courant
        if isAscii(file) == False:
            logging.error("\n nom de fichier ou dossier invalide ( "+file+" ) , le programme va s'arreter")
            sys.exit(0) ## si un nom contient des caracteres non-ASCII on arrete le programme
        
        tempDir = setLocalPathToChild(path,  file)

        if os.path.isdir(tempDir) : ## si c'est un dossier
            serverDirPath =getServerPath(tempDir)
            doesDirectoryExistsOnServer(serverDirPath,  file) ## on verifie l existence de ce dossier sur le serveur
            browseLocalFolder(tempDir) ##on relance la recherche dans ce dossier
        else :
            serverDirPath =getServerPath(path)
            serverFilePath = getServerPath(tempDir)
            #doesDirectoryExistsOnServer(serverDirPath)
            doesFileExistsOnServer(file, setServerPathToChild(serverDirPath,  file),  tempDir) ## on verifie l existence de ce fichier sur le serveur


def getServerPath(path):##permet dobtenir le path du server correspondant au path local
    ##return sys.argv[5] + (path.split(sys.argv[5].split("/")[-1])[-1]).replace("\\", "/")
    return (sys.argv[5]+ (path.replace(sys.argv[4], ""))).replace("\\","/")
    

def checkForDeletedThings(currentLocalFolder,  currentServerPath):##verifie si un fichier local a ete supprime ou non localement et modifie le FTP en consequence 

    files = []
    connect.retrlines("NLST",files.append)

    for file in files :
        if file != ".." and file != "." :
            try:  ## Traitement cest un repertoire
                connect.cwd(file)
                checkForDeletedThings(setLocalPathToChild(currentLocalFolder,  file), setServerPathToChild(currentServerPath,  file) )
                
                if os.path.isdir(setLocalPathToChild(currentLocalFolder,  file)) : ##si le dossier existe en local, on ne fait rien
                    logging.debug(" le dossier "+setLocalPathToChild(currentLocalFolder,  file)  + " est present localement")
                else : ##si il nexiste pas on le supprime sur le serveur
                    connect.rmd(file)
                    logging.info(" dossier " + file + " supprime")
                
            except:## Traitement si cest un fichier
                if os.path.isfile(setLocalPathToChild(currentLocalFolder,  file))== False : ## si le fichier nexiste pas localement on le supprime sur le serveur
                    connect.delete(file)
                    logging.info(" fichier " + file + " supprime")
                else: ##si il existe localement, on ne fait rien
                    logging.debug(" le fichier "+currentLocalFolder+"\\"+ file + " est present localement")
                

    ##on accede au dossier parent            
    connect.cwd("..")
            
##permet de concatener le Serverpath actuel avec un sous dossier quil contient
def setServerPathToChild(currentServerPath,  child):
    return currentServerPath + "/" + child
    
##permet de concatener le path actuel avec un sous dossier quil contient
def setLocalPathToChild(currentPath,  child):
    if isWindows :
        return currentPath +"\\" + child
    else  :
        return currentPath +"/" + child

 
def setServerPathToFather(currentPath):
    return  currentPath.split("/" + currentPath.split("/")[-1])[0]

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    
    if platform.system() == "Windows" :
        isWindows = True
    else : 
        isWindows = False
        
    print "le programme tourne sous " + platform.system() 
    print "\n -----DEBUT-----"
    if os.path.isdir(sys.argv[4]) : 
        logging.info( " le dossier a synchronise " + sys.argv[4] + " est present localement")
        maConnection = Ftp(sys.argv[1],  sys.argv[2], sys.argv[3] )
        connect = maConnection.connect()
        
        
        try :
            connect.cwd(sys.argv[5]) ##on verifie si le dossier a synchroniser existe sur le ftp
            logging.info(" le dossier de destination de la synchronisation " + sys.argv[5] + " est present le serveur")
        except :
            try:
                connect.cwd(setServerPathToFather(sys.argv[5]))## si il nexiste pas, on se connecte au repertoire dans lequel il est contenu
                connect.mkd(sys.argv[5])##on cree le dossier au bon endroit
                logging.info(" creation du dossier de synchronisation " + sys.argv[5] + " sur le serveur")
            except:
                logging.error(" l\'arborescence " + sys.argv[5] + " n\'existe pas"  ) ##si le chemin specifie nexiste pas, on arrete le programme
                sys.exit(0)
                
            
        print "\n --------CREATION ET MISE A JOUR DES FICHIERS ET DOSSIERS--------"
        browseLocalFolder(sys.argv[4]) ## parcours du dossier local
        connect.cwd(sys.argv[5]) ##on revient au dossier principal sur le serveur
        print "\n --------VERIFICATION DE LA SUPPRESSION DE FICHIERS--------"
        checkForDeletedThings(sys.argv[4],  sys.argv[5]) ## parcours du dossier distant pour supprimer les fichiers qui n'existent plus en local
    else :
        logging.info( " le dossier a synchronise " + sys.argv[4] + " n\'existe pas, operation annulee")
    
    print "\n --------SYNCHRONISATION TERMINEE--------"

