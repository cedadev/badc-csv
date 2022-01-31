#!/usr/bin/python

import badctextfilewarn
import cgi, StringIO
import cgitb; cgitb.enable()
import traceback, warnings

import sys

badctextfile = badctextfilewarn

def page(messages):
    if messages == []:
        messages = 'Please select a file to check'
    print  "Content-type: text/html\n"
    print  """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "DTD/xhtml1-strict.dtd">
             <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
             <head>
               <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
               <link rel="stylesheet" href="/styles/meet.css" type="text/css" />
               <title>BADC CSV file checker</title>
             </head>
             <body>
               <h1>BADC CSV file checker - Output</h1>
               <form action="badctextfileChecker-cgi-warn.py" method="post"  
            enctype="multipart/form-data">
                 <input type="file" name="file"/>
                 <input type="submit" name="Submit" value="Check file" /></p>
               </form> 
               
               %s  
            """ % messages

    print"""<hr><h3>Standard metadata </h3>
  
            <p>Full documentation is available on the <a href="http://help.ceda.ac.uk/article/105-badc-csv">BADC-CSV format page</a> on the on the CEDA website</p>
            <p>Red = compulsory elemetents for basic conformance, green = required elements for complete conformance to the metadata standard; other entries are optional, but encouraged.
            </p><p>Data providers are also welcome to add additional metadata entries if desired, but should accompany these with a sutiable comment line to explain to the end user.</p>
            
            <table>
            <tr><th>Label</th><th>Global or Column</th><th>Meaning</th></tr>"""
    
    for label in badctextfile.BADCTextFile.MDinfoOrder:
      
        applyg, applyc, mino, maxo, mandb, mandc, check, meaning = badctextfile.BADCTextFile.MDinfo[label]
        if applyg:
            if applyc:
                glob_or_col = "G or C"
            else:
                glob_or_col = "G"
        else:
            glob_or_col = "C"	
      
        if mandb: htmllabel = '<td bgcolor="#ff5555">%s</td>' % label 
        elif mandc: htmllabel = '<td bgcolor="#55ff55">%s</td>' % label 
        else: htmllabel = '<td>%s</td>' % label 
            	
        print "<tr>%s<td>%s</td><td>%s</td></tr>" % (htmllabel, glob_or_col, meaning) 
        
    print """ </table></body></html>"""


form = cgi.FieldStorage()
if form:
  if form.has_key("file"):
    filecontent=form["file"].value
    fh = StringIO.StringIO(filecontent)
    fh.mode = 'r'
    
    try: 
      t = badctextfile.BADCTextFile(fh)
    except: 
      page(["parsing errors:",sys.exc_value])
      sys.exit()
      
    # do basic checks 
    with warnings.catch_warnings(record=True) as w:  
      warnings.simplefilter("always")
      t.check_complete()
      s = '<h2>Basic standard conformance checks:</h2>\n'   
      if len(w) == 0: s=s+"File conforms with basic metadata requirements"  
      for ww in w:
        s = s+"<pre>%s</pre>" % ww.message    

    with warnings.catch_warnings(record=True) as w:  
      warnings.simplefilter("always")
      t.check_complete(1)
      s = s+'<h2>Complete standard conformance checks:</h2>\n'   
      if len(w) == 0: s=s+"File additionally conforms with complete metadata"  
      for ww in w:
        s = s+"<pre>%s</pre>" % ww.message    

    page(s)
    
else: 
  page([])
  sys.exit()

