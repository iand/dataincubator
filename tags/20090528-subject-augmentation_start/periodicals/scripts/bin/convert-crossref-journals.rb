$KCODE = 'u'
$:.unshift File.join(File.dirname(__FILE__), "..", "lib")
#parseexcel ruby gem.
require 'rubygems'
require 'CrossRefJournal'
require 'fastercsv'
require 'jcode'
filenum = 1
out = File.new( File.join( ARGV[1], "crossref-#{filenum}.rdf" ), "w")
out.write Util.rdf_root  

reader = FasterCSV.open(ARGV[0], 'r')
reader.shift  
i = 0
reader.each do |row|
  i = i+1
  fields = Hash.new
  fields["title"] = row[0]
  fields["publisher"] = row[1]
  fields["subjects"] = row[2]
  if (row[3] != nil)
    issn = row[3].split('|')[0]
    eissn = row[3].split('|')[1]
    if (issn != nil && issn.length == 8)
      fields["ISSN"] = issn.insert(4,'-')
    end
    if (eissn != nil && eissn.length == 8)
      fields["EISSN"] = eissn.insert(4,'-')
    end
  end
  fields["doi"] = row[4]
  journal = CrossRefJournal.new(fields)   
  journal.to_rdf(out)   
  if i%1000 == 0
    p "Processed #{i} results > crossref-#{filenum}.rdf"
    filenum = filenum+1
    out.write Util.rdf_end
    out.close()
    out = File.new( File.join( ARGV[1], "crossref-#{filenum}.rdf" ), "w")
    out.write Util.rdf_root
  end
end

out.write Util.rdf_end
out.close()

p "Processed #{i} results > crossref-#{filenum}.rdf"
p "Total #{i} results, #{filenum} files created"


  
