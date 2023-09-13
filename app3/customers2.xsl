<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="html" encoding="UTF-8" />
    <xsl:template match="/">
        <html>
            <head>
                <title>Liste des clients</title>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" />
            </head>
            <body>
                <div class="container">
                    <h1 class="my-4">Liste des clients</h1>
                    <!-- https://getbootstrap.com/docs/5.3/content/tables/ -->
                    <table class="table table-striped-columns">
                        <tr> <!-- ligne de titre -->
                            <th>ID</th>  <!-- colonne de titre -->
                            <th>Nom</th>
                            <th>Prénom</th>
                            <th>Téléphone</th>
                            <th>Pays</th>
                            <th>Ville</th>
                            <th>Rue</th>
                            <th>Numéro</th>
                            <th>Code postal</th>
                        </tr>

                        <xsl:for-each select="clients/client"> <!-- clients/client, pour chaque client dans clients -->
                            <tr>
                                <td><xsl:value-of select="@id"/></td> <!-- @id = attribut id -->
                                <td><xsl:value-of select="contact/nom"/></td>   <!-- contact/nom = balise nom dans le fichier xml -->
                                <td><xsl:value-of select="contact/prenom"/></td>
                                <td><xsl:value-of select="contact/telephone"/></td>
                                <td><xsl:value-of select="addresse/pays"/></td>
                                <td><xsl:value-of select="addresse/ville"/></td>
                                <td><xsl:value-of select="addresse/rue"/></td>
                                <td><xsl:value-of select="addresse/numero"/></td>
                                <td><xsl:value-of select="addresse/cp"/></td>
                            </tr>
                        </xsl:for-each>
                    </table>
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
