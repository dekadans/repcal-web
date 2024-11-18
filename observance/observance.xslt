<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <xsl:param name="dayUrl" select="'#'"/>
    <xsl:param name="monthUrl" select="'#'"/>

    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="observance">
        <span class="observance">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <xsl:template match="day">
        <a href="{$dayUrl}">
            <xsl:apply-templates/>
        </a>
    </xsl:template>

    <xsl:template match="month">
        <a href="{$monthUrl}">
            <xsl:apply-templates/>
        </a>
    </xsl:template>
</xsl:stylesheet>