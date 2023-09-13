import mysql.connector 
import xml.etree.ElementTree as ET
import lxml.etree as ET
from pymongo import MongoClient
import re #pour extraire le numero de la rue de l'adresse
import pymongo

from pymongo import MongoClient
from lxml import etree


#todo ---------------------------------------------  MySQL to XML  ---------------------------------------------#


#* Connexion à la base de données MySQL
Connexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="isib",
    database="classicmodels"
)


#* Je crèe un curseur pour manipuler les lignes retournées par mes requetes
cursor = Connexion.cursor()

#* Sélection des clients dans la base de données,
# ici je récupère les informations sur les 10 premiers clients
requete_sql = "SELECT customerNumber, customerName, contactLastName, contactFirstName, phone, country, city, addressLine1, postalCode FROM customers LIMIT 10"
cursor.execute(requete_sql)

#* Création de l'élément racine XML, c'est l'élément principal qui contiendra tous les autres élements
# Dans ce contexte je manipule des clients, donc je nomme ma racine "clients"
root = ET.Element("clients")

#* Ici je vais creer plusieurs client pour chaque client qui me sera retourné par requete_SQL (j'en recupere 10)
for client in cursor:
    
    # pour commencer je vais extraire les info de chaque client à partir de ma requete et je les stocks dans client
    # un client est un tuple(respect de l'ordre de mes champs dans la requete)
    # id = customerNumber, contact = customerName, nom = contactLastName, prenom = contactFirstName, phone = phone, pays = country, ville = city, rue = addressLine1, postal_code = postalCode
    id, contact, nom, prenom, phone, pays, ville, rue, postal_code = client #tuple 
    
    
    #* libreire re Ici pour avoir une adresse correcte je vais extraire le numero de la rue de l'adresse
    address_number = re.search(r'\d+', rue) 
    
    if address_number:
        #? print(rue) #pour verifier que j'ai extriat la rue
        address_number = address_number.group() 
        #? print(address_number) #pour verifier que j'ai bien extrait le numero des rues
        rue = rue.replace(address_number, '') 
        #?print(rue) #pour verifier que j'ai bien supprimé le numero des rues

    #* je crée l'élément client
    # il est positionné en dessous du root et a un id qui correspond au customerNumber
    customer_element = ET.SubElement(root, "client", id=str(id))
    
    #* pour construire mon arbre XML je vais creer plusieurs sous elements
    # je cree la balise contact qui est un sous element de client
    contact_sub_element = ET.SubElement(customer_element, "contact")
    
    #je cree la balise nom qui est un sous element de contact
    nom_sub_sub_element = ET.SubElement(contact_sub_element, "nom")
    #je remplis la balise nom avec le nom du client recupere dans la requete
    nom_sub_sub_element.text = nom
    
    #je cree la balise prenom qui est un sous element de contact
    prenom_sub_sub_element = ET.SubElement(contact_sub_element, "prenom")
    prenom_sub_sub_element.text = prenom
    
    #je cree la balise telephone qui est un sous element de contact
    phone_sub_sub_element = ET.SubElement(contact_sub_element, "telephone")
    phone_sub_sub_element.text = phone
    
    #je cree la balise addresse qui est un sous element de client
    address_sub_element = ET.SubElement(customer_element, "addresse")
     
    pays_sub_sub_element = ET.SubElement(address_sub_element, "pays")
    pays_sub_sub_element.text = pays
    
    #je cree la balise ville qui est un sous element de addresse
    ville_sub_sub_element = ET.SubElement(address_sub_element, "ville")
    ville_sub_sub_element.text = ville
    
    #je cree la balise rue qui est un sous element de addresse
    address_line1_sub_sub_element = ET.SubElement(address_sub_element, "rue")
    address_line1_sub_sub_element.text = rue
    
    #je cree la balise numero qui est un sous element de addresse
    address_number_sub_sub_element = ET.SubElement(address_sub_element, "numero")
    address_number_sub_sub_element.text = address_number
    
    #je cree la balise code_postal qui est un sous element de addresse
    postal_code_element = ET.SubElement(address_sub_element, "cp")
    postal_code_element.text = postal_code


