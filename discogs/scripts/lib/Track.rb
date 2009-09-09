require 'rexml/document'
require 'uri'
require 'cgi'
require 'Util'
require 'DiscogResource'
require 'Artist'

class Track
  
  def initialize(release_id, element, number)
    @element = element
    @number = number
    @release_id = release_id
    @position = element.get_elements("position")[0].text
    @title = element.get_elements("title")[0].get_text
    
    artists = @element.get_elements("artists")[0]
    @artists = []
    if artists != nil
      artists.get_elements("artist").each do |artist|
        name = artist.get_elements("name")[0].text
        @artists << Artist.create_uri( name )
      end      
    end
    
    #duration
    duration = @element.get_elements("duration")[0]
    if duration && duration.text
      @duration="PT#{duration.text.gsub(":", "M")}S"
    end
    
    #TODO
    #extrartists -> role. See roles.txt
    
  end
  
  def to_rdf()
    uri = Track.create_uri(@release_id, @position)
    
    rdf = "<mo:Track rdf:about=\"#{ uri  }\">\n"
    rdf << " <dc:title>#{@title}</dc:title>\n"
    rdf << " <dc:isPartOf rdf:resource=\"#{ Release.create_uri(@release_id) }\"/>\n"
    #TODO resolve whether to use consecutive numbering or alphanumeric. Could rdf:List and record position too?
    #Note not using discogs position here, as its alphanumeric. Why is that? A1, A2, B1, B2 -- sides of record?
    #If so, then our track number is consecutive across sides of media
    rdf << " <mo:track_number rdf:datatype=\"http://www.w3.org/2001/XMLSchema#int\">#{@number}</mo:track_number>\n"
    
    if @duration
      rdf << " <time:duration rdf:datatype=\"http://www.w3.org/2001/XMLSchema#duration\">#{@duration}</time:duration>"  
    end
        
    @artists.each do |artist|      
      rdf << " <foaf:maker rdf:resource=\"#{ Util.escape_xml(artist) }\" />\n"        
    end
        
    rdf << "</mo:Track>\n"
  end
  
  def Track.create_uri(release_id, position)
    #using position rather than title
    if position
      slug = Util.slug(position)
    else
      slug = "unknown"  
    end    
    return Util.canonicalize("/release/#{release_id}/track/#{ CGI.escape(slug) }")    
  end
  
end