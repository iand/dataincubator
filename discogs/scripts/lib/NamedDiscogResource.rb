require 'libxml'
require 'uri'
require 'cgi'
require 'Util'
require 'DiscogResource'

class NamedDiscogResource < DiscogResource
  
  attr_reader :raw_name, :name, :urls
  def initialize(string)
    super(string)
        
    @raw_name = @root.find_first("name").first.content
    @name = Util.clean_escape( @raw_name )
    
    @urls = Array.new
    urls = @root.find_first("urls")
    if urls != nil
      urls.find("url").each do |url|
          if url.first && url.first.content != nil && url.first.content != ""
            href = Util.clean_ws(url.first.content)
            if href != nil
              location = href.strip.downcase
              if location.start_with?("www")
                location = "http://#{location}"
              end
              @urls << location if location.start_with?("http://")  
            end           
            
          end
      end      
    end
        
  end
  
end