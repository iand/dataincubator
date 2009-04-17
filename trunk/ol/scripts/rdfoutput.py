try:
	from ezgraph import Graph
	from ezgraph.graphlib import digraph
except ImportError:
	import sys
	sys.path.append("/home/kier/projects/recommender/")
	import graph as graphlib
	import gv as graphvis
	digraph = graphlib.digraph
	class Graph:
		def __init__(self):
			self.nodes = []
			self.edges = {}
			self.add_node = lambda n: self.nodes.append(n)
			self.add_edge = lambda f, t, n=None: self.edges.__setitem__((f, t), n)
		def get_graph(self, cls=graphlib.graph):
			g = cls()
			for n in self.nodes:
				g.add_node(n)
			for (f, t), n in self.edges.items():
				if n is not None:
					g.add_edge(f, t, label=n)
				else:
					g.add_edge(f, t)
			return g
		def get_graphvis(self, cls=graphlib.graph):
			g1 = self.get_graph(cls)
			dot = g1.write(fmt="dot")
			g2 = graphvis.readstring(str(dot))
			graphvis.layout(g2, "dot")
			return g2
		def render(self, fname, format="png", cls=graphlib.graph):
			g = self.get_graphvis(cls)
			graphvis.render(g, format, fname)
reg_pref = {
	"rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
	"rdfs" : "http://www.w3.org/2000/01/rdf-schema#",
	"owl" : "http://www.w3.org/2002/07/owl#",
	"cs" : "http://purl.org/vocab/changeset/schema#",
	"bf" : "http://schemas.talis.com/2006/bigfoot/configuration#",
	"frm" : "http://schemas.talis.com/2006/frame/schema#",
	"dc" : "http://purl.org/dc/elements/1.1/",
	"dct" : "http://purl.org/dc/terms/",
	"dctype" : "http://purl.org/dc/dcmitype/",
	"foaf" : "http://xmlns.com/foaf/0.1/",
	"bio" : "http://purl.org/vocab/bio/0.1/",
	"geo" : "http://www.w3.org/2003/01/geo/wgs84_pos#",
	"rel" : "http://purl.org/vocab/relationship/",
	"rss" : "http://purl.org/rss/1.0/",
	"wn" : "http://xmlns.com/wordnet/1.6/",
	"air" : "http://www.daml.org/2001/10/html/airport-ont#",
	"contact" : "http://www.w3.org/2000/10/swap/pim/contact#",
	"ical" : "http://www.w3.org/2002/12/cal/ical#",
	"icaltzd" : "http://www.w3.org/2002/12/cal/icaltzd#",
	"frbr" : "http://purl.org/vocab/frbr/core#",
	"ad" : "http://schemas.talis.com/2005/address/schema#",
	"lib" : "http://schemas.talis.com/2005/library/schema#",
	"dir" : "http://schemas.talis.com/2005/dir/schema#",
	"user" : "http://schemas.talis.com/2005/user/schema#",
	"sv" : "http://schemas.talis.com/2005/service/schema#",
	"mo" : "http://purl.org/ontology/mo/",
	"status" : "http://www.w3.org/2003/06/sw-vocab-status/ns#",
	"label" : "http://purl.org/net/vocab/2004/03/label#",
	"skos" : "http://www.w3.org/2004/02/skos/core#",
}
reg_ns = {}
for k, v in reg_pref.items():
	reg_ns[v] = k
