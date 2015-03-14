Discuss this project on the [mailing list](http://groups.google.com/group/dataincubator)

# Useful links #
  * OpenLibrary site emits data as [JSON](http://openlibrary.org/b/OL7983950M/Weaving-the-Web.json) and (often broken) [RDF](http://openlibrary.org/b/OL7983950M/Weaving-the-Web.rdf)
  * It has a [RESTful API](http://openlibrary.org/dev/docs/restful_api) and provides  [dumps of all the data in JSON](http://openlibrary.org/static/jsondump/)
  * Thomas Francart's [Open Library wrapper](http://mondeca.wordpress.com/2009/01/05/openlibrary-api-rdf-wrapper-on-google-app-engine/), [details of mapping](https://spreadsheets.google.com/a/mondeca.com/ccc?key=prOEQ8nnfPsH5c7cBBMZzTg&hl=en) and [sample output 1](http://olrdf.appspot.com/key/b/OL7983950M.rdf), [sample output 2](http://olrdf.appspot.com/key/b/OL5218098M.rdf)
  * Rob Styles conversion notes: [part 1](http://blogs.talis.com/n2/archives/92) and [part 2](http://blogs.talis.com/n2/archives/101)
  * [other Open Library datasets](http://openlibrary.org/dev/docs/data)

Some interesting records:

  * http://openlibrary.org/b/OL7815034M/The-Colour-of-Magic - Audio Cassette, abridged edition
  * http://openlibrary.org/b/OL22632398M/colour-of-magic - paperback
  * http://openlibrary.org/b/OL7878387M/The-Colour-Of-Magic - hardback with first sentence
  * http://openlibrary.org/b/OL7985559M/The-Colour-of-Magic - Audio CD, unabridged
  * http://openlibrary.org/b/OL3691799M/Free-culture - lccn is linked
  * http://openlibrary.org/b/OL22859738M/Free-culture - table of contents
  * http://openlibrary.org/b/OL8682804M/Free-Software,-Free-Society - rich detail

# Proposed URI Structure #
  * http://ol.dataincubator.org/editions/{edition-id}
  * http://ol.dataincubator.org/works/{work-id}
  * http://ol.dataincubator.org/series/{series-id}
  * http://ol.dataincubator.org/sections/{section-id}
  * http://ol.dataincubator.org/people/{person-id}
  * http://ol.dataincubator.org/places/{place-id}
  * http://ol.dataincubator.org/events/{event-id}

# JSON Mapping #

These mappings are based heavily on Thomas Francart's mapping spreadsheet (linked above) and are implemented in [json2rdf.py](http://code.google.com/p/dataincubator/source/browse/trunk/ol/scripts/json2rdf.py)

| **JSON Key** | **Mapping** |
|:-------------|:------------|
| title | skos:prefLabel and rdfs:label as Literals |
| name | skos:prefLabel  |
| personal\_name | foaf:name |
| title\_prefix | ol:title\_prefix + ov:sortLabel  formed by removing ttitle\_prefix from the title |
| authors | Create a new group of type rdf:Seq and link with bibo:authorList property. Add each author as an item in the rdf:Seq |
| other\_titles | Create each one as a separate skos:altLabel |
| alternate\_names | Create each one as a separate skos:altLabel |
| subtitle | ov:subtitle |
| lc\_classifications | Create each one as a separate ol:lc\_classification |
| contributions | Create a new group of type rdf:Seq and link with bibo:contributorList property. Add each contributor as an item in the rdf:Seq |
| edition\_name | bibo:edition |
| subjects | Create each one as a separate dc:subject with a literal value (cleaned to remove some trailing punctuation) |
| publish\_country | ol:publish\_country |
| by\_statement | ol:by\_statement |
| oclc\_numbers and oclc\_number | Add each one using bibo:oclcnum, add foaf:isPrimaryTopicOf with a link to http://www.worldcat.org/oclc/{oclcnum}, create a new resource http://ol.dataincubator.org/oclc/{oclcnum} and link to resource with owl:sameAs |
| publishers | Create each one as a separate dc:publisher with a literal value |
| publish\_places | Create each one as a separate ol:publish\_place with a literal value |
| pagination | ol:pagination |
| lccn | Create each one as a separate bibi:lccn with a literal value |
| number\_of\_pages | ov:numberOfPages |
| isbn\_10 | Add each one using bibo:isbn10, add owl:sameAs with a link to http://www4.wiwiss.fu-berlin.de/bookmashup/books/{isbn}, create a new resource http://ol.dataincubator.org/isbn/{isbn} and link to resource with owl:sameAs |
| isbn\_13 | Add each one using bibo:isbn13, create a new resource http://ol.dataincubator.org/isbn/{isbn} and link to resource with owl:sameAs |
| uris and uri | rdfs:seeAlso |
| publish\_date | dct:issued |
| birth\_date | Create a new resource with URI http://ol.dataincubator.org/events/{event-id} and give it a type of bio:Birth and a bio:date, link to resource using bio:event |
| death\_date | Create a new resource with URI http://ol.dataincubator.org/events/{event-id} and give it a type of bio:Death and a bio:date, link to resource using bio:event |
| weight | ov:weight |
| physical\_format | Convert to rdf:type (see below) |
| physical\_dimensions | ol:physical\_dimensions |
| dewey\_decimal\_class | Create each one as a separate ol:dewey\_decimal\_class with a literal value |
| notes | rdfs:comment |
| bio | bio:olb |
| first\_sentence |  ov:firstSentence |
| wikipedia | foaf:isPrimaryTopicOf |
| ocaid | foaf:isPrimaryTopicOf |
| description | dct:description |
| series | Create a new resource with URI http://ol.dataincubator.org/series/{series-id} add dc:title for each value in JSON, link to resource with ol:series |
| languages | Use dct:langauage to link to http://ol.dataincubator.org/l/{language} |
| table\_of\_contents | Create a new group of type rdf:Seq and link with dct:tableOfContents property. Add each item as an item in the rdf:Seq |

The following namespace prefixes are used:
|  **prefix** | **URI** |
|:------------|:--------|
| rdf  | http://www.w3.org/1999/02/22-rdf-syntax-ns# |
| rdfs  | http://www.w3.org/2000/01/rdf-schema# |
| dcterms  | http://purl.org/dc/terms/ |
| ol  | http://olrdf.appspot.com/key/ |
| bibo  | http://purl.org/ontology/bibo/ |
| frbr  | http://purl.org/vocab/frbr/core# |
| skos  | http://www.w3.org/2004/02/skos/core# |
| foaf  | http://xmlns.com/foaf/0.1/ |
| dc  | http://purl.org/dc/elements/1.1/ |
| owl  | http://www.w3.org/2002/07/owl# |
| bio  | http://vocab.org/bio/0.1/ |
| ov  | http://open.vocab.org/terms/ |
| mo  | http://purl.org/ontology/mo/ |

The following JSON keys are ignored: [properties, kind, latest\_revision, id, last\_modified, created, revision, uri\_descriptions, genres, subject\_place, subject\_time, work\_title, work\_titles, isbn\_invalid, location, scan\_on\_demand

Physical formats are mapped to RDF classes where possible. Some cleaning and normalisation of the values is performed. The following is a comprehensive list of formats found in a 1% sample of the data, with mapped classes where assigned.

| **physical\_format value** | **class** |
|:---------------------------|:----------|
| map | bibo:Map |
| audio cd | mo:CD |
| mp3 cd | **TBD** |
| audio cassette | **TBD** |
| pamphlet | **TBD** |
| diskette | **TBD** |
| microform, microforme and microfrom | **TBD** |
| spoken word | **TBD** |
| paperback | **TBD** |
| mass market paperback | **TBD** |
| hardback and hardcover | **TBD** |
| turtleback | **TBD** |
| board book | **TBD** |
| rag book | **TBD** |
| calendar | **TBD** |
| sheet music | **TBD** |
| cd-rom | **TBD** |
| comic | **TBD** |
| cards | **TBD** |
| loose leaf | **TBD** |
| spiral-bound | **TBD** |
| ring-bound | **TBD** |
| plastic comb | **TBD** |
| library binding | **TBD** |
| electronic resource and computer file | **TBD** |
| video recording and "videorecording | **TBD** |
| pdf | **TBD** |
| graphic | **TBD** |
| textbook binding | **TBD** |
| unknown binding | **TBD** |




# Other Data to Mix In #

  * [LibraryThing's ISBN database](http://www.librarything.com/thingology/2007/03/thingisbn-data-in-one-file.php)