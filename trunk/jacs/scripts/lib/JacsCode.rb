require 'Util'

class JacsCode

  attr_reader :fields
  
  def initialize(fields)
    @fields = fields
  end

  def uri()
    code = @fields["code"]
    return "http://jacs.dataincubator.org/" + Util.makeSlug(code)
  end

  def hierarchical_uri()
    code = String.new(@fields["code"])
    
    if code.length == 1
      # top level
      slug = Util.makeSlug(code)
    else
      path = ""
      unless code[3].chr == "0"
        path = "/#{code}" + path
        code[3] = "0"
      end
      unless code[2].chr == "0"
        path = "/#{code}" + path
        code[2] = "0"
      end
      unless code[1].chr == "0"
        path = "/#{code}" + path
        code[1] = "0"
      end
      
      path = "#{code[0].chr}#{path}"
      
      slug = Util.makeSlug(path)
    end 

    return "http://jacs.dataincubator.org/#{slug}"
  end 

  def get_parent_uri(structured_uri, nested)
    parent_uri = nil
    uris = structured_uri.split("/");
    if uris.length > 4
      uris.pop
      if( nested == true)
        parent_uri = uris.join("/")
      else
        parent_code = uris.pop
        parent_uri = "http://jacs.dataincubator.org/" + parent_code
      end
    end

   return parent_uri

  end

  def to_rdf(stream)
    
    
    # Alter these three lines to change the uri structure
    # if you want flat structure (http://jacs.dataincubator.org/a110) do:
    #   concept_uri = uri();
    #   structured_uri = hierarchical_uri()
    #   parent_uri = get_parent_uri(structured_uri, false)
    #
    # if you want hierarchical/path based uri structure (http://jacs.dataincubator.org/a/a100/a110) do
    #   
    #   concept_uri = hierarchical_uri()
    #   parent_uri = get_parent_uri(concept_uri, true)
        
    concept_uri = uri();
    structured_uri = hierarchical_uri()    
    parent_uri = get_parent_uri(structured_uri, false)

    #concept_uri = hierarchical_uri()
    #parent_uri = get_parent_uri(concept_uri, true)
    
        
    print "* Processing #{concept_uri} \n"
    rdf = "<skos:Concept rdf:about=\"#{concept_uri}\">\n"
    
    
    subject = @fields["subject"]
    jacscode = @fields["code"]
    
    
    rdf << " <skos:prefLabel>#{ Util.escape_xml( subject.strip ) }</skos:prefLabel>\n"
    rdf << " <skos:inScheme rdf:resource=\"http://jacs.dataincubator.org/\" />\n"
    rdf << " <dct:identifier>#{jacscode}</dct:identifier>\n"
    
    
    
    if @fields["description"] != nil && @fields["description"] != ""
      description = @fields["description"]
      rdf << " <skos:scopeNote>#{ Util.escape_xml( description.strip ) }</skos:scopeNote>\n"
    end
    
    if parent_uri != nil
      rdf << " <skos:broader rdf:resource=\"#{parent_uri}\" />\n"
    end
    
    rdf << "</skos:Concept>\n"

    if parent_uri != nil    
      rdf << "<skos:Concept rdf:about=\"#{parent_uri}\">\n"
      rdf << " <skos:narrower rdf:resource=\"#{concept_uri}\" />\n"    
      rdf << "</skos:Concept>\n"
    else
      rdf << "<skos:ConceptScheme rdf:about=\"http://jacs.dataincubator.org/\">\n"
      rdf << " <skos:hasTopConcept rdf:resource=\"#{concept_uri}\" />\n"          
      rdf << "</skos:ConceptScheme>\n"
    end
    
    
    stream.write(rdf)
  end
  

end