me = [
	("http://iandavis.com/id/kier.turtle", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://xmlns.com/foaf/0.1/Document"),
	("http://iandavis.com/id/kier.turtle", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://purl.org/dc/dcmitype/Text"),
	("http://iandavis.com/id/kier.turtle", "http://xmlns.com/foaf/0.1/primaryTopic", "http://iandavis.com/id/kier"),
	("http://iandavis.com/id/kier.turtle", "http://purl.org/dc/terms/hasFormat", "http://iandavis.com/id/kier.rdf"),
	("http://iandavis.com/id/kier.turtle", "http://purl.org/dc/terms/hasFormat", "http://iandavis.com/id/kier.html"),
	("http://iandavis.com/id/kier.turtle", "http://purl.org/dc/terms/hasFormat", "http://iandavis.com/id/kier.xml"),
	("http://iandavis.com/id/kier.turtle", "http://purl.org/dc/terms/hasFormat", "http://iandavis.com/id/kier.json"),
	("http://iandavis.com/id/kier.turtle", "http://xmlns.com/foaf/0.1/topic", "http://iandavis.com/id/kier"),
	("http://iandavis.com/id/kier.rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://purl.org/dc/dcmitype/Text"),
	("http://iandavis.com/id/kier.rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://xmlns.com/foaf/0.1/Document"),
	("http://iandavis.com/id/kier.rdf", "http://purl.org/dc/elements/1.1/format", "'application/rdf+xml'"),
	("http://iandavis.com/id/kier.rdf", "http://www.w3.org/2000/01/rdf-schema#label", "'RDF/XML'"),
	("http://iandavis.com/id/kier.html", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://purl.org/dc/dcmitype/Text"),
	("http://iandavis.com/id/kier.html", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://xmlns.com/foaf/0.1/Document"),
	("http://iandavis.com/id/kier.html", "http://purl.org/dc/elements/1.1/format", "'text/html'"),
	("http://iandavis.com/id/kier.html", "http://www.w3.org/2000/01/rdf-schema#label", "'HTML'"),
	("http://iandavis.com/id/kier.xml", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://purl.org/dc/dcmitype/Text"),
	("http://iandavis.com/id/kier.xml", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://xmlns.com/foaf/0.1/Document"),
	("http://iandavis.com/id/kier.xml", "http://purl.org/dc/elements/1.1/format", "'application/xml'"),
	("http://iandavis.com/id/kier.xml", "http://www.w3.org/2000/01/rdf-schema#label", "'XML'"),
	("http://iandavis.com/id/kier.json", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://purl.org/dc/dcmitype/Text"),
	("http://iandavis.com/id/kier.json", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://xmlns.com/foaf/0.1/Document"),
	("http://iandavis.com/id/kier.json", "http://purl.org/dc/elements/1.1/format", "'application/json'"),
	("http://iandavis.com/id/kier.json", "http://www.w3.org/2000/01/rdf-schema#label", "'JSON'"),
	("http://iandavis.com/id/kier", "http://xmlns.com/foaf/0.1/name", "'Kier Davis'"),
	("http://iandavis.com/id/kier", "http://xmlns.com/foaf/0.1/mbox_sha1sum", "'b1e91635028f5ee5f79cbd49dbeafc330852d26a'"),
	("http://iandavis.com/id/kier", "http://xmlns.com/foaf/0.1/knows", "http://iandavis.com/id/me"),
	("http://iandavis.com/id/kier", "http://xmlns.com/foaf/0.1/knows", "http://iandavis.com/id/steph"),
	("http://iandavis.com/id/kier", "http://xmlns.com/foaf/0.1/knows", "http://iandavis.com/id/freya"),
	("http://iandavis.com/id/kier", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "http://xmlns.com/foaf/0.1/Person"),
	("http://iandavis.com/id/kier", "http://purl.org/vocab/relationship/siblingOf", "http://iandavis.com/id/freya"),
	("http://iandavis.com/id/kier", "http://purl.org/vocab/relationship/childOf", "http://iandavis.com/id/me"),
	("http://iandavis.com/id/kier", "http://purl.org/vocab/relationship/childOf", "http://iandavis.com/id/steph"),
]
ns_id = 0
def register(pref, uri):
	global reg_pref, reg_ns
	reg_pref[pref] = uri
	reg_ns[uri] = pref
def make_ns(uri):
	global reg_ns, ns_id
	parts = uri.split("#")
	if len(parts) < 2:
		parts = uri.split("/")
		start = "/".join(parts[:-1]) + "/"
		end = parts[-1]
	else:
		start = parts[0] + "#"
		end = parts[1]
	if start in reg_ns:
		return reg_ns[start] + ":" + end
	else:
		p = "ns" + str(ns_id)
		ns_id += 1
		reg_ns[start] = p
		return p + ":" + end
def make_table(triples):
	triples = list(triples)
	w = 45
	print u"\u250F\u2501" + (u"\u2501" * w) + u"\u2501\u252F\u2501" + (u"\u2501" * w) + u"\u2501\u252F\u2501" + (u"\u2501" * w) + u"\u2501\u2513"
	print u"\u2503 " + u"Subject".ljust(w, u" ") + u" \u2502 " + u"Predicate".ljust(w, u" ") + u" \u2502 " + u"Object".ljust(w, u" ") + u" \u2503"
	triples.sort()
	lastsubj = None
	lastpred = None
	used = []
	for s, p, o in triples:
		if (s, p, o) in used:
			continue
		p = make_ns(p)
		if s != lastsubj:
			print u"\u2520\u2500" + (u"\u2500" * w) + u"\u2500\u253C\u2500" + (u"\u2500" * w) + u"\u2500\u253C\u2500" + (u"\u2500" * w) + u"\u2500\u2528"
		elif p != lastpred:
			print u"\u2503 " + (u" " * w) + u" \u251C\u2500" + (u"\u2500" * w) + u"\u2500\u253C\u2500" + (u"\u2500" * w) + u"\u2500\u2528"
		else:
			print u"\u2503 " + (u" " * w) + u" \u2502 " + (u" " * w) + u" \u251C\u2500" + (u"\u2500" * w) + u"\u2500\u2528"
		if s != lastsubj:
			lastsubj = s
			lastpred = None
		else:
			s = ""
		if p != lastpred:
			lastpred = p
		else:
			p = ""
		if len(s) > w:
			s = s[:40] + "..."
		else:
			s = s.ljust(w, " ")
		if len(p) > w:
			p = p[:40] + "..."
		else:
			p = p.ljust(w, " ")
		if len(o) > w:
			o = o[:40] + "..."
		else:
			o = o.ljust(w, " ")
		print u"\u2503 " + s + u" \u2502 " + p + u" \u2502 " + o + u" \u2503"
		used.append((s, p, o))
	print u"\u2517\u2501" + (u"\u2501" * w) + u"\u2501\u2537\u2501" + (u"\u2501" * w) + u"\u2501\u2537\u2501" + (u"\u2501" * w) + u"\u2501\u251B"
def from_rdflib(rdflib, graph):
	t = graph.triples((None, None, None))
	res = []
	for s, p, o in t:
		s = str(s)
		p = str(p)
		if isinstance(o, rdflib.Literal):
			o = "'" + str(o) + "'"
		else:
			o = str(o)
		res.append((s, p, o))
	return res
def make_graph(triples, fname="output.png"):
	triples = list(triples)
	subjects, predicates, objects = zip(*triples)
	g = Graph()
	for subject in subjects:
		#g.add_node(make_ns(subject))
		g.add_node(subject)
	for object in objects:
		#if object[0] in "\"'":
		#	g.add_node(object)
		#else:
		#	g.add_node(make_ns(object))
		g.add_node(object)
	for s, p, o in triples:
		#if o[0] in "\"'":
		#	g.add_edge(make_ns(s), o, make_ns(p))
		#else:
		#	g.add_edge(make_ns(s), make_ns(o), make_ns(p))
		g.add_edge(s, o, make_ns(p))
	g.render(fname, "png", digraph)
if __name__ == "__main__":
	make_table(me)
	make_graph(me)	
