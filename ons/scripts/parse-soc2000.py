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

g = BatchGraph(30000, "output/soc2000", "rdf")
g.bind("rdf", rdf)
g.bind("rdfs", rdfs)
g.bind("dct", dct)
g.bind("skos", skos)
g.bind("void", void)



scheme_resource = rdflib.URIRef(BASE_URI + "soc2000/")  
g.add((scheme_resource, skos["prefLabel"], rdflib.Literal("Standard Occupational Classification 2000 (SOC2000)")))
g.add((scheme_resource, dct["description"], rdflib.Literal("The Standard Occupational Classification was first published in 1990 to replace both the Classification of Occupations 1980 (CO80) and the Classification of Occupations and Dictionary of Occupational Titles (CODOT). SOC 1990 has been revised and updated to produce SOC2000.")))
g.add((scheme_resource, rdf["type"], skos["ConceptScheme"]))
g.add((scheme_resource, dct["rights"], rdflib.Literal("The data and text in this classification scheme is under Crown Copyright")))
g.add((scheme_resource, dct["source"], rdflib.URIRef("http://www.ons.gov.uk/about-statistics/classifications/current/SOC2000/index.html")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "soc2000/1")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "soc2000/2")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "soc2000/3")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "soc2000/4")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "soc2000/5")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "soc2000/6")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "soc2000/7")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "soc2000/8")))
g.add((scheme_resource, skos["hasTopConcept"], rdflib.URIRef(BASE_URI + "soc2000/9")))



read_terms = False
f = open("../data/soc2000.txt", "r")
for line in f:
  if not read_terms:
    if line.startswith("Summary of Structure"):
      read_terms = True    
  else:

    m = re.match('^\s*(\d+)\s+(.+)', line)
    if m is not None:
      id = m.group(1)
      concept_resource = rdflib.URIRef(BASE_URI + "soc2000/" + id)
      g.add((concept_resource, rdf["type"], skos["Concept"]))
      g.add((concept_resource, skos["prefLabel"], rdflib.Literal(m.group(2))))
      g.add((concept_resource, dct["identifier"], rdflib.Literal(id)))
      g.add((concept_resource, skos["inScheme"], scheme_resource))
      if len(id) > 1:
        g.add((concept_resource, skos["broader"], rdflib.URIRef(BASE_URI + "soc2000/" + id[:-1])))
        g.add((rdflib.URIRef(BASE_URI + "soc2000/" + id[:-1]), skos["narrower"], concept_resource))
      
f.close()


g.add((rdflib.URIRef(BASE_URI), void["exampleResource"], rdflib.URIRef(BASE_URI + "soc2000/")))
g.flush()
