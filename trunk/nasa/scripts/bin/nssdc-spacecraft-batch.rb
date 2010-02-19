$:.unshift File.join(File.dirname(__FILE__), "..", "lib")

require 'NSSDCSpacecraft'
require 'Util'

#these are all holding pages for several flights, no actual spacecraft data
exclusions = [ "1965-024Z.html", "1966-073Z.html", "1968-118Z.html", "1966-045Z.html" ]

#the following are error pages from NASA site
exclusions << "1989-027A.html"
exclusions << "2007-048D.html"

Dir.chdir( ARGV[0] )
if !File.exists?(ARGV[1])
  Dir.mkdir( ARGV[1] )  
end

count = 0
out = File.new( File.join(ARGV[1], "nssdc.rdf"), "w")
out.write Util.rdf_root       

Dir.glob( "*.html" ).each { |filename|
    file = File.new( File.join(ARGV[0], filename) )  
    if exclusions.index(filename) != nil
      puts "Skipping excluded file #{filename}"
    else
      #TODO change times
#      if !File.exists?( File.join(ARGV[1], filename.gsub(/html/, "rdf") ) )
        begin    
          #puts "Processing #{filename}"          
          spacecraft = NSSDCSpacecraft.new( file )
          #datafile = File.new( File.join(ARGV[1], filename.gsub(/html/, "rdf") ), "w" )
          #datafile.puts spacecraft.to_rdf(true)
          #datafile.close()
          out.write spacecraft.to_rdf(false)
          count = count + 1

          if count % 1000 == 0
            out.write Util.rdf_end
            out.close()
            
            out = File.new( File.join(ARGV[1], "nssdc-#{count}.rdf"), "w")
            out.write Util.rdf_root      
            
          end
                    
        rescue StandardError => e
          #TODO ABLE1.html fails
          puts "Failed on #{filename}"
          puts e
          puts e.backtrace
        end      
#      end
    end
}

out.write Util.rdf_end
out.close()
  