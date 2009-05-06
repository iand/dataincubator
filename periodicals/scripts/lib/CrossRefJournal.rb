require 'Util'

class CrossRefJournal
  
  attr_reader :fields
  
  def initialize(fields)
    @fields = fields
  end
  
  def uri()
    slug = Util.makeSlug(fields["title"])
    return "http://periodicals.dataincubator.org/journal/#{slug}"
  end 
        
  def publisher_uri()
    slug = Util.makeSlug(fields["publisher"])
    return "http://periodicals.dataincubator.org/organization/#{slug}"
  end 
        
  def to_rdf(stream)
    rdf = "<bibo:Journal rdf:about=\"#{uri()}\">\n"
    issn = false
    eissn = false
    doi = false
    publisher = false
    rdf << " <dc:title>#{ Util.escape_xml( fields["title"] ) }</dc:title>\n"
        
    if fields["publisher"] != nil && fields["publisher"] != "Unknown" && fields["publisher"] != ""
      publisher = true      
      rdf << " <dc:publisher rdf:resource=\"#{ publisher_uri() }\"/>\n"
    end

    if fields["ISSN"] != nil && fields["ISSN"] != "Unknown" && fields["ISSN"] != ""
      issn = true 
      rdf << " <bibo:issn>#{fields["ISSN"]}</bibo:issn>\n"
      rdf << " <owl:sameAs rdf:resource=\"http://periodicals.dataincubator.org/issn/#{fields["ISSN"]}\" />\n"
    end

    if fields["EISSN"] != nil  && fields["EISSN"] != "Unknown" && fields["EISSN"] != ""
      eissn = true 
      rdf << " <bibo:eissn>#{fields["EISSN"]}</bibo:eissn>\n"
      rdf << " <owl:sameAs rdf:resource=\"http://periodicals.dataincubator.org/eissn/#{fields["EISSN"]}\" />\n"
    end

    if fields["doi"] != nil && fields["doi"] != "Unknown" && fields["doi"] != ""
      doi = true
      rdf << " <bibo:doi>#{ Util.escape_xml( fields["doi"] ) }</bibo:doi>\n"
      rdf << " <foaf:homepage rdf:resource=\"http://dx.doi.org/#{ Util.escape_uri( fields["doi"] ) }\"/>"
    end
         
    rdf << "</bibo:Journal>\n"
    
    if publisher
      rdf << "<foaf:Organization rdf:about=\"#{ publisher_uri() }\">\n"
      rdf << "  <foaf:name>#{ Util.escape_xml( fields["publisher"] ) }</foaf:name>\n";
      # rights holder of the journal
      rdf << "  <dc:rightsHolder rdf:resource=\"#{ uri() }\" />\n"
      rdf << "</foaf:Organization>\n"
      rdf << "<foaf:Group rdf:about=\"http://periodicals.dataincubator.org/groups/crossref-publishers\">\n"
      rdf << "  <foaf:name>CrossRef</foaf:name>\n"
      rdf << "  <foaf:homepage rdf:resource=\"http://crossref.org\"/>\n"
      # is member of crossref
      rdf << "  <foaf:member rdf:resource=\"#{ publisher_uri() }\" />\n"
      rdf << "</foaf:Group>\n"
    end
    
    if issn
      rdf << "<rdf:Description rdf:about=\"http://periodicals.dataincubator.org/issn/#{fields["ISSN"]}\">\n"
      rdf << " <owl:sameAs rdf:resource=\"#{uri()}\" />\n"
      rdf << "</rdf:Description>\n"
    end

    if eissn
      rdf << "<rdf:Description rdf:about=\"http://periodicals.dataincubator.org/eissn/#{fields["EISSN"]}\">\n"
      rdf << " <owl:sameAs rdf:resource=\"#{uri()}\" />\n"
      rdf << "</rdf:Description>\n"
    end
        
    if doi
      rdf << "<rdf:Description rdf:about=\"http://periodicals.dataincubator.org/doi/#{ Util.escape_uri( fields["doi"] ) }\">\n"
      rdf << " <owl:sameAs rdf:resource=\"#{uri()}\" />\n"
      rdf << "</rdf:Description>\n"
    end
        
    stream.write(rdf)
  end
  
end