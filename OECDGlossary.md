# Introduction #

Add your content here.

# Access #

The OECD provide a [web service](http://stats.oecd.org/glossary/webservice.asp) to get the data in XML:
[Sample Data](http://stats.oecd.org/glossary/filter.asp?cET=A&tET=&vED=ON&cED=A&tED=&vEC=ON&cEC=A&tEC=&vFT=ON&cFT=A&tFT=&vFD=ON&cFD=A&tFD=&vFC=ON&cFC=A&tFC=&vP=ON&cP=A&tP=&vU=ON&cU=A&tU=&vS=ON&cS=All&vV=ON&cV=All&vC=ON&cC=All&vT=ON&cT=All&vO=ON&cO=All&vI=ON&Idd=dd&Imm=mm&Iyy=yyyy&vE=ON&Edd=dd&Emm=mm&Eyy=yyyy&vCR=ON&format=martif&vL=ON&cL=All&No=50&SUBMIT.x=10&SUBMIT.y=24&CurPage=1)

Change the CurPage field at the end of the URL to get pages 2, 3, 4 etc. The last page number is 139.

# Sample Data #

This is what one of the entries looks like in XML:

```
<termEntry id="16">

  <descrip type="EnglishDefinition">
    Accrual accounting records flows at the time economic value is created, transformed, exchanged, transferred or extinguished; this means that flows which imply a change of ownership are entered when ownership passes, services are recorded when provided, output is entered at the time products are created and intermediate consumption is recorded when materials and supplies are being used
  </descrip>

  <descrip type="EnglishContext">
    Recognition in financial accounts of the implications of transactions (or decisions giving rise to transactions) when they occur irrespective of when cash is paid or received.  (The OECD Economic Outlook: Sources and Methods.  Available at http://www.oecd.org/eco/sources-and-methods).
  </descrip>
  <descrip type="FrenchDefinition"/>
  <descrip type="FrenchContext"/>
  <descrip type="SourcePublication">SNA 3.94</descrip>
  <descrip type="Hyperlink">http://esa.un.org/unsd/sna1993/introduction.asp</descrip>
  <descrip type="Source">OECD-STD-NAD-National Accounts</descrip>
  <descrip type="VersionIndicator"/>
  <descrip type="ClassificationIndicator"/>
  <descrip type="Theme">National accounts</descrip>
  <descrip type="GlossaryOutputSegmentCodes">Economic Outlook</descrip>
  <descrip type="CrossReference" id="682">Due-for-payment recording</descrip>
  <descrip type="CrossReference" id="7306">Modified accrual accounting</descrip>
  <descrip type="CrossReference" id="290">Cash accounting</descrip>
  <descrip type="Legacy">False</descrip>
  <descrip type="DateAdded">Tuesday, September 25, 2001</descrip>
  <descrip type="DateUpdated">Thursday, July 26, 2007</descrip>
  <langSet xml:lang="en">
    <ntig>
      <termGrp>
        <term>Accrual accounting</term>
      </termGrp>
    </ntig>
  </langSet>
  <langSet xml:lang="fr">
    <ntig>
      <termGrp>
        <term>Comptabilité sur la base des droits et obligations</term>
      </termGrp>
    </ntig>
  </langSet>
</termEntry>
```

# RDF Mapping #

This is what that entry needs to look like in RDF/XML:

```
<rdf:RDF
  xmlns:skos="http://www.w3.org/2004/02/skos/core#"
  xmlns:dct="http://purl.org/dc/terms/"
  xmlns:foaf="http://xmlns.com/foaf/0.1/"
  >
 
  <!-- the 16 comes from the termEntry id attribute -->
  <skos:Concept about="http://example.org/oecd-glossary/concepts/16">
   
    <!-- use the termEntry id attribute at the end of this URL -->
    <foaf:isPrimaryTopicOf rdf:resource="http://stats.oecd.org/glossary/detail.asp?ID=16"/>
   
   
    <!-- this comes from the first langSet -->
    <skos:prefLabel xml:lang="en">Accrual accounting</skos:prefLabel>

    <!-- this comes from the second langSet -->
    <skos:prefLabel xml:lang="fr">Comptabilité sur la base des droits et obligations</skos:prefLabel>

    <!-- these are from the EnglishDefinition and EnglishContext. if there were french ones then these would be repeated with xml:lang="fr" -->
    <skos:definition xml:lang="en">Accrual accounting records flows at the time economic value is created, transformed, exchanged, transferred or extinguished; this means that flows which imply a change of ownership are entered when ownership passes, services are recorded when provided, output is entered at the time products are created and intermediate consumption is recorded when materials and supplies are being used</skos:definition>
    <skos:scopeNote xml:lang="en">Recognition in financial accounts of the implications of transactions (or decisions giving rise to transactions) when they occur irrespective of when cash is paid or received.  (The OECD Economic Outlook: Sources and Methods.  Available at http://www.oecd.org/eco/sources-and-methods).</skos:scopeNote>
   
    <!-- these come from the CrossReference -->
    <skos:related rdf:resource="http://example.org/oecd-glossary/concepts/682" />
    <skos:related rdf:resource="http://example.org/oecd-glossary/concepts/7306" />
    <skos:related rdf:resource="http://example.org/oecd-glossary/concepts/290" />
 
    <!-- this is from DateAdded, note that the format is different. this is called iso -->
    <dct:issued rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2001-09-25</dct:issued>
 
    <!-- this is from DateUpdated -->
    <dct:modified rdf:datatype="http://www.w3.org/2001/XMLSchema#date">2007-07-26</dct:modified>
 
    <!-- the dct:title attribute comes from SourcePublication, the rdf:resource attribute comes from Hyperlink
         if there is no hyperlink then don't add the rdf:resource attribute -->  
    <dct:source rdf:resource="http://esa.un.org/unsd/sna1993/introduction.asp" dct:title="SNA 3.94"/>
 
  </skos:Concept>

  <!-- this is from GlossaryOutputSegmentCodes -->
  <!-- use the slugify function from http://www.djangosnippets.org/snippets/29/ to turn the text into the bit at the end of the URL -->
  <skos:Collection rdf:about="http://example.org/oecd-glossary/segments/economic-outlook">
    <skos:prefLabel xml:lang="en">Economic Outlook</skos:prefLabel>
    <skos:member rdf:resource="http://example.org/oecd-glossary/concepts/16" />
  </skos:Collection>

  <!-- this is from Theme -->
  <skos:Collection rdf:about="http://example.org/oecd-glossary/themes/national-accounts">
    <skos:prefLabel xml:lang="en">National accounts</skos:prefLabel>
    <skos:member rdf:resource="http://example.org/oecd-glossary/concepts/16" />
  </skos:Collection>

</rdf:RDF>
```