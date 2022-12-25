"""

Ce code permet de trouver les fichiers PDF dans un dossier spécifié, de les convertir au format texte et de parser les informations importantes (titre et abstract) dans un nouveau fichier texte. 
Il peut être utilisé pour faciliter la recherche et l'analyse de fichiers PDF.

"""

from os import path
import os
from glob import glob
import sys
from lxml import etree
import xml.etree.ElementTree as ET
import xml.dom.minidom as md


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
Cette fonction cherche l'introduction,abstract et conclusion
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
            elif((titre == "Conclusion" and ligne.find(titre) != -1) or ligne.find("Conclusions") != -1 or titre.upper() in ligne):

                if(len(ligne) <= len(titre)+1):
                    ligne = file.readline()
                    while ligne == "\n":
                        ligne = file.readline()

                while ligne:
                    if(("References" in ligne or "REFERENCES" in ligne)):
                        break

                    p = p + ligne.strip() + " "
                    lignePrecedante = ligne
                    ligne = file.readline()

                if(p != "\n"):
                    return p

    return "Not Found\n"

           

    return "!!Error!!\n"


"""
Cette fonction cherche Les références bibliographiques du papier
"""

def trouverRef(file_path, titre):
    p = ""
    with open(file_path, "r") as file :
        for ligne in file :
            if((ligne.find(titre) != -1 or ligne.find("REFERENCES") != -1) and len(ligne.strip())<=13):            	
                if(len(ligne) <= len(titre)+1):
                        ligne = file.readline()
                        while ligne == "\n":
                            ligne = file.readline()
                while ligne:
                    if(titre == "References" or titre.upper() == "REFERENCES") :
                        if(ligne is None) :
                             break
                    p = p + ligne.strip() + " "
                    ligne = file.readline()
                if(p != "\n"):
                    return p
    return "Not Found\n"



"""
fonction cherche La discussion du papier
"""

def trouverDisc(file_path,titre):
    p=""
    with open(file_path,"r") as file :
        for ligne in file:
            if( (ligne.find(titre)!=-1 or ligne.find("DISCUSSION")==-1)):
                if(len(ligne)<=len(titre)+1):
                    ligne=file.readline()
                    while ligne =="\n":
                        ligne=file.readline()
                while ligne:
                    if(titre=="Discussion" or titre.upper()=="DISCUSSION"):
                        if(((ligne.find("References") != -1 or ligne.find("REFERENCES") != -1 )and len(ligne.strip())<=11) or (ligne.find("Conclusions") != -1 or ligne.find("CONCLUSIONS") != -1 or ligne.find("Conclusion") != -1 or ligne.find("CONCLUSION") != -1)):
                            break;
                    p = p + ligne.strip() + " "
                    ligne = file.readline()
                if(p!="\n"):
                    return p

    return "Not Found\n"

"""
fonction cherche le corps :le développement du papier
"""

def trouverCorps(file_path):
    p = ""
    lignePrecedante = ""
    check = trouverParag(file_path,"introduction")
    with open(file_path, "r") as file :
        for ligne in file :
            if(check == "Not Found\n"):
                if(ligne[0:1] == "1" or ligne[0:3] == "I."):
                    while ligne:
                        if(ligne.find("Discussion") != -1 or ligne.find("DISCUSSION") != -1 or ligne.find("Conclusions") != -1 or ligne.find("CONCLUSIONS") != -1 or ligne.find("Conclusion") != -1 or ligne.find("CONCLUSION") != -1 or ((ligne.find("References") != -1 or ligne.find("REFERENCES") != -1) and len(ligne.strip())<=13)) :
                            break
                        p = p + ligne.strip() + " "
                        ligne = file.readline()
                    return p

                lignePrecedante = ligne

            else:
                if((ligne[0:1] == "2" and lignePrecedante.strip()[-1:] == ".") or (ligne[0:3] == "II." and lignePrecedante.strip()[-1:] == ".")):
                    while ligne:
                        if(ligne.find("Discussion") != -1 or ligne.find("DISCUSSION") != -1 or ligne.find("Conclusions") != -1 or ligne.find("CONCLUSIONS") != -1 or ligne.find("Conclusion") != -1 or ligne.find("CONCLUSION") != -1 or ((ligne.find("References") != -1 or ligne.find("REFERENCES") != -1) and len(ligne.strip())<=13)) :
                            break
                        p = p + ligne.strip() + " "
                        ligne = file.readline()
                    return p

                lignePrecedante = ligne



    return "Not Found\n"





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
il extrait le titre, le nom de l'auteur, l'abstract, biblio, l'intro, le corps, conclusion et la discussion
Elle écrit ensuite ces informations dans le fichier de sortie.
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

    #   -- le titre du fichier --

    fic = open(output_path, "a")
    fic.write("\n\n le titre de ce fichier est  : " + titre.rstrip() + "\n")
    fic.close()

    #   -- les auteurs du fichier --

    fic = open(output_path, "a")
    fic.write("\n\n les auteurs  : " + writer.rstrip() + "\n")
    fic.close()
    

    #   -- abstract --

    abstract = trouverParag(filepath, "abstract")
    fic = open(output_path, "a")
    fic.write("\n\n abstract : " + abstract)
    fic.close()

    #   -- biblio --

    reference = trouverRef(filepath, "References")
    fic = open(output_path, "a")
    fic.write("\n\n references : " + reference)
    fic.close()
    #   -- introduction --

    introduction = trouverParag(filepath, "introduction")
    fic = open(output_path, "a")
    fic.write("\n\n introduction : " + introduction)
    fic.close()
    #   -- corps--

    corps = trouverCorps(filepath)
    fic = open(output_path, "a")
    fic.write("\n\n corps : " + corps)
    fic.close()
    #   -- conclusion --
    conclusion = trouverParag(filepath, "Conclusion")
    fic = open(output_path, "a")
    fic.write("\n\n conclusion : " + conclusion)
    fic.close()

    #   -- discussion --
    discussion = trouverDisc(filepath, "Discussion")
    fic = open(output_path, "a")
    fic.write("\n\n discussion : " + discussion)
    fic.close()


