require 'rexml/document'
require 'uri'
require 'cgi'
require 'Util'
require 'DiscogResource'

class NamedDiscogResource < DiscogResource
  
  def initialize(string)
    super(string)
        
    @raw_name = @root.get_elements("name")[0].text
    @name = Util.clean_escape( @raw_name )
    
    @urls = Array.new
    urls = @root.get_elements("urls")[0]
    if urls != nil
      urls.get_elements("url").each do |url|
          if url.text != nil
            href = Util.clean_ws(url.text)
            if href != nil
              @urls << href.strip  
            end           
            
          end
      end      
    end
        
  end
  
end