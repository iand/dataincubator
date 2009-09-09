class DiscogResource
  
  def initialize(string)
    
    doc = REXML::Document.new(string)
    @root = doc.root
    
    @images = Array.new
    images = @root.get_elements("images")[0]
    if images != nil
      images.get_elements("image").each do |image|
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
    tag = @root.get_elements(tagname)[0]
    if tag != nil && tag.text != nil
      if clean
        return Util.clean_escape( tag.text )
      else
        return tag.text  
      end        
    end    
    return nil
    
  end  
  
  def dump_image(image, label=nil, depicts=nil)
    rdf = ""
    rdf << "<foaf:Image rdf:about=\"#{image["uri"]}\">\n"
    rdf << " <exif:height>#{image["height"]}</exif:height>\n"
    rdf << " <exif:width>#{image["width"]}</exif:width>\n"
    if label != nil
      rdf << "<rdfs:label>#{label}</rdfs:label>\n"
    end
    if depicts != nil
      rdf << "<foaf:depicts rdf:resource=\"#{depicts}\"/>\n"
    end
    rdf << "<foaf:thumbnail rdf:resource=\"#{image["uri150"]}\"/>\n"
    rdf << "</foaf:Image>\n"
    return rdf
  end
  
end