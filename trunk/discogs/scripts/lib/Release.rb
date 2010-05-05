require 'libxml'
require 'uri'
require 'cgi'
require 'Util'
require 'DiscogResource'
require 'Label'
require 'Artist'
require 'Track'
class Release < DiscogResource
  
  attr_reader :id, :title, :artists, :labels, :notes, :released, :tracks, :genres, :styles
  
  def initialize(string)    
    super(string)
    @id = @root.attributes["id"]
    @title = @root.find_first("title").first.content
    artists = @root.find_first("artists")
    @artists = []
    artists.find("artist").each do |artist|
      name = artist.find_first("name").first
      if name && name.content
        @artists << Artist.create_uri( name.content )  
      end      
    end

    labels = @root.find_first("labels")
    @labels = []
    labels.find("label").each do |label|
      #TODO catno
      name = label.attributes["name"]
      @labels << Label.create_uri( name )
    end
        
    notes = @root.find_first("notes")
    @notes = notes.first.content unless notes == nil
    released = @root.find_first("released")
    if released
      @released = released.first.content
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
    
    
    tracklist = @root.find_first("tracklist")
    @tracks = []
    if tracklist != nil    
      tracklist.find("track").each_with_index do |track, i|
        @tracks << Track.new(@id, track, i+1)
      end      
    end
    
    #genres & styles -> SKOS
    genres = @root.find_first("genres")
    @genres = []
    if genres
      genres.find("genre").each do |genre|
        @genres << genre
      end
    end
        
    styles = @root.find_first("styles")
    @styles = []
    if styles
      styles.find("style").each do |style|
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
    
    rdf = "<#{uri}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.org/ontology/mo/Record>.\n"
    #rdf = "<mo:Record rdf:about=\"#{ uri  }\">\n"
    rdf << "<#{uri}> <http://purl.org/dc/terms/title> \"#{Util.escape_ntriples(@title)}\".\n"
    #rdf << " <dc:title>#{@title}</dc:title>\n"
    rdf << "<#{uri}> <http://purl.org/ontology/mo/discogs> <http://www.discogs.com/release/#{ @id }>.\n"
    #rdf << " <mo:discogs rdf:resource=\"http://www.discogs.com/release/#{ @id }\"/>\n"    
    
    if @notes != nil
      rdf << "<#{uri}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#comment> \"#{Util.escape_ntriples(@notes)}\".\n"  
    end
      
    #rdf << " <rdfs:comment>#{@notes}</rdfs:comment>\n"        
    if @released    
      rdf << "<#{uri}> <http://purl.org/dc/terms/issued> \"#{@released}\"^^<#{@release_date_format}>.\n"
      #rdf << " <dc:issued rdf:datatype=\"#{@release_date_format}\">#{@released}</dc:issued>\n"      
    end
    
    @images.each do |image|
      #rdf << " <foaf:depiction>\n"
      rdf << "<#{uri}> <http://xmlns.com/foaf/0.1/depiction> <#{image["uri"]}>.\n"
      rdf << dump_image(image, "Photo of #{Util.escape_ntriples(@title)}", uri)
      #rdf << " </foaf:depiction>\n"  
    end
    
    @artists.each do |artist|
      rdf << "<#{uri}> <http://xmlns.com/foaf/0.1/maker> <#{ artist }>.\n"      
      #rdf << " <foaf:maker rdf:resource=\"#{ Util.escape_xml(artist) }\" />\n"        
    end

    @labels.each do |label|
      rdf << "<#{uri}> <http://purl.org/ontology/mo/publisher> <#{ label }>.\n"
      #rdf << " <mo:publisher rdf:resource=\"#{ Util.escape_xml(label) }\" />\n"        
    end

    @tracks.each do |track|
      rdf << "<#{uri}> <http://purl.org/ontology/mo/track> <#{track.uri}>.\n"
      #rdf << " <mo:track>\n"
      rdf << track.to_rdf()        
      #rdf << " </mo:track>\n"
    end
    
    #TODO genres and formats -- these will be skos concepts linked to relevant scheme
    #but how do we associate a Record with its scheme. Its not its "subject" or "topic" 
        
    #rdf << "</mo:Record>\n"
    return rdf
  end
    
  def Release.create_uri(id)
    return Util.canonicalize("/release/#{id}")
  end
end