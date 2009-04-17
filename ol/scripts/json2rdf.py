import json
import optparse
import os
import rdflib
import sys
import tarfile
import urllib2

#import rdfoutput
BASE_URI = "http://ol.dataincubator.org"
#rdfoutput.register("bibo", "http://purl.org/ontology/bibo/")
#rdfoutput.register("ol", "http://olrdf.appspot.com/key/")
rdf = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")
dcterms = rdflib.Namespace("http://purl.org/dc/terms/")
ol = rdflib.Namespace("http://olrdf.appspot.com/key/")
bibo = rdflib.Namespace("http://purl.org/ontology/bibo/")
frbr = rdflib.Namespace("http://purl.org/vocab/frbr/core#")
skos = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
foaf = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
dc = rdflib.Namespace("http://purl.org/dc/elements/1.1/")
owl = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
ex = rdflib.Namespace("http://example.org/terms/")
bio = rdflib.Namespace("http://vocab.org/bio/0.1/")
skip = ["properties", "kind", "latest_revision", "id", "last_modified", "created", "revision", "uri_descriptions", "genres", "subject_place", "subject_time", "work_title", "work_titles", "isbn_invalid", "location"]
class Converter:
  resource_index = 0
  
  def __init__(self):
    self.graph = rdflib.ConjunctiveGraph()
    self.graph.bind("rdf", rdf)
    self.graph.bind("rdfs", rdfs)
    self.graph.bind("dct", dcterms)
    self.graph.bind("ol", ol)
    self.graph.bind("bibo", bibo)
    self.graph.bind("frbr", frbr)
    self.graph.bind("skos", skos)
    self.graph.bind("foaf", foaf)
    self.graph.bind("dc", dc)
    self.graph.bind("owl", owl)
    self.graph.bind("ex", ex)
    self.graph.bind("bio", bio)
  def convert(self, indata):
    data = json.read(indata)
    
    if data["key"].startswith("/user/"):
      return

    if data["type"]["key"] == "/type/redirect" or data["type"]["key"] == "/type/type" or data["type"]["key"] == "/type/delete" or data["type"]["key"] == "/type/scan_record":
      #print "Ignoring '%s' because it is a '%s'" % (data["key"], data["type"]["key"]) 
      return
    
    # Define a URI for the item itself
    item_uri = self.make_uri("items")
    
    subj = rdflib.URIRef(item_uri)
    
    
    # Temporarily add the original JSON
    self.graph.add((subj, rdfs["comment"], rdflib.Literal(indata)))
    
    # Connect the item resource to the OpenLibrary document describing it
    ol_document = rdflib.URIRef("http://openlibrary.org" + data["key"])
    self.graph.add((subj, foaf["isPrimaryTopicOf"], ol_document))
    self.graph.add((ol_document, rdf["type"], foaf["Document"]))
    
    for k, v in data.items():
      if k == "key":
        pass
      elif k == "type":
        if v["key"] == "/type/edition":
          self.graph.add((subj, rdf["type"], frbr["Manifestation"]))
        elif v["key"] == "/type/author":
          self.graph.add((subj, rdf["type"], foaf["Person"]))
        else:
          print "Unknown type '%s'" % (v["key"])
          #self.graph.add((subj, rdf["type"], rdflib.URIRef(BASE_URI + v["key"])))
      elif k == "title":
        self.graph.add((subj, rdfs["label"], rdflib.Literal(v)))
        self.graph.add((subj, skos["prefLabel"], rdflib.Literal(v)))
      elif k == "name":
        self.graph.add((subj, skos["prefLabel"], rdflib.Literal(v)))
      elif k == "personal_name":
        self.graph.add((subj, foaf["name"], rdflib.Literal(v)))
      elif k == "title_prefix":
        self.graph.add((subj, ol["title_prefix"], rdflib.Literal(data["title_prefix"])))
        sort_title = data["title"][len(data["title_prefix"]):].strip()
        self.graph.add((subj, ol["sort_title"], rdflib.Literal(sort_title)))
      elif k == "authors":
        group_resource = rdflib.URIRef(self.make_uri("groups"))
        self.graph.add((subj, bibo["authorList"], group_resource))
        self.graph.add((group_resource, rdf["type"], rdf["Seq"]))
        i = 1
        for author in v:
          person_resource = rdflib.URIRef(self.make_uri("people"))
          self.graph.add((group_resource, rdf["_" + str(i)], person_resource))
          self.graph.add((person_resource, rdf["type"], foaf["Person"]))
          if isinstance(author, (str, unicode)):
            self.graph.add((person_resource, foaf["name"], rdflib.Literal(author)))
          else:
            self.graph.add((person_resource, foaf["isPrimaryTopicOf"], rdflib.URIRef("http://openlibrary.org" + author["key"])))
          i += 1
      elif k == "other_titles":
        for t in v:
          self.graph.add((subj, skos["altLabel"], rdflib.Literal(t)))
      elif k == "alternate_names":
        for t in v:
          self.graph.add((subj, skos["altLabel"], rdflib.Literal(t)))
      elif k == "subtitle":
        self.graph.add((subj, ol["subtitle"], rdflib.Literal(v)))
      elif k == "lc_classifications":
        for c in v:
          self.graph.add((subj, ol["lc_classification"], rdflib.Literal(c)))
      elif k == "contributions":
        group_resource = rdflib.URIRef(self.make_uri("groups"))
        self.graph.add((subj, bibo["contributorList"], group_resource))
        self.graph.add((group_resource, rdf["type"], rdf["Bag"]))
        i = 1
        for c in v:
          person_resource = rdflib.URIRef(self.make_uri("people"))
          self.graph.add((group_resource, rdf["_" + str(i)], person_resource))
          self.graph.add((person_resource, rdf["type"], foaf["Person"]))
          if isinstance(c, (str, unicode)):
            self.graph.add((person_resource, foaf["name"], rdflib.Literal(c)))
          else:
            self.graph.add((person_resource, foaf["isPrimaryTopicOf"], rdflib.URIRef("http://openlibrary.org" + c["key"])))
          i += 1
      elif k == "edition_name":
        self.graph.add((subj, bibo["edition"], rdflib.Literal(v)))
      elif k == "subjects":
        for sub in v:
          self.graph.add((subj, dc["subject"], rdflib.Literal(sub)))
      elif k == "publish_country":
        self.graph.add((subj, ol["publish_country"], rdflib.Literal(v.strip())))
      elif k == "by_statement":
        self.graph.add((subj, ol["by_statement"], rdflib.Literal(v)))
      elif k == "oclc_numbers" or k == "oclc_number":
        for n in v:
          self.graph.add((subj, bibo["oclcnum"], rdflib.Literal(n)))
          self.graph.add((subj, foaf["isPrimaryTopicOf"], rdflib.URIRef("http://www.worldcat.org/oclc/" + n)))
          oclc_resource = rdflib.URIRef(BASE_URI + "/oclc/" + str(n))
          self.graph.add((subj, owl["sameAs"], oclc_resource))
          self.graph.add((oclc_resource, owl["sameAs"], subj))
          self.graph.add((oclc_resource, ex["canonicalUri"], rdflib.Literal(item_uri)))
      elif k == "publishers":
        for p in v:
          self.graph.add((subj, dc["publisher"], rdflib.Literal(p)))
      elif k == "publish_places":
        for p in v:
          self.graph.add((subj, ol["publish_place"], rdflib.Literal(p)))
      elif k == "pagination":
        self.graph.add((subj, ol["pagination"], rdflib.Literal(v)))
      elif k == "lccn":
        for l in v:
          self.graph.add((subj, bibo["lccn"], rdflib.Literal(l)))
      elif k == "number_of_pages":
        self.graph.add((subj, ol["number_of_pages"], rdflib.Literal(str(v))))
      elif k == "isbn_10":
        for i in v:
          self.graph.add((subj, bibo["isbn10"], rdflib.Literal(i)))
          self.graph.add((subj, owl["sameAs"], rdflib.URIRef("http://www4.wiwiss.fu-berlin.de/bookmashup/books/" + i)))

          isbn_resource = rdflib.URIRef(BASE_URI + "/isbn/" + str(i))
          self.graph.add((subj, owl["sameAs"], isbn_resource))
          self.graph.add((isbn_resource, owl["sameAs"], subj))
          self.graph.add((isbn_resource, ex["canonicalUri"], rdflib.Literal(item_uri)))
      elif k == "isbn_13":
        for i in v:
          self.graph.add((subj, bibo["isbn13"], rdflib.Literal(i)))
          isbn_resource = rdflib.URIRef(BASE_URI + "/isbn/" + str(i))
          self.graph.add((subj, owl["sameAs"], isbn_resource))
          self.graph.add((isbn_resource, owl["sameAs"], subj))
          self.graph.add((isbn_resource, ex["canonicalUri"], rdflib.Literal(item_uri)))
      elif k == "uris" or k == "url":
        for i in v:
          self.graph.add((subj, rdfs["seeAlso"], rdflib.URIRef(str(i))))
            
      elif k == "publish_date":
        self.graph.add((subj, dcterms["issued"], rdflib.Literal(v)))
      elif k == "birth_date":
        event_resource = rdflib.URIRef(self.make_uri("events"))
        self.graph.add((subj, bio["event"], event_resource))
        self.graph.add((event_resource, rdf["type"], bio["Birth"]))
        self.graph.add((event_resource, bio["date"], rdflib.Literal(v)))
      elif k == "death_date":
        event_resource = rdflib.URIRef(self.make_uri("events"))
        self.graph.add((subj, bio["event"], event_resource))
        self.graph.add((event_resource, rdf["type"], bio["Death"]))
        self.graph.add((event_resource, bio["date"], rdflib.Literal(v)))
      elif k == "weight":
        self.graph.add((subj, ol["weight"], rdflib.Literal(v)))
      elif k == "physical_format":
        self.graph.add((subj, ol["physical_format"], rdflib.Literal(v)))
      elif k == "physical_dimensions":
        self.graph.add((subj, ol["physical_dimensions"], rdflib.Literal(v)))
      elif k == "dewey_decimal_class":
        for d in v:
          self.graph.add((subj, ol["dewey_decimal_class"], rdflib.Literal(d)))
      elif k == "notes":
        self.graph.add((subj, ol["notes"], rdflib.Literal(v["value"])))
      elif k == "bio":
        self.graph.add((subj, bio["olb"], rdflib.Literal(v["value"])))
      elif k == "first_sentence":
        self.graph.add((subj, ol["first_sentence"], rdflib.Literal(v["value"])))
      elif k == "wikipedia":
        self.graph.add((subj, foaf["isPrimaryTopicOf"], rdflib.URIRef(v)))
        # TODO: more specific wikipedia property?
      elif k == "ocaid":
        self.graph.add((subj, foaf["isPrimaryTopicOf"], rdflib.URIRef("http://www.archive.org/details/" + v)))
        # TODO: add links to scanned content in internet archive
        # directory of files: http://ia360913.us.archive.org/1/items/{ocaid}/
        # xml description of files: http://ia360913.us.archive.org/1/items/{ocaid}/{ocaid}_files.xml
        # PDF scan: http://www.archive.org/download/{ocaid}/{ocaid}.pdf
        # Full text: http://www.archive.org/stream/{ocaid}/{ocaid}_djvu.txt
      elif k == "description":
        self.graph.add((subj, dcterms["description"], rdflib.Literal(v["value"])))
      elif k == "series":
        for s in v:
          self.graph.add((subj, ol["series"], rdflib.Literal(s)))
      elif k == "languages":
        for l in v:
          self.graph.add((subj, dcterms["language"], rdflib.URIRef(BASE_URI + l["key"])))
      elif k == "table_of_contents":
        toc_resource = rdflib.URIRef(self.make_uri("tocs"))
        self.graph.add((subj, dcterms["tableOfContents"], toc_resource))
        self.graph.add((toc_resource, rdf["type"], rdf["Seq"]))
        i = 1
        for x in v:
          section = rdflib.URIRef(self.make_uri("sections"))
          if isinstance(x, (str, unicode)):
            x = {"type" : "/type/text", "value" : x}
          elif x["type"] == "/type/toc_item":
            try:
              self.graph.add((section, skos["prefLabel"], rdflib.Literal(x["title"])))
            except KeyError:
              continue
          elif x["type"] == "/type/text":
            self.graph.add((section, skos["prefLabel"], rdflib.Literal(x["value"])))
          self.graph.add((section, rdf["type"], bibo["DocumentPart"]))
          self.graph.add((section, dcterms["isPartOf"], subj))
          self.graph.add((toc_resource, rdf["_" + str(i)], section))
          i += 1
      elif k in skip:
        pass
      else:
        print "  Did not process '%s':'%s'" % (k, v)
    #rdfoutput.make_table(triples)
    #rdfoutput.make_graph(triples)
  
  def clear(self):
    self.graph = rdflib.ConjunctiveGraph()
  
  def get_graph(self):
    return self.graph 
    
  def make_uri(self, prefix):
    self.resource_index = self.resource_index + 1
    return BASE_URI + "/" + prefix + "/" + str(self.resource_index)
  
