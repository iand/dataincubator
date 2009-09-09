$:.unshift File.join(File.dirname(__FILE__), "..", "lib")
require 'Release'

f = File.new(ARGV[0])
data = f.read()
release = Release.new(data)
puts release.to_rdf() 