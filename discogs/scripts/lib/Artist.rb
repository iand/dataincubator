require 'rexml/document'
require 'uri'
require 'cgi'
require 'Util'
require 'NamedDiscogResource'

class Artist < NamedDiscogResource
  
  def initialize(string)
    super(string)

    @realname = get_optional_tag("realname")
    #@profile = get_optional_tag("profile")
    profile = @root.get_elements("profile")[0]
    if profile != nil
      @profile = profile.get_text  
    end
        
    #aliases
    #each is a separate record. Should be preserved as distinct entities, not really sameas?
    
    #groups
    @groups = Array.new
    groups = @root.get_elements("groups")[0]
    if groups != nil
      groups.get_elements("name").each do |group|
          if group.text != nil
            name = Util.clean_ws(group.text)
            if name != nil
              @groups << Artist.create_uri( name ) 
            end                       
          end
      end      
    end        
    
  end  
  
  def dump_rdf()    
    uri = Util.escape_xml( Artist.create_uri( @raw_name ) )
    rdf = "<#{rdf_type()} rdf:about=\"#{ uri }\">\n"
    
    rdf << " <foaf:name>#{@name}</foaf:name>\n"
    if @realname
      rdf << " <foaf:name>#{@realname}</foaf:name>\n"
    end
        
    rdf << " <mo:discogs rdf:resource=\"http://www.discogs.com/artist/#{ Util.escape_xml( CGI::escape(@raw_name) ) }\"/>\n"
    @urls.each do |url|      
      
      #hack to strip comments after urls in data
      #TODO: comma-sep
      url = url.split(" ")[0]
      url = Util.clean_url(url)
      begin
        
        URI.parse(url)
              
        if ( /twitter\.com\/([a-zA-Z0-9]+)/.match(url) )
          account_name = /twitter\.com\/([a-zA-Z0-9]+)/.match(url)[1]
          rdf << " <foaf:holdsAccount>\n"
          rdf << "  <foaf:OnlineAccount rdf:about=\"#{uri}/twitter/account_name\">\n"
          rdf << "    <rdf:type rdf:resource=\"http://rdfs.org/sioc/ns#User\"/>\n"
          rdf << "    <foaf:accountName>#{account_name}</foaf:accountName>\n"
          rdf << "    <foaf:accountServiceHomepage rdf:resource=\"http://www.twitter.com\"/>\n"
          rdf << "  </foaf:OnlineAccount>\n"
          rdf << " </foaf:holdsAccount>\n"
        else
          rdf << " <foaf:isPrimaryTopicOf rdf:resource=\"#{ Util.escape_xml(url) }\"/>\n"                
        end
        
        if ( /en\.wikipedia\.org/.match(url) )
          dbpedia_uri = url.sub("en.wikipedia.org/wiki", "dbpedia.org/resource")
          rdf << " <owl:sameAs rdf:resource=\"#{ Util.escape_xml( dbpedia_uri ) }\"/>\n"  
        end
  
        if ( /wikipedia\.org/.match(url) )
          rdf << " <mo:wikipedia rdf:resource=\"#{ Util.escape_xml(url) }\"/>\n"  
        end            
        
        if ( /www\.myspace\.com/.match(url) )
          rdf << " <mo:myspace rdf:resource=\"#{ Util.escape_xml(url) }\"/>\n"
          
          #TODO using seeAlso rather than sameas as sometimes records have >1 myspace account associated with them  
          dbtune_uri = url.sub("www.myspace.com", "dbtune.org/myspace")
          rdf << " <rdfs:seeAlso rdf:resource=\"#{ Util.escape_xml(dbtune_uri) }\"/>\n"
        end
      rescue
        puts "invalid URI: #{url}"
      end            
    end
    
    @groups.each do |group|      
      rdf << " <mo:member_of rdf:resource=\"#{ Util.escape_xml(group) }\"/>\n"
    end
        
    @images.each do |image|
      rdf << " <foaf:depiction>\n"
      rdf << dump_image(image, "Photo of #{Util.escape_xml( @raw_name )}", uri)
      rdf << " </foaf:depiction>\n"  
    end
        
    if @profile != nil
      rdf << " <dc:description>#{@profile}</dc:description>\n"  
    end    
        
    rdf << "</#{rdf_type()}>\n"
    return rdf
      
  end

  def rdf_type()
    if @root.get_elements("members").length() == 0
      return "mo:MusicArtist"
    end
    return "mo:MusicGroup"
  end
  
  def Artist.create_uri(name)
    slug = Util.slug(name)
    return Util.canonicalize("/artist/#{ CGI.escape(slug) }")
  end
      
end