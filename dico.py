
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
        reader = csv.DictReader(csvfile)
        for ligne in reader:
            donnes.append(ligne)
    return donnes
        
etablissements = recupere_donnes()





""""
1)Chaque élément de la liste est de type liste.
2:)Chaque élément de la liste contient 8 éléments.
3)le délimiteur est la virgule (,)
4)the_geom    objectid   insee comm     code et

"""

def filtrer(donnes, criteres, colonnes=None):
    resultat = []

    for info in donnes:
        flag = True
        for k, v in criteres.items():
            if info[k] != v:
                flag = False
        if flag == True:
            resultat.append(info)
    
    if colonnes:
        resultat_final = []
        for info in resultat:
            resultat_final.append({k: info[k] for k in colonnes if k in info})
        return resultat_final
    else:
        
        return resultat


print(filtrer(etablissements, {'COMMUNE':'CHATEAULIN'}))


 #[['FID',                       'the_geom',                      'OBJECTID'     'INSEE_COMM', 'COMMUNE', 'CODE_ET', 'NOM_ET', 'STATUT']

#['colleges_29.1', 'POINT (139542.9111092165 6796291.165203575)', '39', '29003', 'PLOUHINEC', '0330B',   'Locquéran',      'Public']




