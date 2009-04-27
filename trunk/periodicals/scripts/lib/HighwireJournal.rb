require 'Util'

class HighwireJournal
  
  attr_reader :fields
  
  def initialize(fields)
    @fields = fields
  end
  
  def id()
    tester = Regexp.new("http://([a-z0-9\-]+)\.([a-z\-]+)\.([a-z\-]+)")
    matchdata = tester.match( fields["homepage"] ) 
    if matchdata != nil
      if matchdata[1] == "www"
        return matchdata[2]
      end
      return "#{matchdata[1]}-#{matchdata[2]}"      
    end
    #fallback
    return fields["ISSN"]
  end
  
  def uri()
    slug = id()
    return "http://periodicals.dataincubator.org/journal/#{slug}"
  end 
    
  def to_rdf(stream)
    rdf = "<bibo:Journal rdf:about=\"#{uri()}\">\n"
    issn = false
    eissn = false
    rdf << " <dc:title>#{ Util.escape_xml( fields["title"] ) }</dc:title>\n"
        
    if fields["ISSN"] != nil && fields["ISSN"] != "Unknown"
      issn = true 
      rdf << " <bibo:issn>#{fields["ISSN"]}</bibo:issn>\n"
      rdf << " <owl:sameAs rdf:resource=\"http://periodicals.dataincubator.org/issn/#{fields["ISSN"]}\" />\n"
    end

    if fields["EISSN"] != nil  && fields["EISSN"] != "Unknown"
      eissn = true 
      rdf << " <bibo:eissn>#{fields["EISSN"]}</bibo:eissn>\n"
      rdf << " <owl:sameAs rdf:resource=\"http://periodicals.dataincubator.org/eissn/#{fields["EISSN"]}\" />\n"
    end

    if fields["homepage"] != nil 
      rdf << " <foaf:homepage rdf:resource=\"#{fields["homepage"]}\"/>\n"
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
        
    stream.write(rdf)
  end
  
end