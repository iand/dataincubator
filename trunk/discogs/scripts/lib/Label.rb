require 'rexml/document'
require 'uri'
require 'cgi'
require 'Util'
require 'NamedDiscogResource'

class Label < NamedDiscogResource

  def initialize(string)
    
    super(string)
        
    #TODO parse out the markup
    #[l=Seasons Recordings]
    #[url=http://www.usatt.org/rseguine/FAX/fax_facts/interview/peter_namlook_interview.htm]here[/url]
    #[b]Phone:[/b] +1 (773) 862-0073
    #[b]Founder &amp; Owner:[/b] [a=Jeff Craven]
    #[a=DJ Buck]
    #[i]Theories and subjects of substances is the elementary element that fuels the minds within our Axis.[/i]
    # [r=27120]
    #[b][l=Rising High Records][/b]
    #[u]Partisan Recordings[/u]
    #@profile = get_optional_tag("profile")
    profile = @root.get_elements("profile")[0]
    if profile != nil
      @profile = profile.get_text  
    end
    
    
    contact = @root.get_elements("contactinfo")[0]
    if contact != nil && contact.text != nil
      #FIXME losing \n in addresses, temporarily fixed with space
      @address = Util.clean_escape(contact.text)
    end
    
    @parent = get_optional_tag("parentLabel", false)
    
  end
    
  def dump_rdf()    
    uri = Util.escape_xml( Label.create_uri( @raw_name ) )
    rdf = "<mo:Label rdf:about=\"#{ uri  }\">\n"
    rdf << " <foaf:name>#{@name}</foaf:name>\n"
    rdf << " <mo:discogs rdf:resource=\"http://www.discogs.com/label/#{ Util.escape_xml( CGI::escape(@raw_name) ) }\"/>\n"
    @urls.each do |url|
      #hack to strip comments after urls in data
      #TODO: comma-sep
      url = url.split(" ")[0]
      url = Util.clean_url(url)      
      begin
        URI.parse(url)
        rdf << " <foaf:isPrimaryTopicOf rdf:resource=\"#{ Util.escape_xml(url) }\"/>\n"
      rescue
        puts "Invalid uri #{url}"  
      end
      
    end
    
    @images.each do |image|
      rdf << " <foaf:logo>"
      rdf << dump_image(image, "Logo for #{Util.escape_xml( @raw_name )}")
      rdf << " </foaf:logo>"  
    end
    
    if @profile != nil
      rdf << " <dc:description>#{@profile}</dc:description>\n"  
    end    
    if @address != nil
      rdf << " <discogs:contactInformation>#{@address}</discogs:contactInformation>\n"
    end
    
    if @parent != nil
      #clean_parent_name = Util.clean_escape(@parent)
      parent_uri = Util.escape_xml( Label.create_uri( @parent ) )
      rdf << " <dc:isPartOf>\n"
      rdf << "  <mo:Label rdf:about=\"#{ parent_uri }\"/>\n"
      rdf << " </dc:isPartOf>\n"
    end
    rdf << "</mo:Label>\n"
    return rdf
              
  end  
  
  def Label.create_uri(name)
    slug = Util.slug(name)
    return Util.canonicalize("/label/#{ CGI::escape(slug) }")
  end
  
end