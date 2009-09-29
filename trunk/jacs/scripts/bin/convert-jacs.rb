$KCODE = 'u'
$:.unshift File.join(File.dirname(__FILE__), "..", "lib")
#parseexcel ruby gem.
require 'rubygems'
require 'JacsCode'
require 'fastercsv'
require 'jcode'
filenum = 1
out = File.new( File.join( ARGV[1], "jacs-#{filenum}.rdf" ), "w")
out.write Util.rdf_root  

out.write Util.skos_taxonomy_scheme

reader = FasterCSV.open(ARGV[0], 'r')
 
i = 0
reader.each do |row|
  i = i+1
    
  fields = Hash.new
  fields["code"] = row[0]
  fields["subject"] = row[1]
  
  if (row[2] != nil)
    fields["description"] = row[2]
  else
    fields["description"] = ""
  end

  jacsEntry = JacsCode.new(fields)   

  jacsEntry.to_rdf(out)   
  if i%1000 == 0
    p "Processed #{i} results > jacs-#{filenum}.rdf"
    filenum = filenum+1
    out.write Util.rdf_end
    out.close()
    out = File.new( File.join( ARGV[1], "jacs-#{filenum}.rdf" ), "w")
    out.write Util.rdf_root
  end
end

out.write Util.rdf_end
out.close()

p "Processed #{i} results > jacsEntry-#{filenum}.rdf"
p "Total #{i} results, #{filenum} files created"


  
