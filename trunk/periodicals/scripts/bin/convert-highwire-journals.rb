$:.unshift File.join(File.dirname(__FILE__), "..", "lib")
#parseexcel ruby gem.
require 'rubygems'
require 'parseexcel'
require 'HighwireJournal'

workbook = Spreadsheet::ParseExcel.parse( ARGV[0] )
worksheet = workbook.worksheet(0)
#skip first row
skip = 1
out = File.new( File.join( ARGV[1], "highwire.rdf" ), "w")
out.write Util.rdf_root  
worksheet.each(skip) do |row|  
   fields = Hash.new
   fields["title"] = row.at(0).to_s("latin1").strip
   fields["publisher"] = row.at(1).to_s("latin1").strip
   fields["homepage"] = row.at(2).to_s("latin1").strip
   fields["EISSN"] = row.at(3).to_s("latin1").strip
   fields["ISSN"] = row.at(4).to_s("latin1").strip
   journal = HighwireJournal.new(fields)   
   journal.to_rdf(out)   
end
out.write Util.rdf_end
out.close()


  
