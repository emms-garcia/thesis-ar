#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import cgi

form = cgi.FieldStorage()
print "Content type: text/html \n"
import this
print
print "Latitude: "+form.getvalue("lat", "no latitude")
print "Longitude: "+form.getvalue("lon", "no longitude")