"""
Cette fonction a pour but de parser un fichier texte et d'en créer un fichier XML. 
Elle commence par créer un élément "article" qui sera le noeud principal du fichier XML. 
Enfin, elle crée un fichier XML à partir des informations récupérées et l'enregistre dans le chemin d'output spécifié.
""" 

def parser_file_to_xml(target_path, output_path) :

    article = etree.Element("article")
    file_name = os.path.basename(target_path).replace(".txt", ".pdf")
    title = ""
    writer =""
    abstract = ""

    #Elle récupère ensuite le nom du fichier à parser et l'ajoute sous un noeud "preamble".
    preamble = etree.SubElement(article, "preamble")
    preamble.text = file_name

    file = open(target_path, "r")
    for i in range(2) :
        title = title + file.readline().strip('\n').strip() + " "
    
    for ligne in file :
       if(ligne.lower().find("abstract") != -1):         
          break;
       writer = writer + ligne.strip('\n').strip()
        	
    file.close()
    
    
    #Elle récupère ensuite le titre du fichier à parser et l'ajoute sous un noeud "titre".
    titre = etree.SubElement(article, "titre")
    titre.text = title
    
    #Elle récupère ensuite le nom d'auteur et l'ajoute sous un noeud "auteur".
    auteur = etree.SubElement(article, "auteur")
    auteur.text = writer

    #Elle récupère ensuite le resumé du fichier à parser et l'ajoute sous un noeud "abstract".
    abstract = etree.SubElement(article, "abstract")
    abstract.text = trouverParag(target_path, "abstract")

    #Elle récupère ensuite l'introduction du fichier à parser et l'ajoute sous un noeud "introduction".
    introduction = etree.SubElement(article, "introduction")
    introduction.text = trouverParag(target_path, "introduction")

    #Elle récupère ensuite le corps du fichier à parser et l'ajoute sous un noeud "corps".
    corps = etree.SubElement(article,"corps")
    corps.text = trouverCorps(target_path)

    #Elle récupère ensuite la conclusion du fichier à parser et l'ajoute sous un noeud "conclusion".
    conclusion = etree.SubElement(article, "conclusion")
    conclusion.text = trouverParag(target_path, "conclusion")

    #Elle récupère ensuite la discussion du fichier à parser et l'ajoute sous un noeud "discussion".
    discussion = etree.SubElement(article, "discussion")
    discussion.text = trouverDisc(target_path, "discussion")

    #Elle récupère ensuite les references bibliographiques du fichier à parser et l'ajoute sous un noeud "biblio".
    biblio = etree.SubElement(article, "biblio")
    biblio.text = trouverRef(target_path, "References")

    
    #Enregistrer des données dans un fichier XML et le rendre facilement lisible et compréhensible.
    xmlstr = ET.tostring(article).decode('utf8')
    newxml = md.parseString(xmlstr)
    with open(output_path, "a") as output:
        output.write(newxml.toprettyxml(indent='\t',newl='\n'))


   

def main():


    args = sys.argv
    filepath = args[2]   # on prends l'argument apres la commande python3 (chemin de dossier) si le code est dans le meme dossier des fichier il suffit just de mettre le nom de dossier  
    choix_option = args[1]

    dossier_txt = "dossierText"
    dossier_output = creerDossier("Resultat")
    
    files = trouver_ext(filepath,"pdf")
    
    pdf_to_txt(filepath)
    

    """
    choisir -t
    Cette fonction permet de parser les fichiers PDF et de créer des fichiers TXT correspondants.
    """  	
    if(choix_option == "-t"): 
    	
    	for file in files :
		
            File_txt_path = dossier_txt + "/" + os.path.basename(file).replace(".pdf", ".txt")
            output_path = dossier_output + "/" + os.path.basename(file).replace(".pdf", ".txt") 
            parser_file_to_txt(File_txt_path, output_path)


    """
    choisir -x
    Cette fonction permet de parser les fichiers PDF et de créer des fichiers XML correspondants.
    """
    if(choix_option == "-x"): 
    	for file in files :
            
            File_txt_path = dossier_txt  + "/" + os.path.basename(file).replace(".pdf", ".txt")
            
            output_path =  dossier_output + "/" + os.path.basename(file).replace(".pdf", ".xml")
            parser_file_to_xml(File_txt_path, output_path)

    
            
            

if __name__ == "__main__":
    main()
