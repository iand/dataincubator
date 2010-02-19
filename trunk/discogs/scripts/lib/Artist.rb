require 'libxml'
require 'uri'
require 'cgi'
require 'Util'
require 'NamedDiscogResource'

class Artist < NamedDiscogResource
  
  def initialize(string)
    super(string)

    @realname = get_optional_tag("realname")
    #@profile = get_optional_tag("profile")
    profile = @root.find_first("profile")
    if profile != nil
      @profile = profile.first.content
    end
        
    #aliases
    #each is a separate record. Should be preserved as distinct entities, not really sameas?
    
    #groups
    @groups = Array.new
    groups = @root.find_first("groups")
    if groups != nil 
      groups.find("name").each do |group|
          if group.first.content != nil && group.first.content != ""
            name = Util.clean_ws(group.first.content)
            if name != nil
              @groups << Artist.create_uri( name ) 
            end                       
          end
      end      
    end        
    
  end  
  
  def dump_rdf()    
    uri = Util.escape_xml( Artist.create_uri( @raw_name ) )
    rdf = "<#{uri}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> #{rdf_type()}.\n"
    #rdf = "<#{rdf_type()} rdf:about=\"#{ uri }\">\n"
    
    rdf << "<#{uri}> <http://xmlns.com/foaf/0.1/name> \"#{Util.escape_ntriples(@name)}\".\n"
    #rdf << " <foaf:name>#{@name}</foaf:name>\n"
    if @realname
      rdf << "<#{uri}> <http://xmlns.com/foaf/0.1/name> \"#{Util.escape_ntriples(@realname)}\".\n"
      #rdf << " <foaf:name>#{@realname}</foaf:name>\n"
    end
    
    rdf << "<#{uri}> <http://purl.org/ontology/mo/discogs> <http://www.discogs.com/artist/#{ CGI::escape(@raw_name) }>.\n"    
    #rdf << " <mo:discogs rdf:resource=\"http://www.discogs.com/artist/#{ Util.escape_xml( CGI::escape(@raw_name) ) }\"/>\n"
    @urls.each do |url|      
      
      #hack to strip comments after urls in data
      #TODO: comma-sep
      url = url.split(" ")[0]
      url = Util.clean_url(url)
      begin
        
        URI.parse(url)
              
        if ( /twitter\.com\/([a-zA-Z0-9]+)/.match(url) )
          account_name = /twitter\.com\/([a-zA-Z0-9]+)/.match(url)[1]
          rdf << "<#{uri}> <http://xmlns.com/foaf/0.1/holdsAccount> <#{uri}/twitter/account_name>.\n"
          #rdf << " <foaf:holdsAccount>\n"
          rdf << "<#{uri}/twitter/account_name> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/OnlineAccount>.\n"
          rdf << "<#{uri}/twitter/account_name> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://rdfs.org/sioc/ns#User>.\n"
          rdf << "<#{uri}/twitter/account_name> <http://xmlns.com/foaf/0.1/accountName> \"#{account_name}\".\n"
          rdf << "<#{uri}/twitter/account_name> <http://xmlns.com/foaf/0.1/accountServiceHomepage> <http://www.twitter.com>.\n"
          #rdf << "  <foaf:OnlineAccount rdf:about=\"#{uri}/twitter/account_name\">\n"
          #rdf << "    <rdf:type rdf:resource=\"http://rdfs.org/sioc/ns#User\"/>\n"
          #rdf << "    <foaf:accountName>#{account_name}</foaf:accountName>\n"
          #rdf << "    <foaf:accountServiceHomepage rdf:resource=\"http://www.twitter.com\"/>\n"
          #rdf << "  </foaf:OnlineAccount>\n"
          #rdf << " </foaf:holdsAccount>\n"
        else
          rdf << "<#{uri}> <http://xmlns.com/foaf/0.1/isPrimaryTopicOf> <#{url}>.\n"
          #rdf << " <foaf:isPrimaryTopicOf rdf:resource=\"#{ Util.escape_xml(url) }\"/>\n"                
        end
        
        if ( /en\.wikipedia\.org/.match(url) )
          dbpedia_uri = url.sub("en.wikipedia.org/wiki", "dbpedia.org/resource")
          rdf << "<#{uri}> <http://www.w3.org/2002/07/owl#sameAs> <#{dbpedia_uri}>.\n"
          #rdf << " <owl:sameAs rdf:resource=\"#{ Util.escape_xml( dbpedia_uri ) }\"/>\n"  
        end
  
        if ( /wikipedia\.org/.match(url) )
          rdf << "<#{uri}> <http://purl.org/ontology/mo/wikipedia> <#{url}>.\n"
          #rdf << " <mo:wikipedia rdf:resource=\"#{ Util.escape_xml(url) }\"/>\n"  
        end            
        
        if ( /www\.myspace\.com/.match(url) )
          rdf << "<#{uri}> <http://purl.org/ontology/mo/myspace> <#{url}>.\n"
          #rdf << " <mo:myspace rdf:resource=\"#{ Util.escape_xml(url) }\"/>\n"
          
          #TODO using seeAlso rather than sameas as sometimes records have >1 myspace account associated with them  
          dbtune_uri = url.sub("www.myspace.com", "dbtune.org/myspace")
          rdf << "<#{uri}> <http://www.w3.org/2000/01/rdf-schema#seeAlso> <#{dbtune_uri}>.\n"
          #rdf << " <rdfs:seeAlso rdf:resource=\"#{ Util.escape_xml(dbtune_uri) }\"/>\n"
        end
      rescue
        puts "invalid URI: #{url}"
      end            
    end
    
    @groups.each do |group|
      rdf << "<#{uri}> <http://purl.org/ontology/mo/member_of> <#{group}>.\n"      
      #rdf << " <mo:member_of rdf:resource=\"#{ Util.escape_xml(group) }\"/>\n"
    end
        
    @images.each do |image|
      rdf << "<#{uri}> <http://xmlns.com/foaf/0.1/depiction> <#{image["uri"]}>.\n"
      #rdf << " <foaf:depiction>\n"      
      rdf << dump_image(image, "Photo of #{Util.escape_ntriples(@raw_name)}", uri)
      #rdf << " </foaf:depiction>\n"  
    end
        
    if @profile != nil
      rdf << "<#{uri}> <http://purl.org/dc/terms/description> \"#{Util.escape_ntriples(@profile)}\".\n"
      #rdf << " <dc:description>#{@profile}</dc:description>\n"  
    end    
        
    #rdf << "</#{rdf_type()}>\n"
    return rdf
      
  end

  def rdf_type()
    if @root.find("members").length() == 0
      return "<http://purl.org/ontology/mo/MusicArtist>"
    end
    return "<http://purl.org/ontology/mo/MusicGroup>"
  end
  
  def Artist.create_uri(name)
    slug = Util.slug(name)
    return Util.canonicalize("/artist/#{ CGI.escape(slug) }")
  end
      
end