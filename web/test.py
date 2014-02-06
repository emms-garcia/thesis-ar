#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import json
import cgi
import os
import time

form = cgi.FieldStorage()
print "Content type: text/html \n"
print form.getvalue("lat", "no latitude")
print form.getvalue("lon", "no longitude")
