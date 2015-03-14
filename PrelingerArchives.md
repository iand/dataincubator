# Introduction #

The prelinger archive consists of thousands of digitalized industrial, educational, travel, propaganda and other short films from 1903 to the 1970s. More information available on  [wikipedia](http://en.wikipedia.org/wiki/Prelinger_Archives).

Just over 2000 films are now available as a collection from the [Internet Archive](http://www.archive.org/details/prelinger).

All of the films are in the Public Domain under a CC0 license.

# Metadata #

The collection can be [browsed in the Internet Archive](http://www.archive.org/search.php?query=(collection%3Aprelinger%20OR%20mediatype%3Aprelinger)%20AND%20-mediatype%3Acollection&sort=-avg_rating%3B-num_reviews) at this URL.

The [advanced search](http://www.archive.org/advancedsearch.php?q=(collection:prelinger%20OR%20mediatype:prelinger)%20AND%20-mediatype:collection) page provides access to forms that allow the retrieval of the core metadata as XML, JSON or CSV. The form includes options for retrieving just the id or any collection of fields. The complete set of results can be retrieved by adjusting the number of results (the archive currently holds just over 2000 records).

This data could be used to convert the collection metadata into RDF, minting URIs for each movie.

Each movie currently has a simple mixed-case key that is used to identify it on the website, e.g. "tomorrow\_television"

This can be used to link to the movie, e.g:

http://www.archive.org/details/tomorrow_television

The detail page for each movie also has an "All Files" link that also uses the movie identifier, e.g.:

http://ia300228.us.archive.org/0/items/tomorrow_television

This is a directory that contains the movie files, thumbnails and some XML files that also contain the core movie metadata (presumably the same as through the search interface). The reviews of the movie can also be accessed from this location too.

(note those urls seem to be machine specific, so its probably not suitable to use them in the generated metadata)

# Modelling #

  * The basic metadata such as title, description, etc could be captured as Dublin Core
  * The work can be associated with its different versions using dc terms and/or FRBR data
  * The thumbnails can be associated with the work using depiction/thumbnail
  * Reviews could be captured using the review ontology and FOAF data
  * It might be possible to capture the subject classifications using SKOS

# Other Notes #

There is possibly a wide range of other media information that could be extracted from the Internet Archive in this way. The Prelinger Archive is a good starting point as it is explicitly Public Domain
