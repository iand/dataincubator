$:.unshift File.join(File.dirname(__FILE__), "..", "lib")
require 'Artist'

f = File.new(ARGV[0])
data = f.read()
label = Artist.new(data)
puts label.to_rdf() 