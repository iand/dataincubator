require "libxml"

class DiscogResource
  
  attr_reader :images
  
  def initialize(string)
    
    parser = LibXML::XML::Parser.string(string)
    doc = parser.parse
    @root = doc.root
    
    @images = Array.new
    images = @root.find_first("images")
    if images != nil
      images.find("image").each do |image|
         @images << image.attributes 
      end      
    end
    
  end
  
  def to_rdf(root=true)
    rdf = ""
    if root
      rdf << Util.rdf_root
    end

    rdf << dump_rdf()
    
    if root
      rdf << Util.rdf_end
    end
    return rdf
              
  end  
      
  def get_optional_tag(tagname, clean=true)
    tag = @root.find_first(tagname)
    if tag != nil && tag.first.content != nil
      if clean
        return Util.clean_escape( tag.first.content )
      else
        return tag.first.content
      end        
    end    
    return nil
    
  end  
  
  def dump_image(image, label=nil, depicts=nil)
    rdf = ""
    uri = "<#{image["uri"]}>"
    rdf << "#{uri} <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Image>.\n"
    #rdf << "<foaf:Image rdf:about=\"#{image["uri"]}\">\n"
    rdf << "#{uri} <http://www.w3.org/2003/12/exif/ns#height> \"#{image["height"]}\".\n"
    #rdf << " <exif:height>#{image["height"]}</exif:height>\n"
    #rdf << ""
    rdf << "#{uri} <http://www.w3.org/2003/12/exif/ns#width> \"#{image["width"]}\".\n"
    #rdf << " <exif:width>#{image["width"]}</exif:width>\n"
    if label != nil
      rdf << "#{uri} <http://www.w3.org/2000/01/rdf-schema#label> \"#{label}\".\n"
      #rdf << "<rdfs:label>#{label}</rdfs:label>\n"
    end
    if depicts != nil
      rdf << "#{uri} <http://xmlns.com/foaf/0.1/depicts> <#{depicts}>.\n"
      #rdf << "<foaf:depicts rdf:resource=\"#{depicts}\"/>\n"
    end
    rdf << "#{uri} <http://xmlns.com/foaf/0.1/thumbnail> <#{image["uri150"]}>.\n"
    #rdf << "<foaf:thumbnail rdf:resource=\"#{image["uri150"]}\"/>\n"
    #rdf << "</foaf:Image>\n"
    return rdf    
  end
  
end