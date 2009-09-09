#Split labels file

f = File.new(ARGV[0])
count = 1
out = File.new( "/home/ldodds/data/discogs/xml/labels/#{count}.xml", "w")
f.each do |line|        
    if line.match(/<\/label>$/)
      out.puts(line)
      count += 1
      out = File.new( "/home/ldodds/data/discogs/xml/labels/#{count}.xml", "w")
    else
      out.puts(line)  
    end  
end