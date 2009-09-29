module Util
  
  def Util.rdf_root
    return "<rdf:RDF     
    xmlns:dc=\"http://purl.org/dc/elements/1.1/\"\n\
    xmlns:dct=\"http://purl.org/dc/terms/\"\n\
    xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n\
    xmlns:foaf=\"http://xmlns.com/foaf/0.1/\"\n\
    xmlns:owl=\"http://www.w3.org/2002/07/owl#\"\n\
    xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n\
    xmlns:xsd=\"http://www.w3.org/2001/XMLSchema#\"\n\
    xmlns:void=\"http://rdfs.org/ns/void#\"\n\
    xmlns:skos=\"http://www.w3.org/2004/02/skos/core#\"\n\
    xmlns:bibo=\"http://purl.org/ontology/bibo/\">\n\n"  
  end
  
  
  def Util.skos_taxonomy_scheme
     return "\n<skos:ConceptScheme rdf:about=\"http://jacs.dataincubator.org/\">\n\
       <dc:title xml:lang=\"en\">Joint Academic Coding System</dc:title>
     </skos:ConceptScheme>\n\n"
  end
  
  def Util.rdf_end
    return "\n\n</rdf:RDF>"  
  end 
  
  def Util.escape_xml(s)
    escaped = s.dup
    
    escaped.gsub!("&", "&amp;")
    escaped.gsub!("<", "&lt;")
    escaped.gsub!(">", "&gt;")
            
    return escaped
    
  end

  def Util.escape_uri(s)
    escaped = s.dup
    
    escaped.gsub!(/\s/, "%20")
    escaped.gsub!(/\&/, "&amp;")
            
    return escaped
    
  end


  #Util code for cleaning up whitespace, newlines, etc
  def Util.clean_ws(s)
    cleaned = s.gsub /^\r\n/, ""
    cleaned.gsub! /\n/, ""    
    cleaned.gsub! /\s{2,}/, " "
    cleaned.gsub! /^\s/, ""
    if cleaned == "" or cleaned == " "
      return nil
    end
    return cleaned
  end
  
  
  def Util.makeSlug(s) 
    slug = s.downcase.strip
    return slug
  end
  
end