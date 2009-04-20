<?php
ob_start("ob_gzhandler"); 
define('LIB_DIR', dirname(dirname(dirname(dirname(__FILE__)))) . '/lib/');
define('PAGET_DIR', LIB_DIR . 'paget' . DIRECTORY_SEPARATOR);
define('MORIARTY_DIR', LIB_DIR . 'moriarty' . DIRECTORY_SEPARATOR);
define('MORIARTY_ARC_DIR', LIB_DIR . 'arc_2008_08_04' . DIRECTORY_SEPARATOR);

if (!defined('MORIARTY_HTTP_CACHE_DIR')  && file_exists(dirname(dirname(__FILE__)).DIRECTORY_SEPARATOR.'cache')) {
  define('MORIARTY_HTTP_CACHE_DIR', dirname(dirname(__FILE__)).DIRECTORY_SEPARATOR.'cache');
}
define('MORIARTY_HTTP_CACHE_READ_ONLY', TRUE);
define('MORIARTY_HTTP_CACHE_USE_STALE_ON_FAILURE', TRUE ); // use a cached response if network fails



require_once PAGET_DIR . 'paget_urispace.class.php';
require_once PAGET_DIR . 'paget_simplepropertylabeller.class.php';
require_once PAGET_DIR . 'paget_storedescribegenerator.class.php';



class StoreBackedUriSpace extends PAGET_UriSpace {
  function get_description($uri) {
    $desc = new StoreBackedResourceDescription($uri, 'http://api.talis.com/stores/openlibrary'); 
    $desc->set_namespace_mapping('bibo', 'http://purl.org/ontology/bibo/');
    $desc->set_namespace_mapping('bio', 'http://vocab.org/bio/0.1/');
    $desc->set_namespace_mapping('ol', 'http://olrdf.appspot.com/key/');
    $desc->set_namespace_mapping('ov', 'http://open.vocab.org/terms/');
    return $desc;
  } 
  
  function get_template($request) {
    return dirname(dirname(dirname(__FILE__))) . "/lib/paget-template.html";
  } 
    
  
}

class StoreBackedResourceDescription extends PAGET_ResourceDescription {   
  var $_store_uri;
  
  function __construct($uri, $store_uri) {
    $this->_store_uri = $store_uri; 
    parent::__construct($uri);
  }

  function get_generators() {
    return array( new PAGET_StoreDescribeGenerator($this->_store_uri, 'scbd') );
  }
  
}


$space = new StoreBackedUriSpace();
$space->dispatch();

?>