# Écriture du XML dans un fichier, construction de l'arbre XML
tree = ET.ElementTree(root)
tree.write("customers.xml")

# toujours fermer le curseur et la connexion
cursor.close()
Connexion.close()

print("1. MySQL >>>> XML ")


# todo -----------------------VERIFICATEUR------------------------------------------"

try:

    # todo 1 : Charger le fichier XSD, qui gere le schema de mon fichier XML
    xsd_file = ET.parse("customers.xsd").getroot()
    #?print(xsd_file)
    # je crée un objet XMLSchema, il sert à de valider mon fichier XML qui est coinstruit au dessus
    XMLSchema  = ET.XMLSchema(xsd_file)
    #?print(xsd)

    # todo 2 : Charger le fichier XML
    xml_file = ET.parse("customers.xml").getroot()

    # todo 3 : Vérifier si le fichier XML respecte le schéma XSD
    XMLSchema .assertValid(xml_file)

    # Imprimer un message si la validation a échoué
    print("2. VERIFICATEUR : Le fichier XML respecte le schéma XSD")  
    
except ET.DocumentInvalid as error:
    # Imprimer un message d'erreur en cas d'échec de validation
    print("2. Le fichier XML ne respecte pas le schéma XSD :")
    print(error)
    
#todo ---------------------------------------------  XML to mongo  ---------------------------------------------#



#* Connexion à la db mongo compass
client = MongoClient("mongodb://localhost:27017/")
db = client["DB_CRUD"]
collection = db["app4"]

#* Suppression des données de la collection, si non quand je vais avoir des doublont à chaque fois que je relance le script
collection.delete_many({})

# Parsing du fichier XML pour pouvoir lire et manipuler son contenu
tree = ET.parse('customers.xml')
#?print(tree)
root = tree.getroot()
#?print(root)

#* Insertion des data dans la collection
# je recupere les data de chaque client 
for client in root.findall('client'):
    
    id = int(client.attrib['id']) # je recupere la valeur de l'attribut id dans balise client
    
    nom = client.find('contact/nom').text.strip() #text.strip() pour supprimer les espaces
    prenom = client.find('contact/prenom').text.strip()
    telephone = client.find('contact/telephone').text.strip()

    pays = client.find('addresse/pays').text.strip()
    ville = client.find('addresse/ville').text.strip()
    rue = client.find('addresse/rue').text.strip()
    numero = int(client.find('addresse/numero').text.strip())
    cp = int(client.find('addresse/cp').text.strip())

    # construction de l'objet customer avec des sous objets
    customer = {
        "id": id,
        "contact": {
            "nom": nom,
            "prenom": prenom,
            "telephone": telephone
        },
        "adresse": {
            "pays": pays,
            "ville": ville,
            "rue": rue,
            "numero": numero,
            "cp": cp
        }
    }
    
    # construction de l'objet customer comme une liste
    customer1 = {
        "id": id,
        "nom": nom,
        "prenom": prenom,
        "telephone": phone,
        "pays": pays,
        "ville": ville,
        "rue": rue,
        "numero": numero,
        "cp": cp
    }

    # j'insert les data dans la collection
    collection.insert_one(customer)
    collection.insert_one(customer1)

print("3. XML >>>> MongoDB ")


# todo -----------------------  XSLT >>> HTML ------------------------------------------"

#je charge le fichier XML
xml_file = etree.parse('customers.xml')

# je charge le XSL
xsl_file = etree.parse('customers2.xsl')

# création d'un transformateur XSLT qui va transformer le fichier XML en HTML
transformateur = etree.XSLT(xsl_file)  
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
# je fais la transformation du XSLT au fichier XML
final_file = transformateur(xml_file)

# ecriture du fichier HTML
with open('customers.html', 'wb') as file: #wb pour ecrire en binaire 
    file.write(final_file)

print("4. XSLT >>>>>> HTML")