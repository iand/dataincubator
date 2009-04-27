<?php
if (!defined('STORE_URI') ) {
  echo "STORE_URI not defined";
  exit; 
}


ob_start("ob_gzhandler"); 
define('LIB_DIR', dirname(dirname(dirname(__FILE__))) . '/lib/');
define('PAGET_DIR', LIB_DIR . 'paget2' . DIRECTORY_SEPARATOR);
//define('PAGET_DIR', '/home/iand/wip/paget2/');
define('MORIARTY_DIR', LIB_DIR . 'moriarty' . DIRECTORY_SEPARATOR);
define('MORIARTY_ARC_DIR', LIB_DIR . 'arc_2008_11_18' . DIRECTORY_SEPARATOR);

if (!defined('MORIARTY_HTTP_CACHE_DIR') && defined('DI_DOMAIN') && file_exists(dirname(dirname(__FILE__)).DIRECTORY_SEPARATOR.'cache')) {
  $cache_dir = dirname(dirname(__FILE__)).DIRECTORY_SEPARATOR.'cache'.DIRECTORY_SEPARATOR.DI_DOMAIN;
  if ( ! file_exists($cache_dir)) {
    if (mkdir($cache_dir) === FALSE) {
      echo 'Could not create cache directory ' . $cache_dir;
      exit; 
    }
  }
  define('MORIARTY_HTTP_CACHE_DIR', $cache_dir);
}

define('MORIARTY_HTTP_CACHE_READ_ONLY', TRUE);
define('MORIARTY_HTTP_CACHE_USE_STALE_ON_FAILURE', TRUE ); // use a cached response if network fails



//require_once PAGET_DIR . 'paget_urispace.class.php';
//require_once PAGET_DIR . 'paget_simplepropertylabeller.class.php';
//require_once PAGET_DIR . 'paget_storedescribegenerator.class.php';
require_once PAGET_DIR . 'paget_storebackedurispace.class.php';

$space = new PAGET_StoreBackedUriSpace(STORE_URI);
$space->set_description_template(dirname(dirname(__FILE__)) . "/lib/paget2-desc-template.html");
$space->set_search_template(dirname(dirname(__FILE__)) . "/lib/paget2-search-template.html");
$space->set_namespace_mapping('bibo', 'http://purl.org/ontology/bibo/');
$space->set_namespace_mapping('bio', 'http://vocab.org/bio/0.1/');
$space->set_namespace_mapping('ol', 'http://olrdf.appspot.com/key/');
$space->set_namespace_mapping('ov', 'http://open.vocab.org/terms/');
$space->set_namespace_mapping('void', 'http://rdfs.org/ns/void#');
$space->dispatch();

?>
