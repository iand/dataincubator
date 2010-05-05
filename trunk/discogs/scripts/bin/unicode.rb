$:.unshift File.join(File.dirname(__FILE__), "..", "lib")
$KCODE="U"

require 'Release'

f = File.new("/home/ldodds/data/discogs/cache/releases/1.xml")
data = f.read()
release = Release.new(data)

puts Util.rdf_root()
puts "<rdf:Description rdf:about=\"\">"
release.tracks.each do |track|
  puts "<dc:title>" + track.title + "</dc:title>"
end
puts "</rdf:Description>"
puts Util.rdf_end()
#puts release.to_rdf() 