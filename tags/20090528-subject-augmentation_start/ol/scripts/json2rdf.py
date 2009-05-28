import json
import optparse
import os
import rdflib
import sys
import tarfile
import urllib2
import re
import gdbm
import isbn

from time import strftime

BASE_URI = "http://ol.dataincubator.org"
rdf = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")
dct = rdflib.Namespace("http://purl.org/dc/terms/")
ol = rdflib.Namespace("http://olrdf.appspot.com/key/")
bibo = rdflib.Namespace("http://purl.org/ontology/bibo/")
frbr = rdflib.Namespace("http://purl.org/vocab/frbr/core#")
skos = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
foaf = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
owl = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
bio = rdflib.Namespace("http://purl.org/vocab/bio/0.1/")
ov = rdflib.Namespace("http://open.vocab.org/terms/")
mo = rdflib.Namespace("http://purl.org/ontology/mo/")
void = rdflib.Namespace("http://rdfs.org/ns/void#")

class Converter:
   
  def __init__(self):
    self.interesting_uris = []
    self.worksdone = {}
    self.key_cache = gdbm.open('key_cache.db', 'c');
    self.identifier_map = gdbm.open('identifier_map.db', 'c');
    self.lcsh_lookup = gdbm.open('lcsh_lookup.db', 'r');
    self.thingisbn_lookup = gdbm.open('thingisbn_lookup.db', 'r');
    self.dataset_resource = rdflib.URIRef(BASE_URI + "/")
    self.reset()

  def reset(self):
    self.graph = rdflib.ConjunctiveGraph()
    self.graph.bind("rdf", rdf)
    self.graph.bind("rdfs", rdfs)
    self.graph.bind("dct", dct)
    self.graph.bind("ol", ol)
    self.graph.bind("bibo", bibo)
    self.graph.bind("frbr", frbr)
    self.graph.bind("skos", skos)
    self.graph.bind("foaf", foaf)
    self.graph.bind("owl", owl)
    self.graph.bind("bio", bio)
    self.graph.bind("ov", ov)
    self.graph.bind("mo", mo)
    

  def convert(self, indata):
    data = json.read(indata)
    
    if data["key"].startswith("/user/"):
      return

    elif data["type"]["key"] == "/type/redirect" or data["type"]["key"] == "/type/type" or data["type"]["key"] == "/type/delete" or data["type"]["key"] == "/type/scan_record" or data["type"]["key"] == "/type/usergroup" or data["type"]["key"] == "/type/permission" or data["type"]["key"] == "/type/property" or data["type"]["key"] == "/type/backreference":
      #print "Ignoring '%s' because it is a '%s'" % (data["key"], data["type"]["key"]) 
      return
    elif data["type"]["key"] == "/type/edition":
      self.parse_edition(data)
    elif data["type"]["key"] == "/type/author":
      self.parse_person(data)
    else:
      print "  Ignoring unknown type %s" % data["type"]["key"]
      return


  def parse_edition(self, data):
    item_uri = None
    work_uri = None
    manifestations = []     

    # Look for librarything work id      
    if data.has_key("isbn_10"):
      for isbn10 in data["isbn_10"]:
        if self.thingisbn_lookup.has_key(isbn10):
          workid = self.thingisbn_lookup[isbn10]
          work_uri = self.get_work_uri("workid:" + workid)
          self.graph.add((rdflib.URIRef(work_uri), foaf["isPrimaryTopicOf"], rdflib.URIRef("http://www.librarything.com/work/" + workid)))
          break          
  
    if work_uri is None:
      work_uri = self.get_work_uri(data["key"])

    isbn13s = {}
    if data.has_key("isbn_10"):
      for isbn10 in data["isbn_10"]:
        manifestation_uri = self.get_manifestation_uri("isbn:" + isbn10)
        manifestations.append(manifestation_uri)
        isbn13 =  isbn.convert(isbn10)
        if isbn13 is not None:
          isbn13s[isbn13] = 1
          self.graph.add((rdflib.URIRef(manifestation_uri), bibo["isbn10"], rdflib.Literal(isbn10)))
          self.graph.add((rdflib.URIRef(manifestation_uri), bibo["isbn13"], rdflib.Literal(isbn13)))
          self.graph.add((rdflib.URIRef(manifestation_uri), owl["sameAs"], rdflib.URIRef("http://www4.wiwiss.fu-berlin.de/bookmashup/books/" + isbn10)))
        else:
          print "  ISBN %s is invalid" % isbn10

    else:
      manifestations.append(self.get_manifestation_uri(data["key"]))
  
    if not self.worksdone.has_key(work_uri):
      self.worksdone[work_uri] = 1
      self.parse_work(data,work_uri)

    for manifestation_uri in manifestations:
      self.graph.add((rdflib.URIRef(manifestation_uri), dct["isVersionOf"], rdflib.URIRef(work_uri)))
      self.graph.add((rdflib.URIRef(work_uri), dct["hasVersion"], rdflib.URIRef(manifestation_uri)))
      self.parse_manifestation(data,manifestation_uri)


  def parse_work(self, data, item_uri ):
    skip = ["key", "type", "properties", "kind", "latest_revision", "id", "last_modified", "created", "revision", "uri_descriptions", "genres", "subject_place", "subject_time", "work_title", "work_titles", "isbn_invalid", "location", "scan_on_demand",
            "edition_name", "publish_country", "isbn_10", "isbn_13", "oclc_numbers", "oclc_number", "publishers", "publish_places", "pagination", "lccn", "number_of_pages", "publish_date", "weight", "physical_format", "physical_dimensions", "ocaid", "languages", "table_of_contents", "coverimage",
            "first_sentence"]
    subj = rdflib.URIRef(item_uri)
    self.graph.add((subj, rdf["type"], frbr["Work"]))

    # Connect the item resource to the OpenLibrary document describing it
    ol_document = rdflib.URIRef("http://openlibrary.org" + data["key"])
    self.graph.add((subj, foaf["isPrimaryTopicOf"], ol_document))
    self.add_preflabel(data, subj)
    
    for k, v in data.items():
      if k == "title":
        self.graph.add((subj, dct["title"], rdflib.Literal(v)))
      elif k == "subtitle":
        self.graph.add((subj, ov["subtitle"], rdflib.Literal(v)))
      elif k == "title_prefix":
        self.graph.add((subj, ol["title_prefix"], rdflib.Literal(v)))
      elif k == "other_titles":
        for t in v:
          self.graph.add((subj, skos["altLabel"], rdflib.Literal(t)))
      elif k == "by_statement":
        self.graph.add((subj, ol["by_statement"], rdflib.Literal(v)))
      elif k == "series":
        series = ""
        for s in v:
          if not series.endswith(";"):
            series_resource = rdflib.URIRef(self.make_uri("series"))
            self.graph.add((subj, ol["series"], series_resource))
            self.graph.add((series_resource, skos["prefLabel"], rdflib.Literal(s)))
            series = ""
          series += " " + s
        if s != "":
          series_resource = rdflib.URIRef(self.make_uri("series"))
          self.graph.add((subj, ol["series"], series_resource))
          self.graph.add((series_resource, skos["prefLabel"], rdflib.Literal(s)))
          
      elif k == "authors":
        group_resource = rdflib.URIRef(self.make_uri("groups"))
        self.graph.add((group_resource, dct["isPartOf"], self.dataset_resource))
        self.graph.add((subj, bibo["authorList"], group_resource))
        self.graph.add((group_resource, rdf["type"], rdf["Seq"]))
        i = 1
        for author in v:
          person_resource = rdflib.URIRef(self.get_person_uri(author["key"]))
          self.graph.add((subj, dct["creator"], person_resource))
          self.graph.add((group_resource, rdf["_" + str(i)], person_resource))
          self.graph.add((person_resource, rdf["type"], foaf["Person"]))
          if isinstance(author, (str, unicode)):
            self.graph.add((person_resource, foaf["name"], rdflib.Literal(author)))
          else:
            self.graph.add((person_resource, foaf["isPrimaryTopicOf"], rdflib.URIRef("http://openlibrary.org" + author["key"])))
          i += 1
      elif k == "alternate_names":
        for t in v:
          self.graph.add((subj, skos["altLabel"], rdflib.Literal(t)))
      elif k == "lc_classifications":
        for c in v:
          self.graph.add((subj, ol["lc_classification"], rdflib.Literal(c)))
      elif k == "contributions":
        group_resource = rdflib.URIRef(self.make_uri("groups"))
        self.graph.add((subj, bibo["contributorList"], group_resource))
        self.graph.add((group_resource, rdf["type"], rdf["Bag"]))
        i = 1
        for c in v:
          if isinstance(c, (str, unicode)):
            person_resource = rdflib.URIRef(self.make_uri("people"))
            self.graph.add((subj, dct["contributor"], person_resource))
            self.graph.add((group_resource, rdf["_" + str(i)], person_resource))
            self.graph.add((person_resource, rdf["type"], foaf["Person"]))
            self.graph.add((person_resource, foaf["name"], rdflib.Literal(c)))
          else:
            person_resource = rdflib.URIRef(self.get_person_uri(c["key"]))
            self.graph.add((subj, dct["contributor"], person_resource))
            self.graph.add((group_resource, rdf["_" + str(i)], person_resource))
            self.graph.add((person_resource, rdf["type"], foaf["Person"]))
            self.graph.add((person_resource, foaf["isPrimaryTopicOf"], rdflib.URIRef("http://openlibrary.org" + c["key"])))
          i += 1
      elif k == "subjects":
        for sub in v:
          sub = sub.replace(" -- ", "--")
          if self.lcsh_lookup.has_key(sub):
            lcsh_uri = self.lcsh_lookup[sub]
            self.graph.add((subj, dct["subject"], rdflib.URIRef(lcsh_uri)))
            self.graph.add((rdflib.URIRef(lcsh_uri), skos["prefLabel"], rdflib.Literal(sub)))
          else:          
            #print "  did not match subject %s" % sub
            self.graph.add((subj, dct["subject"], rdflib.Literal(sub)))
      elif k == "uris" or k == "url":
        for i in v:
          self.graph.add((subj, rdfs["seeAlso"], rdflib.URIRef(str(i))))
      elif k == "dewey_decimal_class":
        for d in v:
          self.graph.add((subj, ol["dewey_decimal_class"], rdflib.Literal(d)))
      elif k == "notes":
        self.graph.add((subj, rdfs["comment"], rdflib.Literal(self.clean_text(v["value"]))))
      elif k == "wikipedia":
        self.graph.add((subj, foaf["isPrimaryTopicOf"], rdflib.URIRef(v)))
        self.graph.add((subj, mo["wikipedia"], rdflib.URIRef(v)))
        if re.match('^http://en.wikipedia.org/wiki/', v):
          dbpedia_uri = re.sub('http://en.wikipedia.org/wiki/', 'http://dbpedia.org/resource/', v)
          self.graph.add((subj, owl["sameAs"], rdflib.URIRef(dbpedia_uri)))
      elif k == "description":
        self.graph.add((subj, dct["description"], rdflib.Literal(v["value"])))
      elif k in skip:
        pass
      else:
        print "  parse_work did not process '%s':'%s'" % (k, v)
    
  def add_preflabel(self, data, subj):
    if data.has_key("title"):
      title = data["title"]
      if data.has_key("subtitle"):  
        title += ": " + data["subtitle"]
      if data.has_key("title_prefix"):    
        if not data["title_prefix"].endswith(" "):
          title = data["title_prefix"] + " " + title
        else:
          title = data["title_prefix"] + title
      self.graph.add((subj, skos["prefLabel"], rdflib.Literal(title)))
    
    
  def parse_manifestation(self, data, item_uri ):
    skip = ["key", "type", "properties", "kind", "latest_revision", "id", "last_modified", "created", "revision", "uri_descriptions", "genres", "subject_place", "subject_time", "work_title", "work_titles", "isbn_invalid", "location", "scan_on_demand",
            "lc_classifications","authors","contributions","subjects","isbn_10","isbn_13","uris", "url","dewey_decimal_class","wikipedia","series"];

    subj = rdflib.URIRef(item_uri)
    self.graph.add((subj, rdf["type"], frbr["Manifestation"]))

    # Connect the item resource to the OpenLibrary document describing it
    ol_document = rdflib.URIRef("http://openlibrary.org" + data["key"])
    self.graph.add((subj, foaf["isPrimaryTopicOf"], ol_document))
    self.add_preflabel(data, subj)

    for k, v in data.items():
      if k == "title":
        self.graph.add((subj, dct["title"], rdflib.Literal(v)))
      elif k == "title_prefix":
        self.graph.add((subj, ol["title_prefix"], rdflib.Literal(v)))
      elif k == "other_titles":
        for t in v:
          self.graph.add((subj, skos["altLabel"], rdflib.Literal(t)))
      elif k == "subtitle":
        self.graph.add((subj, ov["subtitle"], rdflib.Literal(v)))
      elif k == "edition_name":
        self.graph.add((subj, bibo["edition"], rdflib.Literal(v)))
      elif k == "publish_country":
        self.graph.add((subj, ol["publish_country"], rdflib.Literal(v.strip())))
      elif k == "by_statement":
        self.graph.add((subj, ol["by_statement"], rdflib.Literal(v)))
      elif k == "oclc_numbers" or k == "oclc_number":
        for n in v:
          self.graph.add((subj, bibo["oclcnum"], rdflib.Literal(n)))
          self.graph.add((subj, foaf["isPrimaryTopicOf"], rdflib.URIRef("http://www.worldcat.org/oclc/" + n)))
          self.identifier_map["oclc:" + str(n)] = item_uri;
      elif k == "publishers":
        for p in v:
          self.graph.add((subj, dct["publisher"], rdflib.Literal(p)))
      elif k == "publish_places":
        for p in v:
          self.graph.add((subj, ol["publish_place"], rdflib.Literal(p)))
      elif k == "pagination":
        self.graph.add((subj, ol["pagination"], rdflib.Literal(v)))
      elif k == "lccn":
        for l in v:
          self.graph.add((subj, bibo["lccn"], rdflib.Literal(l)))
          self.graph.add((subj, foaf["isPrimaryTopicOf"], rdflib.URIRef("http://lccn.loc.gov/" + l)))
      elif k == "number_of_pages":
        self.graph.add((subj, ov["numberOfPages"], rdflib.Literal(str(v))))
      elif k == "publish_date":
        self.graph.add((subj, dct["issued"], rdflib.Literal(v)))
      elif k == "weight":
        self.graph.add((subj, ov["weight"], rdflib.Literal(v)))
      elif k == "physical_format":
        format = self.clean_text(str(v)).lower()
        if format == "microforme" or format == "microfrom" or format == "mciroform":
          format = "microform"
          
        self.graph.add((subj, dct["medium"], rdflib.Literal(format)))
        
        if format == "map":
          self.graph.add((subj, rdf["type"], bibo["Map"]))
        elif format == "audio cd":
          self.graph.add((subj, rdf["type"], mo["CD"]))
        elif format == "mp3 cd":
          # TODO: find a class for mp3 cd
          pass
        elif format == "audio cassette":
          # TODO: find a class for audio cassette
          pass
        elif format == "pamphlet":
          # TODO: find a class for pamphlet
          pass
        elif format == "diskette":
          # TODO: find a class for diskette
          pass
        elif format == "microform" or format == "microforme" or format == "microfrom" or format == "mciroform":
          # TODO: find a class for microform
          pass
        elif format == "spoken word":
          # TODO: find a class for spoken word
          pass
        elif format == "paperback" or format == "mass market paperback":
          # TODO: find a class for paperback
          pass
        elif format == "hardback" or format == "hardcover":
          # TODO: find a class for paperback
          pass
        elif format == "turtleback":
          # TODO: find a class for turtleback
          pass
        elif format == "board book":
          # TODO: find a class for board book
          pass
        elif format == "rag book":
          # TODO: find a class for rag book
          pass
        elif format == "calendar":
          # TODO: find a class for calendar
          pass
        elif format == "sheet music":
          # TODO: find a class for sheet music
          pass
        elif format == "cd-rom":
          # TODO: find a class for cd rom
          pass
        elif format == "comic":
          # TODO: find a class for comic
          pass
        elif format == "cards":
          # TODO: find a class for cards
          pass
        elif format == "loose leaf":
          # TODO: find a class for loose leaf
          pass
        elif format == "spiral-bound":
          # TODO: find a class for spiral bound
          pass
        elif format == "ring-bound":
          # TODO: find a class for ring bound
          pass
        elif format == "plastic comb":
          # TODO: find a class for plastic comb
          pass
        elif format == "library binding":
          # TODO: find a class for library binding
          pass
        elif format == "electronic resource" or format == "computer file":
          # TODO: find a class for electronic resource
          pass
        elif format == "video recording" or format == "videorecording":
          # TODO: find a class for video recording
          pass
        elif format == "pdf":
          # TODO: find a class for pdf
          pass
        elif format == "graphic":
          # TODO: find a class for graphic
          pass
        elif format == "textbook binding":
          # TODO: find a class for tectbook binding
          pass
        elif format == "unknown binding":
          pass
        else:
          print "  Found physical format '%s'" % (self.clean_text(str(v)))
      elif k == "physical_dimensions":
        self.graph.add((subj, ol["physical_dimensions"], rdflib.Literal(v)))
      elif k == "notes":
        self.graph.add((subj, rdfs["comment"], rdflib.Literal(self.clean_text(v["value"]))))
      elif k == "first_sentence":
        self.graph.add((subj, ov["firstSentence"], rdflib.Literal(self.clean_text(v["value"]))))
      elif k == "ocaid":
        self.graph.add((subj, foaf["isPrimaryTopicOf"], rdflib.URIRef("http://www.archive.org/details/" + v)))
        # TODO: add links to scanned content in internet archive
        # directory of files: http://ia360913.us.archive.org/1/items/{ocaid}/
        # xml description of files: http://ia360913.us.archive.org/1/items/{ocaid}/{ocaid}_files.xml
        # PDF scan: http://www.archive.org/download/{ocaid}/{ocaid}.pdf
        # Full text: http://www.archive.org/stream/{ocaid}/{ocaid}_djvu.txt
      elif k == "description":
        self.graph.add((subj, dct["description"], rdflib.Literal(v["value"])))
      elif k == "languages":
        for l in v:
          if l["key"].startswith('/l/'):
            self.graph.add((subj, dct["language"], rdflib.Literal(l["key"][3:])))
      elif k == "table_of_contents":
        toc_resource = rdflib.URIRef(self.make_uri("tocs"))
        self.graph.add((subj, dct["tableOfContents"], toc_resource))
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
          self.graph.add((toc_resource, rdf["_" + str(i)], section))
          i += 1
      elif k in skip:
        pass
      else:
        print "  parse_manifestation not process '%s':'%s'" % (k, v)
  


  def parse_person(self, data ):
    item_uri = self.get_person_uri(data["key"])
    subj = rdflib.URIRef(item_uri)
    
    skip = ["key", "type", "properties", "kind", "latest_revision", "id", "last_modified", "created", "revision", "uri_descriptions", "genres", "subject_place", "subject_time", "work_title", "work_titles", "isbn_invalid", "location", "scan_on_demand"]
    self.graph.add((subj, rdf["type"], foaf["Person"]))

    # Connect the item resource to the OpenLibrary document describing it
    ol_document = rdflib.URIRef("http://openlibrary.org" + data["key"])
    self.graph.add((subj, foaf["isPrimaryTopicOf"], ol_document))
    
    for k, v in data.items():
      if k == "title":
        self.graph.add((subj, foaf["title"], rdflib.Literal(v)))
      elif k == "name":
        self.graph.add((subj, skos["prefLabel"], rdflib.Literal(v)))
      elif k == "personal_name":
        self.graph.add((subj, foaf["name"], rdflib.Literal(v)))
      elif k == "alternate_names":
        for t in v:
          self.graph.add((subj, skos["altLabel"], rdflib.Literal(t)))
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
      elif k == "notes":
        self.graph.add((subj, rdfs["comment"], rdflib.Literal(self.clean_text(v["value"]))))
      elif k == "bio":
        self.graph.add((subj, bio["olb"], rdflib.Literal(self.clean_text(v["value"]))))
      elif k == "wikipedia":
        self.graph.add((subj, foaf["isPrimaryTopicOf"], rdflib.URIRef(v)))
        self.graph.add((subj, mo["wikipedia"], rdflib.URIRef(v)))
        if re.match('^http://en.wikipedia.org/wiki/', v):
          dbpedia_uri = re.sub('http://en.wikipedia.org/wiki/', 'http://dbpedia.org/resource/', v)
          self.graph.add((subj, owl["sameAs"], rdflib.URIRef(dbpedia_uri)))
      elif k in skip:
        pass
      else:
        print "  parse_person did not process '%s':'%s'" % (k, v)




  def clear(self):
    self.graph = rdflib.ConjunctiveGraph()
  
  def get_graph(self):
    return self.graph 
    
  def make_uri(self, prefix):
    return BASE_URI + "/" + prefix + "/" + str(self.get_next_resource_index(prefix))
   
  def get_next_resource_index(self, prefix):
    if self.key_cache.has_key('idx_' + prefix):
      self.key_cache['idx_' + prefix] = str(int(self.key_cache['idx_' + prefix]) + 1)
    else:
      self.key_cache['idx_' + prefix] = '1';
    return self.key_cache['idx_' + prefix]
        
  def get_work_uri(self, key):  
    if self.key_cache.has_key("[work]" + key):
      return self.key_cache["[work]" + key]
    else:
      index = str(self.get_next_resource_index("works"))
      self.key_cache["[work]" + key] = BASE_URI + "/works/" + index
      return BASE_URI + "/works/" + index

  def get_manifestation_uri(self, key):  
    if self.key_cache.has_key("[item]" + key):
      return self.key_cache["[item]" + key]
    else:
      index = str(self.get_next_resource_index("items"))
      self.key_cache["[item]" + key] = BASE_URI + "/items/" + index
      return BASE_URI + "/items/" + index

  def get_person_uri(self, key):  
    if self.key_cache.has_key("[person]" + key):
      return self.key_cache["[person]" + key]
    else:
      index = str(self.get_next_resource_index("people"))
      self.key_cache["[person]" + key] = BASE_URI + "/people/" + index
      return BASE_URI + "/people/" + index
      
  def clean_uri(self, uri):
    return uri
  
  def clean_text(self, text):
    text = re.sub('[^\w]+$', '', text)
    text = re.sub('^[^\w\)\]\!]+', '', text)
    return text 
  
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

  c = Converter()
  

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
      c.reset()
      
    try:
      c.convert(line)
      count += 1
    except (UnicodeEncodeError):
      bad_record_file.write(line)

  batch_delim = "_" + str(batch) + "."
  batch_filename = batch_delim.join(output_filename_parts)
  g = c.get_graph()
  triple_count = triple_count + len(g)
  
  output_file = open(batch_filename, "w")
  output_file.write(g.serialize(format=output_format))
  output_file.close()
  print "Completed last batch, %s records converted to %s triples" % (count,triple_count)

  f.close()
  bad_record_file.close()

  print "Creating void description"
  void_graph = rdflib.ConjunctiveGraph()
  void_graph.bind("dct", dct)
  void_graph.bind("void", void)
  void_graph.bind("rdfs", rdfs)
  dataset_resource = rdflib.URIRef(BASE_URI + "/")  

  void_graph.add((dataset_resource, dct["title"], rdflib.Literal("OpenLibrary Data")))
  void_graph.add((dataset_resource, dct["description"], rdflib.Literal("A conversion of the OpenLibrary JSON dumps. Currently this is only a sample of %s records (out of about 20 million) which corresponds to %s triples."  % (count, triple_count))))
  void_graph.add((dataset_resource, dct["rights"], rdflib.Literal("The OpenLibrary data, as factual information, is in the public domain. This derived dataset is also public domain and is explictly licensed using the Open Data Commons Public Domain Dedication and License")))
  void_graph.add((dataset_resource, dct["license"], rdflib.URIRef("http://www.opendatacommons.org/odc-public-domain-dedication-and-licence/")))
  void_graph.add((dataset_resource, dct["source"], rdflib.URIRef("http://openlibrary.org/")))
  void_graph.add((dataset_resource, dct["issued"], rdflib.Literal("2009-04-20",datatype=rdflib.URIRef("http://www.w3.org/2001/XMLSchema#date"))))
  void_graph.add((dataset_resource, dct["modified"], rdflib.Literal(strftime("%Y-%m-%d"),datatype=rdflib.URIRef("http://www.w3.org/2001/XMLSchema#date"))))
  void_graph.add((dataset_resource, dct["creator"], rdflib.URIRef("http://iandavis.com/id/me")))
  void_graph.add((dataset_resource, dct["subject"], rdflib.URIRef("http://lcsubjects.org/subjects/sh85079330#concept")))
  void_graph.add((rdflib.URIRef("http://iandavis.com/id/me"), rdfs["label"], rdflib.Literal("Ian Davis")))
  void_graph.add((dataset_resource, void["exampleResource"], rdflib.URIRef(BASE_URI + "/works/59650")))
  void_graph.add((dataset_resource, void["exampleResource"], rdflib.URIRef(BASE_URI + "/works/6102")))
  void_graph.add((dataset_resource, void["exampleResource"], rdflib.URIRef(BASE_URI + "/items/49015")))
  void_graph.add((dataset_resource, void["exampleResource"], rdflib.URIRef(BASE_URI + "/people/6889")))
  void_graph.add((dataset_resource, void["sparqlEndpoint"], rdflib.URIRef("http://api.talis.com/stores/openlibrary/services/sparql")))
  void_graph.add((dataset_resource, void["uriLookupEndpoint"], rdflib.URIRef("http://api.talis.com/stores/openlibrary/meta?about=")))
  void_graph.add((dataset_resource, void["uriRegexPattern"], rdflib.Literal(BASE_URI + "/.+")))
  void_graph.add((dataset_resource, void["vocabulary"], rdflib.URIRef("http://purl.org/dc/terms/")))
  void_graph.add((dataset_resource, void["vocabulary"], rdflib.URIRef("http://olrdf.appspot.com/key/")))
  void_graph.add((dataset_resource, void["vocabulary"], rdflib.URIRef("http://purl.org/ontology/bibo/")))
  void_graph.add((dataset_resource, void["vocabulary"], rdflib.URIRef("http://purl.org/vocab/frbr/core#")))
  void_graph.add((dataset_resource, void["vocabulary"], rdflib.URIRef("http://www.w3.org/2004/02/skos/core#")))
  void_graph.add((dataset_resource, void["vocabulary"], rdflib.URIRef("http://xmlns.com/foaf/0.1/")))
  void_graph.add((dataset_resource, void["vocabulary"], rdflib.URIRef("http://www.w3.org/2002/07/owl#")))
  void_graph.add((dataset_resource, void["vocabulary"], rdflib.URIRef("http://purl.org/vocab/bio/0.1/")))
  void_graph.add((dataset_resource, void["vocabulary"], rdflib.URIRef("http://open.vocab.org/terms/")))
  void_graph.add((dataset_resource, void["vocabulary"], rdflib.URIRef("http://purl.org/ontology/mo/")))
  void_graph.add((rdflib.URIRef("http://purl.org/dc/terms/"), rdfs["label"], rdflib.Literal("Dublin Core")))
  void_graph.add((rdflib.URIRef("http://olrdf.appspot.com/key/"), rdfs["label"], rdflib.Literal("Misc. Open Library Terms (temporary)")))
  void_graph.add((rdflib.URIRef("http://purl.org/ontology/bibo/"), rdfs["label"], rdflib.Literal("The Bibliographic Ontology")))
  void_graph.add((rdflib.URIRef("http://purl.org/vocab/frbr/core#"), rdfs["label"], rdflib.Literal("FRBR")))
  void_graph.add((rdflib.URIRef("http://www.w3.org/2004/02/skos/core#"), rdfs["label"], rdflib.Literal("SKOS")))
  void_graph.add((rdflib.URIRef("http://xmlns.com/foaf/0.1/"), rdfs["label"], rdflib.Literal("FOAF")))
  void_graph.add((rdflib.URIRef("http://www.w3.org/2002/07/owl#"), rdfs["label"], rdflib.Literal("OWL")))
  void_graph.add((rdflib.URIRef("http://purl.org/vocab/bio/0.1/"), rdfs["label"], rdflib.Literal("BIO (Biographical Information)")))
  void_graph.add((rdflib.URIRef("http://open.vocab.org/terms/"), rdfs["label"], rdflib.Literal("OpenVocab")))
  void_graph.add((rdflib.URIRef("http://purl.org/ontology/mo/"), rdfs["label"], rdflib.Literal("Music Ontology")))
  void_graph.add((dataset_resource, rdfs["seeAlso"], rdflib.URIRef("http://code.google.com/p/dataincubator/wiki/OpenLibrary")))
  void_graph.add((dataset_resource, rdfs["seeAlso"], rdflib.URIRef("http://groups.google.com/group/dataincubator")))
  void_file = open(output_filename_parts[0] + "_void.rdf", "w")
  void_file.write(void_graph.serialize(format=output_format))
  void_file.close()



  print "Dumping out identifiers"
  k = c.identifier_map.firstkey()
  identifier_file = open("identifiers.csv", "w")
  while k != None:
    identifier_file.write(k + "," + c.identifier_map[k] + "\n")
    k = c.identifier_map.nextkey(k)
  identifier_file.close()

