# Converts the Standard Occupational Classification 2000 (SOC2000) to SKxOS
# Run pdftotext -layout soc2000.pdf soc2000.txt first
import rdflib
import re
from graphutils import BatchGraph
from time import strftime

BASE_URI = "http://ons.dataincubator.org/"
rdf = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")
dct = rdflib.Namespace("http://purl.org/dc/terms/")
skos = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
void = rdflib.Namespace("http://rdfs.org/ns/void#")

g = BatchGraph(30000, "output/sic2007", "rdf")
g.bind("rdf", rdf)
g.bind("rdfs", rdfs)
g.bind("dct", dct)
g.bind("skos", skos)
g.bind("void", void)


scheme_resource = rdflib.URIRef(BASE_URI + "sic2007/")  
g.add((scheme_resource, skos["prefLabel"], rdflib.Literal("UK Standard Industrial Classification of Economic Activities 2007 (SIC 2007)")))
g.add((scheme_resource, dct["description"], rdflib.Literal("A Standard Industrial Classification (SIC) was first introduced into the United Kingdom in 1948 for use in classifying business establishments and other statistical units by the type of economic activity in which they are engaged. The classification provides a framework for the collection, tabulation, presentation and analysis of data and its use promotes uniformity. In addition, it can be used for administrative purposes and by non-government bodies as a convenient way of classifying industrial activities into a common structure.")))
g.add((scheme_resource, rdf["type"], skos["ConceptScheme"]))
g.add((scheme_resource, dct["rights"], rdflib.Literal("The data and text in this classification scheme is under Crown Copyright")))
g.add((scheme_resource, dct["source"], rdflib.URIRef("http://www.statistics.gov.uk/statbase/Product.asp?vlnk=14012")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/A")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/B")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/C")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/D")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/E")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/F")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/G")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/H")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/I")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/J")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/K")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/L")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/M")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/N")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/O")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/P")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/Q")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/R")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/S")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/T")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "sic2007/U")))



# sic2007
state = "seek terms"
section = None
notes = ""
open_tags = []
concept_uri= None
f = open("../data/sic2007.txt", "r")
for line in f:
  if state == "seek terms":
    if "UK SIC 2007 - Summary of Structure" in line:
      state = "read terms"
      section = None
        
  elif state == "read terms":
    if "Explanatory Notes" in line:
      state = "read notes"
      section = None
    else:
      id = None
      m = re.match('^([\d\.\/]+)\s([a-zA-Z].*)$', line)
      if m is not None:
        id = m.group(1).strip()
        title = m.group(2).strip()
      else:
        m = re.match('^SECTION\s([A-Z])\s(.+)$', line)
        if m is not None:
          id = m.group(1).strip()
          title = m.group(2).strip()
          section = id
              
      if id is not None:
        concept_resource = rdflib.URIRef(BASE_URI + "sic2007/" + id)
        g.add((concept_resource, rdf["type"], skos["Concept"]))
        g.add((concept_resource, skos["prefLabel"], rdflib.Literal(title)))
        g.add((concept_resource, dct["identifier"], rdflib.Literal(id)))
        if len(id) == 2:
          g.add((concept_resource, skos["broader"], rdflib.URIRef(BASE_URI + "sic2007/" + section)))
          g.add((rdflib.URIRef(BASE_URI + "sic2007/" + section), skos["narrower"], concept_resource))
        elif len(id) == 4:
          g.add((concept_resource, skos["broader"], rdflib.URIRef(BASE_URI + "sic2007/" + id[:-2])))
          g.add((rdflib.URIRef(BASE_URI + "sic2007/" + id[:-2]), skos["narrower"], concept_resource))
        elif len(id) > 4:
          g.add((concept_resource, skos["broader"], rdflib.URIRef(BASE_URI + "sic2007/" + id[:-1])))
          g.add((rdflib.URIRef(BASE_URI + "sic2007/" + id[:-1]), skos["narrower"], concept_resource))
  else:
    if "UK Standard Industrial Classification of Economic" in line or "14/12/2007" in line:
      pass
    else:
      m = re.match('^([\d\.\/]+)\s([a-zA-Z].*)$', line)
      if m is not None:
        if concept_uri is not None:
          while len(open_tags) > 0:
            notes += "</"  + open_tags.pop() + ">\n"

          if len(notes.strip()) > 0:
            notes = '<div xmlns="http://www.w3.org/1999/xhtml">' + notes + "</div>"
            g.add((rdflib.URIRef(concept_uri), skos["scopeNote"], rdflib.Literal(notes, datatype=rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral') )))
          
        id = m.group(1).strip()
        concept_uri = BASE_URI + "sic2007/" + id
        notes = ""
        open_tags = []
      else:
        m = re.match('^SECTION\s([A-Z])\s(.+)$', line)
        if m is not None:
          if concept_uri is not None:
            while len(open_tags) > 0:
              notes += "</"  + open_tags.pop() + ">\n"

            if len(notes.strip()) > 0:
              notes = '<div xmlns="http://www.w3.org/1999/xhtml">' + notes + "</div>"
              g.add((rdflib.URIRef(concept_uri), skos["scopeNote"], rdflib.Literal(notes, datatype=rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral') )))
          id = m.group(1).strip()
          concept_uri = BASE_URI + "sic2007/" + id
          notes = ""
          open_tags = []
        else:
          line = line.strip()
          if line == "":
            while len(open_tags) > 0:
              notes += "</"  + open_tags.pop() + ">\n"
          elif line.startswith("-"):    
            if len(open_tags) > 0:
              if open_tags[-1] == "p":
                notes += "</"  + open_tags.pop() + ">\n"
                notes += "<ul>\n"
                open_tags.append("ul")
              elif open_tags[-1] == "li":
                if len(open_tags) > 2 and open_tags[-3] == "li":
                  notes += "</"  + open_tags.pop() + ">\n"
                  notes += "    </"  + open_tags.pop() + ">\n  "

                notes += "</"  + open_tags.pop() + ">\n"

            notes += "  <li>"
            notes += line[2:] + " "
            open_tags.append("li")


          elif line.startswith("\xe2"):    
            if len(open_tags) > 0:
              if open_tags[-1] == "p":
                notes += "</"  + open_tags.pop() + ">\n"
                notes += "<ul>\n"
                open_tags.append("ul")
              elif open_tags[-1] == "li":
                if len(open_tags) > 2 and open_tags[-3] == "li":
                  notes += "</"  + open_tags.pop() + ">\n"
                else:
                  notes += "\n    <ul>\n"
                  open_tags.append("ul")

            notes += "     <li>"
            notes += line[4:] + " "
            open_tags.append("li")

          else:
            if len(open_tags) == 0:
              notes += "<p>"
              open_tags.append("p")
            notes += line + " "
          
while len(open_tags) > 0:
  notes += "</"  + open_tags.pop() + ">\n"
        
if len(notes.strip()) > 0:
  notes = '<div xmlns="http://www.w3.org/1999/xhtml">' + notes + "</div>"
  g.add((rdflib.URIRef(concept_uri), skos["scopeNote"], rdflib.Literal(notes, datatype=rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral') )))
    
f.close()


g.add((rdflib.URIRef(BASE_URI), void["exampleResource"], rdflib.URIRef(BASE_URI + "sic2007/")))
g.flush()

