<?php
// this file is not in SVN but contains the store credentials
// it defines two constants: AUTH_USER and AUTH_PWD
//include_once(dirname(__FILE__).DIRECTORY_SEPARATOR.'auth.php'); 

if (preg_match('~^([a-z\-]+)\.dataincubator\.org~i', $_SERVER["HTTP_HOST"], $m)) {
  define('DI_DOMAIN', $m[1]);
  define('STORE_URI', 'http://api.talis.com/stores/' . DI_DOMAIN);
  require_once(dirname(dirname(dirname(__FILE__))).DIRECTORY_SEPARATOR.'lib'.DIRECTORY_SEPARATOR.'paget2.php');
}
else {
  header("404 Not Found");  
}


