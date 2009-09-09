$:.unshift File.join(File.dirname(__FILE__), "..", "lib")
require 'rubygems'
require 'pho'
require 'Artist'
require 'Util'

#Where we're reading from
CACHE_DIR = ARGV[0]
#Where we're writing to
DATA_DIR = ARGV[1]

Dir.chdir( CACHE_DIR )
label_files = Dir.glob("discogs_*_artists.xml")
if label_files.length() == 0
  puts "Unable to find artists file"
  exit(1)
end
labels = label_files[0]

file = File.new(labels)
chunk = ""
count = 0
out = File.new( "#{ARGV[1]}/artists_#{count}.rdf", "w")
out.puts( Util.rdf_root() )

file.each do |line|        
    chunk << line 
    if line.match(/<\/artist>$/)
      #completed label      
      count = count + 1
      begin
       artist = Artist.new(chunk)
        out.puts( artist.to_rdf(false) )
      rescue StandardError => e
        puts e
        $stderr.puts chunk
      end
      
      #break if count == 1000
      
      if count % 2000 == 0
        puts "Completed #{count}"
        out.puts( Util.rdf_end() )
        out.close()                
        out = File.new( "#{ARGV[1]}/artists_#{count}.rdf", "w")
        out.puts( Util.rdf_root() )
      end
            
      chunk = ""
    end  
end

out.puts( Util.rdf_end() )