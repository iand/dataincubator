import urllib2
import json
import rdflib
import sys
import rdfoutput
JSON_URIS = [
	"file:///home/kier/openlibrary/Weaving-the-Web.json",
	"file:///home/kier/openlibrary/Open-Sources.json",
	"file:///home/kier/openlibrary/Python-Cookbook.json",
]
BASE_URI = "http://olrdf.appspot.com/key"
rdfoutput.register("bibo", "http://purl.org/ontology/bibo/")
rdfoutput.register("ol", "http://olrdf.appspot.com/key/")
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
skip = ["latest_revision", "id", "last_modified", "created"]
def download(uri):
	print "Downloading '%s'" % uri
	req = urllib2.Request(uri)
	resp = urllib2.urlopen(req)
	data = resp.read()
	resp.close()
	return json.read(data)
def convert(uris):
	graph = rdflib.ConjunctiveGraph()
	graph.bind("rdf", rdf)
	graph.bind("rdfs", rdfs)
	graph.bind("dct", dcterms)
	graph.bind("ol", ol)
	graph.bind("bibo", bibo)
	graph.bind("frbr", frbr)
	graph.bind("skos", skos)
	graph.bind("foaf", foaf)
	graph.bind("dc", dc)
	graph.bind("owl", owl)
	for uri in uris:
		data = download(uri)
		subj = rdflib.URIRef(BASE_URI + data["key"])
		graph.add((subj, foaf["isPrimaryTopicOf"], rdflib.URIRef("http://openlibrary.org" + data["key"])))
		for k, v in data.items():
			if k == "key":
				pass
			elif k == "type":
				if v["key"] == "/type/edition":
					graph.add((subj, rdf["type"], frbr["Manifestation"]))
				else:
					graph.add((subj, rdf["type"], rdflib.URIRef(BASE_URI + v["key"])))
			elif k == "title":
				graph.add((subj, rdfs["label"], rdflib.Literal(v)))
				graph.add((subj, skos["prefLabel"], rdflib.Literal(v)))
			elif k == "title_prefix":
				graph.add((subj, ol["title_prefix"], rdflib.Literal(data["title_prefix"])))
				sort_title = data["title"][len(data["title_prefix"]):].strip()
				graph.add((subj, ol["sort_title"], rdflib.Literal(sort_title)))
			elif k == "authors":
				bnode = rdflib.BNode()
				graph.add((subj, bibo["authorList"], bnode))
				graph.add((bnode, rdf["type"], rdf["Seq"]))
				i = 1
				for author in v:
					graph.add((bnode, rdf["_" + str(i)], rdflib.URIRef(BASE_URI + author["key"])))
					i += 1
			elif k == "other_titles":
				for t in v:
					graph.add((subj, skos["altLabel"], rdflib.Literal(t)))
			elif k == "subtitle":
				graph.add((subj, ol["subtitle"], rdflib.Literal(v)))
			elif k == "lc_classifications":
				for c in v:
					graph.add((subj, ol["lc_classification"], rdflib.Literal(c)))
			elif k == "contributions":
				bnode = rdflib.BNode()
				graph.add((subj, bibo["contributorList"], bnode))
				graph.add((bnode, rdf["type"], rdf["Bag"]))
				i = 1
				for c in v:
					person = rdflib.BNode()
					graph.add((person, rdf["type"], foaf["Person"]))
					graph.add((person, foaf["name"], rdflib.Literal(c)))
					graph.add((bnode, rdf["_" + str(i)], person))
					i += 1
			elif k == "edition_name":
				graph.add((subj, bibo["edition"], rdflib.Literal(v)))
			elif k == "subjects":
				for sub in v:
					graph.add((subj, dc["subject"], rdflib.Literal(sub)))
			elif k == "publish_country":
				graph.add((subj, ol["publish_country"], rdflib.Literal(v.strip())))
			elif k == "by_statement":
				graph.add((subj, ol["by_statement"], rdflib.Literal(v)))
			elif k == "oclc_numbers":
				for n in v:
					graph.add((subj, bibo["oclcnum"], rdflib.Literal(n)))
			elif k == "revision":
				s = rdflib.URIRef("http://openlibrary.org" + data["key"])
				graph.add((s, ol["revision"], rdflib.Literal(str(v))))
			elif k == "publishers":
				for p in v:
					graph.add((subj, dc["publisher"], rdflib.Literal(p)))
			elif k == "publish_places":
				for p in v:
					graph.add((subj, ol["publish_place"], rdflib.Literal(p)))
			elif k == "pagination":
				graph.add((subj, ol["pagination"], rdflib.Literal(v)))
			elif k == "lccn":
				for l in v:
					graph.add((subj, bibo["lccn"], rdflib.Literal(l)))
			elif k == "number_of_pages":
				graph.add((subj, ol["number_of_pages"], rdflib.Literal(str(v))))
			elif k == "isbn_10":
				for i in v:
					graph.add((subj, bibo["isbn10"], rdflib.Literal(i)))
					graph.add((subj, owl["sameAs"], rdflib.URIRef("http://www4.wiwiss.fu-berlin.de/bookmashup/books/" + i)))
			elif k == "isbn_13":
				for i in v:
					graph.add((subj, bibo["isbn13"], rdflib.Literal(i)))
			elif k == "publish_date":
				graph.add((subj, dcterms["issued"], rdflib.Literal(v)))
			elif k == "weight":
				graph.add((subj, ol["weight"], rdflib.Literal(v)))
			elif k == "physical_format":
				graph.add((subj, ol["physical_format"], rdflib.Literal(v)))
			elif k == "physical_dimensions":
				graph.add((subj, ol["physical_dimensions"], rdflib.Literal(v)))
			elif k == "dewey_decimal_class":
				for d in v:
					graph.add((subj, ol["dewey_decimal_class"], rdflib.Literal(v)))
			elif k == "notes":
				graph.add((subj, ol["notes"], rdflib.Literal(v["value"])))
			elif k == "first_sentence":
				graph.add((subj, ol["first_sentence"], rdflib.Literal(v["value"])))
			elif k == "description":
				graph.add((subj, dcterms["description"], rdflib.Literal(v["value"])))
			elif k == "series":
				for s in v:
					graph.add((subj, ol["series"], rdflib.Literal(s)))
			elif k == "languages":
				for l in v:
					graph.add((subj, dcterms["language"], rdflib.URIRef(BASE_URI + l["key"])))
			elif k == "table_of_contents":
				bnode = rdflib.BNode()
				graph.add((subj, dcterms["tableOfContents"], bnode))
				graph.add((bnode, rdf["type"], rdf["Seq"]))
				i = 1
				for x in v:
					section = rdflib.BNode()
					if x["type"]["key"] == "/type/toc_item":
						try:
							graph.add((section, skos["prefLabel"], x["title"]))
						except KeyError:
							continue
					elif x["type"] == "/type/text":
						graph.add((section, skos["prefLabel"], x["value"]))
					graph.add((section, rdf["type"], bibo["DocumentPart"]))
					graph.add((section, dcterms["isPartOf"], subj))
					graph.add((bnode, rdf["_" + str(i)], section))
					i += 1
			elif k in skip:
				pass
			else:
				print k, v
	f = open("output.rdf", "w")
	graph.serialize(f, "pretty-xml")
	f.close()
	print
	triples = rdfoutput.from_rdflib(rdflib, graph)
	rdfoutput.make_table(triples)
	#rdfoutput.make_graph(triples)
if __name__ == "__main__":
	convert(JSON_URIS)
