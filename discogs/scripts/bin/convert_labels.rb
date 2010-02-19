$:.unshift File.join(File.dirname(__FILE__), "..", "lib")
require 'rubygems'
require 'pho'
require 'Label'
require 'Util'

#Where we're reading from
CACHE_DIR = ARGV[0]
#Where we're writing to
DATA_DIR = ARGV[1]

Dir.chdir( CACHE_DIR )
label_files = Dir.glob("discogs_*_labels.xml")
if label_files.length() == 0
  puts "Unable to find labels file"
  exit(1)
end
labels = label_files[0]

file = File.new(labels)
label_chunk = ""
count = 0
out = File.new( "#{ARGV[1]}/labels_#{count}.nt", "w")
#out = File.new( "#{ARGV[1]}/labels_#{count}.rdf", "w")
#out.puts( Util.rdf_root() )

file.each do |line|        
    label_chunk << line 
    if line.match(/<\/label>$/)
      #completed label      
      count = count + 1
      begin
       label = Label.new(label_chunk)
        out.puts( label.to_rdf(false) )
      rescue StandardError => e
        puts e
        puts e.backtrace
        $stderr.puts label_chunk
      end
      
      #break if count == 1000
      
      if count % 50000 == 0
        puts "Completed #{count}"
        #out.puts( Util.rdf_end() )
        out.close()
        out = File.new( "#{ARGV[1]}/labels_#{count}.nt", "w")
        #out = File.new( "#{ARGV[1]}/labels_#{count}.rdf", "w")
        #out.puts( Util.rdf_root() )
      end
            
      label_chunk = ""
    end  
end

#out.puts( Util.rdf_end() )