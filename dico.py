# importation des bibliothèques nécessaires
import requests
import os
import csv

def recupere_donnes():
    """
    Retourne les données sous forme d'une liste de dictionnaires
    """
    local_file = "college_finistere.csv" #nom donné au fichier
    # recuperation des données depuis l'url
    if not os.path.exists(local_file):
        print("Je Telecharge")
        url = "https://geobretagne.fr/geoserver/cd29/wfs?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=cd29%3Acolleges_29&OUTPUTFORMAT=csv"
        data = requests.get(url).content # on récupère les données sous forme de bytes
        # création d'un fichier et écriture des données
        with open(local_file, 'wb') as csvfile: # 'w' pour write et 'b' pour bytes
            csvfile.write(data)
    
    donnes = []
    # ouverture du fichier précédemment créé
    with open(local_file) as csvfile:
        reader = csv.reader(csvfile)
        for ligne in reader:
            donnes.append(ligne)
    return donnes
        
etablissements = recupere_donnes()
print(etablissements[0:10])




""""
1)Chaque élément de la liste est de type liste.
2:)Chaque élément de la liste contient 8 éléments.
3)le délimiteur est la virgule (,)
4)the_geom    objectid   insee comm     code et

"""

def filtre(donnees, criteres):
    resultat = []
    for item in donnees:
        # Vérifier si tous les critères sont satisfaits pour chaque dictionnaire
        if all(item.get(cle) == valeur for cle, valeur in criteres.items()):
            resultat.append(item)
    return resultat