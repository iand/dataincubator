<?php
// this file is not in SVN but contains the store credentials
// it defines two constants: AUTH_USER and AUTH_PWD
//include_once(dirname(__FILE__).DIRECTORY_SEPARATOR.'auth.php'); 

define('STORE_URI', 'http://api.talis.com/stores/moseley');
define('DI_DOMAIN', 'moseley');
require_once(dirname(dirname(dirname(__FILE__))).DIRECTORY_SEPARATOR.'lib'.DIRECTORY_SEPARATOR.'paget2.php');
