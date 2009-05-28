import rdflib

class BatchGraph:
  def __init__(self, batch_size, file_prefix, format):
    self.current_batch = 1
    self.batch_size = batch_size
    self.file_prefix = file_prefix
    self.format = format
    self.bindings = {}
    self.reset()
    
  def reset(self):
    self.g = rdflib.ConjunctiveGraph()
    self.triple_count = 0
    for prefix, ns in self.bindings.items():
      self.g.bind(prefix, ns)
      
  
  def bind(self, prefix, ns):
    self.bindings[prefix] =  ns
    self.g.bind(prefix, ns)

  def add(self, triple):
    self.g.add(triple)
    self.triple_count += 1
    if self.triple_count >= self.batch_size:
      self.flush()

  def flush(self):
    g_file = open("%s_%s.%s" % (self.file_prefix, self.current_batch, self.format), "w")
    if self.format == "nt":
      format_name = "ntriples"
    else:
      format_name = "pretty-xml"
      
    g_file.write(self.g.serialize(format=format_name))
    g_file.close()
    self.reset()
    self.current_batch += 1

  def serialize(self, format):
    return self.g.serialize(format)
