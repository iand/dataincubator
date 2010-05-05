module Util
      
  def Util.rdf_root
    return "<rdf:RDF     
    xmlns:dc=\"http://purl.org/dc/terms/\"\n\
    xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n\
    xmlns:foaf=\"http://xmlns.com/foaf/0.1/\"\n\
    xmlns:sioc=\"http://rdfs.org/sioc/ns#\"\n\
    xmlns:owl=\"http://www.w3.org/2002/07/owl#\"\n\
    xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n\
    xmlns:xsd=\"http://www.w3.org/2001/XMLSchema#\"\n\    
    xmlns:exif=\"http://www.w3.org/2003/12/exif/ns#\"\n\        
    xmlns:discogs=\"http://purl.org/net/schemas/discogs/\"\n\
    xmlns:skos=\"http://www.w3.org/2008/05/skos#\"\n\
    xmlns:time=\"http://purl.org/NET/c4dm/timeline.owl#\"\n\        
    xmlns:mo=\"http://purl.org/ontology/mo/\">\n\n"  
  end
  
  def Util.rdf_end
    return "\n\n</rdf:RDF>"  
  end 
 
  def Util.escape_ntriples(s)
    escaped = s.dup
    escaped.gsub!(/["]/, "\\\\\"")
    escaped.gsub!("\n", " ")
    escaped.gsub!("\r", " ")
    escaped.gsub!("\\", "\\\\")
    return escaped
  end
    
#  def Util.escape_xml(s)
#    escaped = s.dup    
#    escaped.gsub!("&", "&amp;")
#    escaped.gsub!("<", "&lt;")
#    escaped.gsub!(">", "&gt;")
#            
#    return escaped    
#  end
  
  #Util code for cleaning up whitespace, newlines, etc
  def Util.clean_ws(s)
    cleaned = s.gsub(/^\r\n/, "")
    cleaned.gsub!(/\n/, " ")    
    cleaned.gsub!(/\s{2,}/, " ")
    cleaned.gsub!(/^\s/, "")
    
    illegal = /\x00|\x01|\x02|\x03|\x04|\x05|\x06|\x07|\x08|\x0B|
    \x0C|\x0E|\x0F|\x10|\x11|\x12|\x13|\x14|\x15|\x16|\x17|\x18|\x19|\x1A|
    \x1B|\x1C|\x1D|\x1E|\x1F/
    
    cleaned.gsub!(illegal, " ")    
    if cleaned == "" or cleaned == " "
      return nil
    end
    return cleaned
  end  
  
  def Util.slug(s)
    normalized = s.downcase
    if normalized.end_with?(", the")
       normalized = normalized.gsub(", the", "")
       normalized = "the-" + normalized  
    end
    
    normalized.gsub!(/\s+/, "-")
    normalized.gsub!(/\(|\)/, "")

    normalized.gsub!(/%/, "")        
    normalized.gsub!(/,/, "")
    normalized.gsub! /\./, ""              
    normalized.gsub! /&/, "and"    
    normalized.gsub! /\?/, ""
    normalized.gsub! /\=/, ""
    normalized.gsub! /\[/, ""
    normalized.gsub! /\{/, ""
    normalized.gsub! /\]/, ""
    normalized.gsub! /\}/, ""
    normalized.gsub! /"/, ""    
    normalized.gsub! /'/, ""
    normalized.gsub! /|/, ""
    normalized.gsub! /!/, ""
    normalized.gsub! /:/, ""
    
    return normalized    
  end
   

  def Util.escape_xml(s)
    if s == nil
      return s
    end
    
    escaped = s.dup
    
    escaped.gsub!("&", "&amp;")
    escaped.gsub!("<", "&lt;")
    escaped.gsub!(">", "&gt;")
            
    return escaped
    
  end

  def Util.clean_url(url)
     if /http\:www/.match(url)
       url = url.gsub("http:www", "http://www")
     end
     if /http\:\/www/.match(url)
       url = url.gsub("http:/www", "http://www")
     end     
     if url.end_with?(",")
       url = url.gsub(",", "")
     end
     url = url.strip
     return url    
  end
  
  def Util.clean_escape(s)
    return escape_xml( clean_ws(s) ) 
  end  
    
  def Util.canonicalize(path)
    if path.start_with?("http")
      return path
    end  
    return "http://discogs.dataincubator.org#{path}"
  end
      
end