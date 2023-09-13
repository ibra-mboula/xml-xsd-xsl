# xml-xsd-xslt

1. MySQL >>>> XML
2. VERIFICATEUR : Le fichier XML respecte le schéma XSD
3. XML >>>> MongoDB
4. XSLT >>>>>> HTML

Ce projet réalise un flux complet de traitement de données :

- Extraction depuis MySQL : Les données sont d'abord extraites d'une base de données MySQL.
  
- Transformation en XML : Les données extraites sont ensuite transformées en format XML.
  
- Validation avec XSD : Avant l'enregistrement, le contenu XML est vérifié par rapport à un schéma XSD pour assurer sa conformité.
  
- Stockage dans MongoDB : Une fois validées, les données XML sont stockées dans une base de données MongoDB.

- Transformation XSLT en HTML : Les données stockées sont également transformées en HTML à l'aide de XSLT pour une visualisation et une interaction utilisateur possibles.




