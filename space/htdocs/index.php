<?php
define('STORE_URI', 'http://api.talis.com/stores/space');
define('LIB_DIR', dirname(dirname(dirname(dirname(__FILE__)))) . '/lib/');
define('PAGET_DIR', LIB_DIR . 'paget' . DIRECTORY_SEPARATOR);
define('MORIARTY_DIR', LIB_DIR . 'moriarty' . DIRECTORY_SEPARATOR);
define('MORIARTY_ARC_DIR', LIB_DIR . 'arc_2008_08_04' . DIRECTORY_SEPARATOR);

if (!defined('MORIARTY_HTTP_CACHE_DIR')  && file_exists(dirname(__FILE__).DIRECTORY_SEPARATOR.'cache')) {
  define('MORIARTY_HTTP_CACHE_DIR', dirname(__FILE__).DIRECTORY_SEPARATOR.'cache');
}
define('MORIARTY_HTTP_CACHE_READ_ONLY', TRUE);
define('MORIARTY_HTTP_CACHE_USE_STALE_ON_FAILURE', TRUE ); // use a cached response if network fails

require_once PAGET_DIR . 'paget_urispace.class.php';
require_once PAGET_DIR . 'paget_simplepropertylabeller.class.php';
require_once PAGET_DIR . 'paget_storedescribegenerator.class.php';



class TopicSpaceUriSpace extends PAGET_UriSpace {
  function get_description($uri) {
      
    if ( $uri == 'http://' . $_SERVER['HTTP_HOST'] . '/space/spacecraft.html' ) {
      $desc = new SpacecraftListResourceDescription($uri, 'http://api.talis.com/stores/space'); 
      $desc->set_namespace_mapping('space', 'http://purl.org/net/schemas/space/');
      return $desc;
    }
    else if ( preg_match('~^http://' . $_SERVER['HTTP_HOST'] . '/space/(.+)$~', $uri, $m) ) {
      $desc = new StoreBackedResourceDescription('http://purl.org/net/schemas/space/' . $m[1], 'http://api.talis.com/stores/space'); 
      $desc->set_namespace_mapping('space', 'http://purl.org/net/schemas/space/');
      return $desc;
    }
  } 
}

class StoreBackedResourceDescription extends PAGET_ResourceDescription {   
  private $_store_uri;

  function __construct($uri, $store_uri) {
    $this->_store_uri = $store_uri;
    parent::__construct($uri);  
  }
  function get_generators() {
    return array( new PAGET_StoreDescribeGenerator($this->_store_uri) );
  }
  
  function get_html() {
    $config = array();
    $config['rights_text'] = 'All text and data in this document are in the Public Domain.';
    $config['credits_html'] = 'Built with <a href="http://code.google.com/p/paget/">paget</a>.';
   
    $repr = new PAGET_SimpleHtmlRepresentation($config);
    $repr->emit($this);
  }
  
  function map_uri($uri) {
    if ( preg_match('~^http://purl.org/net/schemas/space/(.+)$~', $uri, $m) ) {
      return 'http://' . $_SERVER['HTTP_HOST'] . '/' . $m[1];
    }
    
    return $uri;
  }
  
}

class SpacecraftListResourceDescription extends PAGET_ResourceDescription {   
  private $_store_uri;

  function __construct($uri, $store_uri) {
    $this->_store_uri = $store_uri;
    parent::__construct($uri);  
  }
  function get_generators() {
    return array( new SpacecraftListGenerator($this->_store_uri) );
  }
  
  function get_html() {
    $config = array();
    $config['rights_text'] = 'All text and data in this document are in the Public Domain.';
    $config['credits_html'] = 'Built with <a href="http://code.google.com/p/paget/">paget</a>.';
   
    $repr = new PAGET_SimpleHtmlRepresentation($config);
    $repr->emit($this);
  }
  
  function map_uri($uri) {
    if ( preg_match('~^http://purl.org/net/schemas/space/(.+)$~', $uri, $m) ) {
      return 'http://' . $_SERVER['HTTP_HOST'] . '/' . $m[1];
    }
    
    return $uri;
  }
  
}


class SpacecraftListGenerator {
  var $_store_uri;
  var $_query = 'prefix space: <http://purl.org/net/schemas/space/>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix foaf: <http://xmlns.com/foaf/0.1/>
construct {
?s foaf:name ?name .
}

where {
 ?s a space:Spacecraft ; foaf:name ?name.
}
limit 30
';

  function __construct($store_uri) {
    $this->_store_uri = $store_uri;
  }
  
  function add_triples($resource_uri, &$desc) {
    $store = new Store($this->_store_uri);
    $s = $store->get_sparql_service();
    $response = $s->graph($this->_query);
    if ($response->is_success()) {
      $desc->add_rdfxml($response->body);
    }
  }

}

$space = new TopicSpaceUriSpace();
$space->dispatch();

?>