if __name__ == "__main__":
  p = optparse.OptionParser()
  p.set_defaults(batch_size=800, compress=False, format="xml")
  p.add_option("-b", "--batch-size", action="store", type="int", dest="batch_size", metavar="BATCH_SIZE", help="specify the size of each batch")
  p.add_option("-c", "--compress", action="store_true", dest="compress", help="compress the output using TAR-GZ compression")
  p.add_option("-x", "--xml", action="store_const", const="xml", dest="format", help="save output as XML")
  p.add_option("-p", "--pretty-xml", action="store_const", const="pretty-xml", dest="format", help="save output as pretty XML")
  p.add_option("-n", "--ntriples", action="store_const", const="nt", dest="format", help="save output as NTriples")
  opts, args = p.parse_args()
  
  if len(args) < 2:
    p.print_usage()
  
  batch_size = opts.batch_size
  input_filename = args[0]
  output_filename = args[1]
  output_format = opts.format
  compress = opts.compress
  output_filename_parts = output_filename.split(".")

  bad_record_filename = output_filename_parts[0] + "_bad.json"
  bad_record_file = open(bad_record_filename, "w")

  f = open(input_filename, "r")
  error_count = 0
  count = 0
  triple_count = 0
  batch = 1
  for line in f:
    if count % batch_size == 0:
      if count > 0:
        batch_delim = "_" + str(batch) + "."
        batch_filename = batch_delim.join(output_filename_parts)
        g = c.get_graph()
        triple_count = triple_count + len(g)
        print "Completed batch %s, %s records converted to %s triples so far" % (batch, count, triple_count)
        output_file = open(batch_filename, "w")
        output_file.write(g.serialize(format=output_format))
        output_file.close()
        if compress:
          archive_filename = batch_filename + ".tgz"
          archive = tarfile.open(archive_filename, "w:gz")
          archive.add(batch_filename, os.path.basename(batch_filename))
          archive.close()
        batch = batch + 1
      print "\nStarting batch %s" % batch
      c = Converter()
      
    try:
      c.convert(line)
      count = count + 1
    except Exception,e:
      bad_record_file.write(line)

  print "Completed last batch, %s records converted to %s triples" % (count,triple_count)
  batch_delim = "_" + str(batch) + "."
  batch_filename = batch_delim.join(output_filename_parts)
  g = c.get_graph()
  
  
  output_file = open(batch_filename, "w")
  output_file.write(g.serialize(format=output_format))
  output_file.close()

  f.close()
  bad_record_file.close()


