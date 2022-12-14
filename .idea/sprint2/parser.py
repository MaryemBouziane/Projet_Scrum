# Ce code permet de trouver les fichiers PDF dans un dossier spécifié, de les convertir au format texte et de parser les informations importantes (titre et abstract) dans un nouveau fichier texte. 
# Il peut être utilisé pour faciliter la recherche et l'analyse de fichiers PDF.

from os import path
import os
from glob import glob
import sys


"""Cette fonction permet de rechercher les fichiers se trouvant dans le 
dossier passé en paramètre et qui finissent par l'extension passée en paramètre.
Elle retourne une liste contenant le chemin des fichiers trouvés.
"""

def trouver_ext(chemin_dossier, ext):
    return glob(path.join(chemin_dossier, "*.{}".format(ext)))


"""
Cette fonction prend un chemin d'entrée et exécute la commande pour convertir un fichier PDF en fichier texte. 
Il s'appuie sur le script pdfToText.sh pour effectuer la conversion.
"""

def pdf_to_txt(inpute_path) :
    cmd = "./pdfToText.sh "+inpute_path
    os.system(cmd)


"""
Cette fonction prend deux arguments : file_path et titre. Elle parcours le fichier dont le chemin est fourni et cherche la phrase qui commence avec le titre donné. 
Elle retourne la phrase complétée en chaine de caractères, ou "Error" si elle ne trouve pas le titre demandé.
"""

def trouverParag(file_path, titre):
    p = ""
    lignePrecedante = "aa"
    with open(file_path, "r") as file :
        for ligne in file :
            if((ligne.lower().find(titre) != -1) or (ligne.lower().replace(" ","").find(titre) != -1)):   
                       	
                if(len(ligne) <= len(titre)+1):
                        ligne = file.readline()
                        while ligne == "\n":
                            ligne = file.readline()
                while ligne:
                    if(titre == "introduction") :
                        if((ligne[0:1] == "2" and lignePrecedante.strip()[-1:] == ".") or (ligne[0:3] == "II." and lignePrecedante.strip()[-1:] == ".")):
                             break   

                    else :
                        if(ligne.lower().strip() == "1 introduction" or ligne.strip() == "I. INTRODUCTION" or ligne[0:9] == "Keywords:" or ligne.strip() == "1. Introduction"):
                             break

                    p = p + ligne.strip() + " "
                    lignePrecedante = ligne
                    ligne = file.readline()

                if(p != "\n"):
                    return p

           

    return "!!Error!!\n"



"""
Cette fonction prend le nom du dossier en paramètre et crée un nouveau dossier. Si un dossier portant le même nom existe déjà, alors il sera supprimé et un nouveau dossier sera créé.
"""
def creerDossier(dossier):
    directory_name = dossier
    path = directory_name
    if(os.path.isdir(path)):
        os.system("rm -r " + path)                  #supprimer le dossier s'il exit    
    os.system("mkdir " + path)                      #re creer le dossier
    return path    


"""
Cette fonction permet de parser un fichier donné et d'en extraire le titre et l'abstract et de les enregistrer dans un fichier texte.
Il prend en entrée un chemin vers un fichier et le chemin de sortie du fichier texte. Il lit le fichier et extrait le titre et l'abstract et les enregistre dans le fichier de sortie.
"""

def parser_file_to_txt(filepath, output_path) :
    writer = ""
    file_name = os.path.basename(filepath).replace(".txt", ".pdf")
    titre = ""
    abstract = ""
    #   -- nom de fichier --

    fic= open(output_path, "a")
    fic.write("le nom de ce fichier est : " + file_name + "\n")
    fic.close()

    fic = open(filepath, "r")
    for i in range(2) :
        titre = titre + fic.readline().strip('\n').strip() + " "
    
    for ligne in fic :
       if(ligne.lower().find("abstract") != -1):         
          break;
       writer = writer + ligne.strip('\n').strip()
        	
    fic.close()

	
    #   -- le titre de fichier --

    fic = open(output_path, "a")
    fic.write("\n\n le titre de ce fichier est  : " + titre.rstrip() + "\n")
    fic.close()
    

    #   -- abstract --

    abstract = trouverParag(filepath, "abstract")
    fic = open(output_path, "a")
    fic.write("\n\n abstract : " + abstract)
    fic.close()
    
   
    
  
    

def main():


    args = sys.argv
    filepath = args[1]   # on prends l'argument apres la commande python3 (chemin de dossier) si le code est dans le meme dossier des fichier il suffit just de mettre le nom de dossier  
                  
    dossier_txt = "dossierText"
    dossier_output = creerDossier("Resultat")
    
    files = trouver_ext(filepath,"pdf")
    
    pdf_to_txt(filepath)
    
    	
    for file in files :
		
            File_txt_path = dossier_txt + "/" + os.path.basename(file).replace(".pdf", ".txt")
            output_path = dossier_output + "/" + os.path.basename(file).replace(".pdf", ".txt") 
            parser_file_to_txt(File_txt_path, output_path)

    
            
            

if __name__ == "__main__":
    main()
