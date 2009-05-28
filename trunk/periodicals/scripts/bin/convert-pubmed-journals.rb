$KCODE = 'u'
$:.unshift File.join(File.dirname(__FILE__), "..", "lib")
require "PubmedJournal"
require 'jcode'
  
fields = nil
count = 0
out = File.new( File.join(ARGV[1], "pubmed.rdf"), "w")
out.write Util.rdf_root       
File.new(ARGV[0], "r").each_line do |line|
  if line.match("---")
    if fields != nil
      journal = PubmedJournal.new(fields)      
      journal.to_rdf(out)
      count = count + 1
      
      if count % 1000 == 0
        out.write Util.rdf_end
        out.close()
        
        out = File.new( File.join(ARGV[1], "pubmed-#{count}.rdf"), "w")
        out.write Util.rdf_root      
        
      end
            
    end
    fields = Hash.new
  else
    field, value = line.split(": ")
    fields[field] = Util.clean_ws( value )    
  end
end
  
out.write Util.rdf_end
out.close()

p "Total #{count} results"

