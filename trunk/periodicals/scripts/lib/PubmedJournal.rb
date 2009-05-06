require "Util"

class PubmedJournal
  
  attr_reader :fields
  
  def initialize(fields)
    @fields = fields
  end
  
  def uri()
    slug = Util.makeSlug(fields["JournalTitle"])
    return "http://periodicals.dataincubator.org/journal/#{slug}"
  end 

  def to_rdf(stream)
    rdf = "<bibo:Journal rdf:about=\"#{uri()}\">\n"
    rdf << " <dc:title>#{Util.escape_xml( fields["JournalTitle"] )}</dc:title>\n"
    
    rdf << "<dc:identifier rdf:resource=\"info:pmid/#{fields["NlmId"]}\"/>\n"
    
    rdf << "<foaf:isPrimaryTopicOf rdf:resource=\"http://www.ncbi.nlm.nih.gov/sites/entrez?Db=nlmcatalog&amp;doptcmdl=Expanded&amp;cmd=search&amp;Term=#{fields["NlmId"]}%5BNlmId%5D\"/>\n"
    rdf << "<foaf:isPrimaryTopicOf rdf:resource=\"http://locatorplus.gov/cgi-bin/Pwebrecon.cgi?DB=local&amp;v1=1&amp;ti=1,1&amp;Search_Arg=#{fields["NlmId"]}&amp;Search_Code=0359&amp;CNT=20&amp;SID=1\"/>\n"

    issn = false    
    if fields["ISSN"] != nil
      issn = true
      rdf << " <bibo:issn>#{fields["ISSN"]}</bibo:issn>\n"
      rdf << " <owl:sameAs rdf:resource=\"http://periodicals.dataincubator.org/issn/#{fields["ISSN"]}\" />\n"
    end

    eissn = false
    if fields["ESSN"] != nil
      eissn = true 
      rdf << " <bibo:eissn>#{fields["ESSN"]}</bibo:eissn>\n"
      rdf << " <owl:sameAs rdf:resource=\"http://periodicals.dataincubator.org/eissn/#{fields["ESSN"]}\" />\n"
    end

            
    if fields["MedAbbr"] != nil
      rdf << " <bibo:shortTitle>#{Util.escape_xml( fields["MedAbbr"] )}</bibo:shortTitle>\n"  
    end

    if fields["IsoAbbr"] != nil
      rdf << " <bibo:shortTitle>#{Util.escape_xml( fields["IsoAbbr"] )}</bibo:shortTitle>\n"  
    end
         
    rdf << "</bibo:Journal>\n"
    
    if issn
      rdf << "<rdf:Description rdf:about=\"http://periodicals.dataincubator.org/issn/#{fields["ISSN"]}\">\n"
      rdf << " <owl:sameAs rdf:resource=\"#{uri()}\" />\n"
      rdf << "</rdf:Description>\n"
    end

    if eissn
      rdf << "<rdf:Description rdf:about=\"http://periodicals.dataincubator.org/eissn/#{fields["ESSN"]}\">\n"
      rdf << " <owl:sameAs rdf:resource=\"#{uri()}\" />\n"
      rdf << "</rdf:Description>\n"
    end
    
    stream.write(rdf)    
  end
  
end