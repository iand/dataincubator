$:.unshift File.join(File.dirname(__FILE__), "..", "lib")
require 'Label'

f = File.new(ARGV[0])
data = f.read()
label = Label.new(data)
puts label.to_rdf() 