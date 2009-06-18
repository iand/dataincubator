<?php

define('STORE_URI', 'http://api.talis.com/stores/kwijibo-dev2');
define('DI_DOMAIN', 'yahooweather');
$requestUri =  $_SERVER['REQUEST_URI'];//'/forecast/UKXX0295';//
if(preg_match('%/forecast/([A-Z]+\d+)%', $requestUri, $m)){
	$xml = file_get_contents('http://weather.yahooapis.com/forecastrss?p='.$m[1]);
	$dom = new DomDocument();
	$dom->loadXML($xml);
	$xsldom = new DOMDocument();
	$xsldom->loadXML(file_get_contents('weather.xsl'));
	$XslT = new XSLTProcessor();
	$XslT->importStylesheet($xsldom);
	$rdfxml = $XslT->transformToXML($dom);
	header("content-type: application/rdf+xml");
	echo $rdfxml;
	die;
} else {
	echo "request URIs should be of the form /forecast/{yahoo area code}";
}
// if(preg_match('%/now%',$requestUri)){ // now resource uri
// 	//redirect to current date stamped forecast uri
// } else if(){ // dated resource uri
// 	//redirect to
// } else if() { //document uri
// 	
// }
//require_once(dirname(dirname(dirname(__FILE__))).DIRECTORY_SEPARATOR.'lib'.DIRECTORY_SEPARATOR.'paget2.php');
?>