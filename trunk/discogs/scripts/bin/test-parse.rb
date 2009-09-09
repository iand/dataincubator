require 'rubygems'
#require 'xml/libxml'
require 'rexml/document'

#XML::Error.set_handler(&XML::Error::QUIET_HANDLER)

Dir.glob( "#{ARGV[0]}/*.xml" ).each do |f|
  begin        
      #parser = XML::Parser.file( f )
      #doc = parser.parse

      doc = REXML::Document.new( File.new( f ) )
  rescue StandardError => e
      puts "#{f} is invalid"
      #puts e
  end  
end
