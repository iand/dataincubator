module Util
  
  def Util.rdf_root
    return "<rdf:RDF     
    xmlns:dc=\"http://purl.org/dc/terms/\"\n\
    xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n\
    xmlns:foaf=\"http://xmlns.com/foaf/0.1/\"\n\
    xmlns:owl=\"http://www.w3.org/2002/07/owl#\"\n\
    xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n\
    xmlns:xsd=\"http://www.w3.org/2001/XMLSchema#\"\n\
    xmlns:void=\"http://rdfs.org/ns/void#\"\n\
    xmlns:bibo=\"http://purl.org/ontology/bibo/\">\n\n"  
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
    
    escaped.gsub!(" ", "%20")
    escaped.gsub!("&", "&amp;")
            
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
    removelist = ["a", "an", "as", "at", "before", "but", "by", "for","from","is", "in", "into", "like", "of", "off", "on", "onto","per","since", "than", "the", "this", "that", "to", "up", "via","with"];
    removelist.each do |word|
       slug = slug.gsub(" #{ word } ",' ')
    end
    return slug.gsub("&","and").gsub(/[\s]/,'-').gsub(/[^A-Za-z\d-]/,'').gsub("--","-")
  end

  def Util.lookupSubjectHeading(subject_heading)
    require 'net/http'
    require 'uri'

    location = "/authorities/label/" << subject_heading    
    response = nil
    Net::HTTP.start('id.loc.gov', 80) {|http|
      response = http.head(location)
    }
                
    if response.instance_of? Net::HTTPFound
      location_uri = response['Location']
      print "     -> found location: #{location_uri} \n"
      return location_uri
    end
    
    return false
  end
end