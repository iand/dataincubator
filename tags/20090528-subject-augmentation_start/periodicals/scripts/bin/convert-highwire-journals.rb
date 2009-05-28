$KCODE = 'u'
$:.unshift File.join(File.dirname(__FILE__), "..", "lib")
#parseexcel ruby gem.
require 'rubygems'
require 'parseexcel'
require 'HighwireJournal'
require 'jcode'

workbook = Spreadsheet::ParseExcel.parse( ARGV[0] )
worksheet = workbook.worksheet(0)
#skip first row
skip = 1
filenum = 1
out = File.new( File.join( ARGV[1], "highwire-#{filenum}.rdf" ), "w")
out.write Util.rdf_root  
i = 1 
worksheet.each(skip) do |row|  
   fields = Hash.new
   fields["title"] = row.at(0).to_s("latin1").strip
# need to resolve UTF-8 issues before converting publisher
   fields["publisher"] = row.at(1).to_s("latin1").strip
   fields["homepage"] = row.at(2).to_s("latin1").strip
   fields["EISSN"] = row.at(3).to_s("latin1").strip
   fields["ISSN"] = row.at(4).to_s("latin1").strip
   journal = HighwireJournal.new(fields)   
   journal.to_rdf(out)   
   if i%100 == 0
     p "Processed #{i} results > highwire-#{filenum}.rdf"
     filenum = filenum+1
     out.write Util.rdf_end
     out.close()
     out = File.new( File.join( ARGV[1], "highwire-#{filenum}.rdf" ), "w")
     out.write Util.rdf_root
   end
   i = i+1   
end
out.write Util.rdf_end
out.close()

p "Processed #{i} results > highwire-#{filenum}.rdf"
p "Total #{i} results, #{filenum} files created"


  
