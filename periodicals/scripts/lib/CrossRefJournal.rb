require 'Util'

class CrossRefJournal
  
  attr_reader :fields
  
  def initialize(fields)
    @fields = fields
  end
  
  def id()
    id = fields["title"].clone
    id.gsub!(/[^\w\d]/,'')
    if (id == nil)
      return fields["ISSN"]  
    end
    id.gsub!(/[^A-z0-9]/,'')
    return id.downcase
  end

  def uri()
    slug = id()
    return "http://periodicals.dataincubator.org/journal/#{slug}"
  end 
    
  def to_rdf(stream)
    rdf = "<bibo:Journal rdf:about=\"#{uri()}\">\n"
    issn = false
    eissn = false
    doi = false
    rdf << " <dc:title>#{ Util.escape_xml( fields["title"] ) }</dc:title>\n"
    rdf << " <dc:partOf rdf:resource=\"http://periodicals.dataincubator.org/datasets/crossref\" />\n"
        
    if fields["publisher"] != nil && fields["publisher"] != "Unknown" && fields["publisher"] != ""
      rdf << " <dc:publisher>#{ Util.escape_xml( fields["publisher"] ) }</dc:publisher>\n"
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
      rdf << " <bibo:uri rdf:resource=\"http://dx.doi.org/#{ Util.escape_uri( fields["doi"] ) }\"/>"
    end
         
    rdf << "</bibo:Journal>\n"
    
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