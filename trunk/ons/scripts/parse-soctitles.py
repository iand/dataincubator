# Converts the Standard Occupational Classification 2000 (SOC2000) to SKxOS
# Run pdftotext -layout soc2000.pdf soc2000.txt first
import rdflib
import re
from graphutils import BatchGraph
from time import strftime

def slugify(inStr):
  removelist = ["a", "an", "as", "at", "before", "but", "by", "for","from","is", "in", "into", "like", "of", "off", "on", "onto","per","since", "than", "the", "this", "that", "to", "up", "via","with"];
  for a in removelist:
      aslug = re.sub(r'\b'+a+r'\b','',inStr)
  aslug = re.sub('[^\w\s-]', '', aslug).strip().lower()
  aslug = re.sub('\s+', '-', aslug)
  return aslug



BASE_URI = "http://ons.dataincubator.org/"
rdf = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")
dct = rdflib.Namespace("http://purl.org/dc/terms/")
skos = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
void = rdflib.Namespace("http://rdfs.org/ns/void#")

g = BatchGraph(30000, "output/soctitles", "rdf")
g.bind("rdf", rdf)
g.bind("rdfs", rdfs)
g.bind("dct", dct)
g.bind("skos", skos)
g.bind("void", void)
scheme_resource = rdflib.URIRef(BASE_URI + "soctitles/")  
g.add((scheme_resource, skos["prefLabel"], rdflib.Literal("Job titles classified under the Standard Occupational Classification 2000 (SOC2000) maintained by the Office of National Statistics.")))
g.add((scheme_resource, dct["description"], rdflib.Literal("An alphabetical list of over 26,000 job titles each one linked to a unit group of both the 1990 and 2000 editions of the classification.")))
g.add((scheme_resource, rdf["type"], skos["ConceptScheme"]))
g.add((scheme_resource, dct["rights"], rdflib.Literal("The data and text in this classification scheme is under Crown Copyright")))
g.add((scheme_resource, dct["source"], rdflib.URIRef("http://www.ons.gov.uk/about-statistics/classifications/current/SOC2000/dissemination/soc2000-index.xls")))
g.add((scheme_resource, rdfs["seeAlso"], rdflib.URIRef("http://www.ons.gov.uk/about-statistics/classifications/current/SOC2000/dissemination/index.html")))


# job titles
f = open("../data/soc2000-titles.csv", "r")
for line in f:
  m = re.match('^(.*)\t(.*)\t(.*)\t(.*)\t([0-9]+)\t([0-9]+)\t(.*)\t(.*)\t(.*)\t(.*)$', line)
  if m is not None:
    title = m.group(7).strip() + "  " + m.group(8).strip() + " " + m.group(9).strip()
    title = title.strip()
    id = slugify( title )
    concept_resource = rdflib.URIRef(BASE_URI + "soctitles/" + id)
    g.add((concept_resource, rdf["type"], skos["Concept"]))
    g.add((concept_resource, skos["prefLabel"], rdflib.Literal(title)))
    g.add((concept_resource, skos["broader"], rdflib.URIRef(BASE_URI + "soc2000/" + m.group(6))))
    g.add((rdflib.URIRef(BASE_URI + "soc2000/" + m.group(6)), skos["narrower"], concept_resource))
    g.add((concept_resource, skos["broader"], rdflib.URIRef(BASE_URI + "soc1990/" + m.group(5))))
    g.add((rdflib.URIRef(BASE_URI + "soc1990/" + m.group(5)), skos["narrower"], concept_resource))
    g.add((rdflib.URIRef(BASE_URI + "soc1990/" + m.group(5)), skos["closeMatch"], rdflib.URIRef(BASE_URI + "soc2000/" + m.group(6))))
    g.add((rdflib.URIRef(BASE_URI + "soc2000/" + m.group(6)), skos["closeMatch"], rdflib.URIRef(BASE_URI + "soc1990/" + m.group(5))))

f.close()

g.add((rdflib.URIRef(BASE_URI), void["exampleResource"], rdflib.URIRef(BASE_URI + "soctitles/")))
g.flush()
