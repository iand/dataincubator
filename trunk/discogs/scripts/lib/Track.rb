require 'libxml'
require 'uri'
require 'cgi'
require 'Util'
require 'DiscogResource'
require 'Artist'
require 'Release'

class Track
  
  attr_reader :title
  
  def initialize(release_id, element, number)
    @element = element
    @number = number
    @release_id = release_id
    position = element.find_first("position").first
    if position != nil
      @position = position.content
    end
    title = element.find_first("title").first
    @title = title.content if title && title.content
    #puts element.find_first("title").inspect()
    #puts @title.inspect()
    
    artists = @element.find_first("artists")
    @artists = []
    if artists != nil
      artists.find("artist").each do |artist|
        name = artist.find_first("name").first.to_s
        @artists << Artist.create_uri( name )
      end      
    end
    
    #duration
    duration = @element.find_first("duration")
    if duration && duration.first.to_s != ""
      duration = duration.first.to_s.gsub("'", "M")
      duration = duration.first.to_s.gsub(":", "M")      
      @duration="PT#{duration}S"
    end
    
    #TODO
    #extrartists -> role. See roles.txt
    
  end
  
  def uri()
    return Track.create_uri(@release_id, @position)
  end
  
  def to_rdf()
    uri = Track.create_uri(@release_id, @position)
  
    rdf = "<#{uri}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/mo/Track>.\n"  
    #rdf = "<mo:Track rdf:about=\"#{ uri  }\">\n"
    if @title
      rdf << "<#{uri}> <http://purl.org/dc/terms/title> \"#{Util.escape_ntriples(@title)}\".\n"  
    end
     
    #rdf << " <dc:title>#{@title}</dc:title>\n"
    rdf << "<#{uri}> <http://purl.org/dc/terms/isPartOf> <#{ Release.create_uri(@release_id) }>.\n"
    #rdf << " <dc:isPartOf rdf:resource=\"#{ Release.create_uri(@release_id) }\"/>\n"
    #TODO resolve whether to use consecutive numbering or alphanumeric. Could rdf:List and record position too?
    #Note not using discogs position here, as its alphanumeric. Why is that? A1, A2, B1, B2 -- sides of record?
    #If so, then our track number is consecutive across sides of media
    rdf << "<#{uri}> <http://purl.org/ontology/mo/track_number> \"#{@number}\"^^<http://www.w3.org/2001/XMLSchema#int>.\n"
    #rdf << " <mo:track_number rdf:datatype=\"http://www.w3.org/2001/XMLSchema#int\">#{@number}</mo:track_number>\n"
    
    if @duration
      rdf << "<#{uri}> <http://purl.org/NET/c4dm/timeline.owl#duration> \"#{@duration}\"^^<http://www.w3.org/2001/XMLSchema#duration>.\n"
      #rdf << " <time:duration rdf:datatype=\"http://www.w3.org/2001/XMLSchema#duration\">#{@duration}</time:duration>"  
    end
        
    @artists.each do |artist|
      rdf << "<#{uri}> <http://xmlns.com/foaf/0.1/maker> <#{artist}>.\n"      
      #rdf << " <foaf:maker rdf:resource=\"#{ Util.escape_xml(artist) }\" />\n"        
    end
        
    #rdf << "</mo:Track>\n"
    return rdf
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