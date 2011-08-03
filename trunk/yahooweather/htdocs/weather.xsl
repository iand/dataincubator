<?xml version="1.0" encoding="UTF-8" ?>
<!--
	untitled
	Created by Keith Alexander on 2009-06-03.
	Copyright (c) 2009 Talis Information Ltd. All rights reserved.
-->

<xsl:stylesheet version="1.0"
                	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
				    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
				    xmlns:foaf="http://xmlns.com/foaf/0.1/"
				    xmlns:sioc="http://rdfs.org/sioc/spec/"
				    xmlns:dc="http://purl.org/dc/elements/1.1/"
				    xmlns:dct="http://purl.org/dc/terms/"
				    xmlns:weather="http://vocab.org/weather#"
				    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
				    xmlns:ov="http://open.vocab.org/terms/"
				    xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#"
					xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0"
                    xmlns="http://purl.org/rss/1.0/"
				>


	<xsl:output encoding="UTF-8" indent="yes" method="xml"/>
	<xsl:strip-space elements="*"/>					
	<xsl:template match="/">
	<rdf:RDF>
	    <channel rdf:about="">
	        <title><xsl:value-of select="///title"/> as Linked Data</title>
		<geo:SpatialThing><xsl:attribute name="rdf:about">http://placetime.com/geopoint/wgs84/X<xsl:value-of select="//item/geo:lat"/>Y<xsl:value-of select="//item/geo:long"/></xsl:attribute>
			<weather:forecast>
				<weather:Forecast rdf:about="#forecast">
					<rdfs:label><xsl:value-of select="//item/title"/></rdfs:label>
					<dct:creator>
					    <foaf:Agent rdf:about="http://yahooweather.dataincubator.org/agents/yahooweather">
						    <foaf:homepage><xsl:attribute name="rdf:resource">http://weather.yahoo.com</xsl:attribute></foaf:homepage>
					    </foaf:Agent>
					</dct:creator>
					<dct:created><xsl:value-of select="//item/pubDate"/></dct:created>
					<foaf:isPrimaryTopicOf>
						<xsl:attribute name="rdf:resource"><xsl:value-of select="//item/link"/></xsl:attribute>
					</foaf:isPrimaryTopicOf>
					<weather:sunrise><xsl:value-of select="//yweather:astronomy/@sunrise"/></weather:sunrise>
					<weather:sunset><xsl:value-of select="//yweather:astronomy/@sunset"/></weather:sunset>
					<weather:date><xsl:value-of select="//yweather:condition/@date"/></weather:date>
					<weather:temperature><xsl:call-template name="getDatatype"><xsl:with-param name="unit" select="//yweather:units/@temperature"/></xsl:call-template><xsl:value-of select="//yweather:condition/@temp"/></weather:temperature>
		
			           <weather:windChill><xsl:call-template name="getDatatype"><xsl:with-param name="unit" select="//yweather:units/@temperature"/></xsl:call-template><xsl:value-of select="//yweather:wind/@chill"/></weather:windChill>

			           <weather:windSpeed><xsl:value-of select="//yweather:wind/@speed"/></weather:windSpeed>
			           <weather:windDirection><xsl:value-of select="//yweather:wind/@direction"/></weather:windDirection>

			           <dct:description rdf:datatype="http://dbpedia.org/resource/HTML"><xsl:value-of select="//item/description"/></dct:description>

			           <weather:humidity><xsl:call-template name="getDatatype"><xsl:with-param name="unit" select="//yweather:units/@temperature"/></xsl:call-template><xsl:value-of select="//yweather:atmosphere/@humidity"/></weather:humidity>

			           <weather:visibility><xsl:value-of select="//yweather:atmosphere/@visibility"/><xsl:call-template name="getDatatype"><xsl:with-param name="unit" select="//yweather:units/@distance"/></xsl:call-template></weather:visibility>
			           <weather:pressure><xsl:value-of select="//yweather:atmosphere/@pressure"/><xsl:call-template name="getDatatype"><xsl:with-param name="unit" select="//yweather:units/@pressure"/></xsl:call-template></weather:pressure>
			           <weather:rising><xsl:value-of select="//yweather:atmosphere/@rising"/></weather:rising>
				</weather:Forecast>
			</weather:forecast>
		</geo:SpatialThing>
		</channel>
	</rdf:RDF>
	</xsl:template>
	
	<xsl:template name="getDatatype">
		<xsl:param name="unit"/>
		<xsl:param name="value"/>
		    <rdf:Description>
			<xsl:if test="$unit = 'F'">
				<xsl:attribute name="rdf:datatype">http://dbpedia.org/resource/Fahrenheit</xsl:attribute>
			</xsl:if>
			<xsl:if test="$unit = 'C'">
				<xsl:attribute name="rdf:datatype">http://dbpedia.org/resource/Celcius</xsl:attribute>
			</xsl:if>
			<!-- <xsl:if test="$unit = 'km'"><xsl:attribute name="rdf:datatype">http://dbpedia.org/resource/Kilometer</xsl:attribute></xsl:if>
			<xsl:if test="$unit = 'mi'"><xsl:attribute name="rdf:datatype">http://dbpedia.org/resource/Mile</xsl:attribute></xsl:if>
			<xsl:if test="$unit = 'mph'"><xsl:attribute name="rdf:datatype">http://dbpedia.org/resource/Mph</xsl:attribute></xsl:if>
			<xsl:if test="$unit = 'kmph'"><xsl:attribute name="rdf:datatype">http://dbpedia.org/resource/Kmph</xsl:attribute></xsl:if>
			<xsl:if test="$unit = 'mb'"><xsl:attribute name="rdf:datatype">http://dbpedia.org/resource/Millibar</xsl:attribute></xsl:if> -->
			</rdf:Description>
	</xsl:template>
</xsl:stylesheet>
