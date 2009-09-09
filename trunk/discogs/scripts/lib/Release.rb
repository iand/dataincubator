require 'rexml/document'
require 'uri'
require 'cgi'
require 'Util'
require 'DiscogResource'
require 'Label'
require 'Artist'
require 'Track'
class Release < DiscogResource
  
  def initialize(string)
    super(string)
    @id = @root.attributes["id"]
    @title = @root.get_elements("title")[0].get_text
    
    artists = @root.get_elements("artists")[0]
    @artists = []
    artists.get_elements("artist").each do |artist|
      name = artist.get_elements("name")[0].text
      if name
        @artists << Artist.create_uri( name )  
      end      
    end

    labels = @root.get_elements("labels")[0]
    @labels = []
    labels.get_elements("label").each do |label|
      #TODO catno
      name = label.attributes["name"]
      @labels << Label.create_uri( name )
    end
        
    notes = @root.get_elements("notes")[0]
    @notes = notes.get_text unless notes == nil
    released = @root.get_elements("released")[0]
    if released
      @released = released.text
      #clean up dates
      if @released.match("-00-00")
        @released = @released[0..3]
      end
      if @released.match("-00")
        @released = @released[0..@released.length-4]
      end    
      if @released.length == 4
        @release_date_format = "http://www.w3.org/2001/XMLSchema#year"
      elsif @released.length == 7
        @release_date_format = "http://www.w3.org/2001/XMLSchema#gYearMonth"
      else
        @release_date_format = "http://www.w3.org/2001/XMLSchema#date"  
      end

    end
    
    
    tracklist = @root.get_elements("tracklist")[0]
    @tracks = []
    if tracklist != nil    
      tracklist.get_elements("track").each_with_index do |track, i|
        @tracks << Track.new(@id, track, i+1)
      end      
    end
    
    #genres & styles -> SKOS
    genres = @root.get_elements("genres")[0]
    @genres = []
    if genres
      genres.get_elements("genre").each do |genre|
        @genres << genre
      end
    end
        
    styles = @root.get_elements("styles")[0]
    @styles = []
    if styles
      styles.get_elements("style").each do |style|
        @styles << style
      end
    end
        
    #TODO 
    #discogs record status
    #formats -> Manifestation?    
    #country (where released)
  end
  
  def dump_rdf()    
    uri = Release.create_uri(@id)
    
    rdf = "<mo:Record rdf:about=\"#{ uri  }\">\n"
    rdf << " <dc:title>#{@title}</dc:title>\n"
    rdf << " <mo:discogs rdf:resource=\"http://www.discogs.com/release/#{ @id }\"/>\n"    
        
    rdf << " <rdfs:comment>#{@notes}</rdfs:comment>\n"        
    if @released    
      rdf << " <dc:issued rdf:datatype=\"#{@release_date_format}\">#{@released}</dc:issued>\n"      
    end
    
    @images.each do |image|
      rdf << " <foaf:depiction>\n"
      rdf << dump_image(image, "Photo of #{@title}", uri)
      rdf << " </foaf:depiction>\n"  
    end
    
    @artists.each do |artist|      
      rdf << " <foaf:maker rdf:resource=\"#{ Util.escape_xml(artist) }\" />\n"        
    end

    @labels.each do |label|
      rdf << " <mo:publisher rdf:resource=\"#{ Util.escape_xml(label) }\" />\n"        
    end

    @tracks.each do |track|
      rdf << " <mo:track>\n"
      rdf << track.to_rdf()        
      rdf << " </mo:track>\n"
    end
    
    #TODO genres and formats -- these will be skos concepts linked to relevant scheme
    #but how do we associate a Record with its scheme. Its not its "subject" or "topic" 
        
    rdf << "</mo:Record>\n"
    return rdf
  end
    
  def Release.create_uri(id)
    return Util.canonicalize("/release/#{id}")
  end
end