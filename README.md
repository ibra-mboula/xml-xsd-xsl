# xml-xsd-xsl

Ce projet réalise un flux complet de traitement de données :

- Importation de JSON : Les données sont d'abord récupérées à partir d'un fichier JSON.

- Transformation en XML : Les données JSON sont ensuite transformées en format XML.

- Validation avec XSD : Avant l'enregistrement, le contenu XML est vérifié par rapport à un schéma XSD pour assurer sa conformité.

- Stockage dans MongoDB : Une fois validées, les données XML sont stockées dans une base de données MongoDB.

- Transformation XSLT en HTML : Les données stockées sont également transformées en HTML à l'aide de XSLT pour une visualisation et une interaction utilisateur possibles.




