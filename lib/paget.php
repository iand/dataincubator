<?php
if (!defined('STORE_URI') ) {
  echo "STORE_URI not defined";
  exit; 
}


ob_start("ob_gzhandler"); 
define('LIB_DIR', dirname(dirname(dirname(__FILE__))) . '/lib/');
define('PAGET_DIR', LIB_DIR . 'paget' . DIRECTORY_SEPARATOR);
define('MORIARTY_DIR', LIB_DIR . 'moriarty' . DIRECTORY_SEPARATOR);
define('MORIARTY_ARC_DIR', LIB_DIR . 'arc_2008_11_18' . DIRECTORY_SEPARATOR);

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
    $augment = TRUE;
    if ( preg_match('~\.(rdf|xml|turtle|json)$~', $uri, $m) ) {
      $augment = FALSE;
    }
    $desc = new StoreBackedResourceDescription($uri, STORE_URI, $augment); 
    $desc->set_namespace_mapping('bibo', 'http://purl.org/ontology/bibo/');
    $desc->set_namespace_mapping('bio', 'http://vocab.org/bio/0.1/');
    $desc->set_namespace_mapping('ol', 'http://olrdf.appspot.com/key/');
    $desc->set_namespace_mapping('ov', 'http://open.vocab.org/terms/');
    return $desc;
  } 
  
  function get_template($request) {
    return dirname(dirname(__FILE__)) . "/lib/paget-template.html";
  } 
    
  
}

class StoreBackedResourceDescription extends PAGET_ResourceDescription {   
  var $_store_uri;
  var $_augment;
  
  function __construct($uri, $store_uri, $augment) {
    $this->_store_uri = $store_uri; 
    $this->_augment = $augment;
    parent::__construct($uri);
  }

  function get_augmentors() {
    if ($this->_augment) {
      return  array( new PAGET_SimplePropertyLabeller() );
    }
    else {
      return array();
    }
  }

  function get_generators() {
    return array( new PAGET_StoreDescribeGenerator($this->_store_uri, 'scbd') );
  }
  
}


$space = new StoreBackedUriSpace();
$space->dispatch();

?>
