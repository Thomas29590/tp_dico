
# importation des bibliothèques nécessaires
import requests
import os
import csv
import pandas as pd
import folium
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
    with open(local_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        colonnes_attendues = reader.fieldnames
        nb_colonnes = len(colonnes_attendues)
        for ligne in reader:
            if len(ligne) != nb_colonnes:
                print(f"Ligne invalide (mauvais nombre de colonnes) : {ligne}")
                continue 
            ligne_convertie = {}
            for cle, valeur in ligne.items():
                if cle in ['latitude', 'longitude', 'y', 'x']: 
                    ligne_convertie[cle] = float(valeur) if valeur else 0.0
                elif cle in ['nombre_eleves', 'identifiant', 'code_postal']: 
                    ligne_convertie[cle] = int(valeur) if valeur else 0
                else:  
                    ligne_convertie[cle] = valeur
            donnes.append(ligne_convertie)
    
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


#return(filtrer(etablissements, {'COMMUNE':'CHATEAULIN', 'STATUT' : 'Privé', }))


 #[['FID',                       'the_geom',                      'OBJECTID'     'INSEE_COMM', 'COMMUNE', 'CODE_ET', 'NOM_ET', 'STATUT']

#['colleges_29.1', 'POINT (139542.9111092165 6796291.165203575)', '39', '29003', 'PLOUHINEC', '0330B',   'Locquéran',      'Public']


    """_
  
def trier(donnees, criteres):
    #Retourne les données triées selon criteres
    def multi_criteres(donnees):
        result = []
        for c in criteres:
            result.append(donnees[c])
        return result
   
    return sorted(donnees, key=multi_criteres)

etablissements = recupere_donnes()
#print(etablissements[0:10])
results = trier(etablissements, ['COMMUNE', 'STATUT'])
for result in results:
    print(result)
  """

url = "https://www.data.gouv.fr/fr/datasets/r/bf9d46b1-5430-4866-ab7d-58a4d794324d"
colleges_morbihan = pd.read_csv(url, delimiter=';', encoding='iso 8859-15')




local_file = "geolocalisation.csv"
if not local_file in os.listdir():
    url = "https://data.education.gouv.fr/explore/dataset/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B"
    data = requests.get(url).content
    with open(local_file, 'wb') as csvfile:
        csvfile.write(data)
geolocalisations = pd.read_csv(local_file, delimiter = ";")





mapper = {'numero_uai':'CODE',}

geolocalisations.rename(columns=mapper, inplace=True)

print(geolocalisations)



f =colleges_morbihan.merge(geolocalisations, on=['CODE'], how='left')

colleges_morbihan = f
pd.set_option('display.max_rows',90)
pd.set_option('display.max_columns',20)
print(f)

m = folium.Map([47.676116620401416,-2.7710275095710846], zoom_start=12)



for i in f.index :
    p = f["position"][i]
    if str(p) != "nan":
        latitude , longitude = p.split(",")
        folium.Marker(
            location=[float(latitude), float(longitude)],
            tooltip="Click me!",
            popup=f["ADRESSE"][i],
            icon=folium.Icon(color="red"),
        ).add_to(m)

m.save('test.html')