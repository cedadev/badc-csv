#!/usr/local/ceda_mezzanine/venv/bin/python

# the contents of this file have been replaced with that of csvchecker from https://breezy.badc.rl.ac.uk/aharwood/ceda-archive-website/-/blob/master/cgi-bin/badccsv/csvchecker

import badctextfilewarn
import cgi, io
import cgitb; cgitb.enable()
import traceback, warnings

import sys


from django.conf import settings
import django.template.loader
from django.template import Template, Context
import django
import codecs

badctextfile = badctextfilewarn


settings.configure(TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates','DIRS': [],
                              'APP_DIRS': True,'OPTIONS': {}}],
                   INSTALLED_APPS=['fwtheme_django_ceda_serv', 'fwtheme_django', 'django.contrib.staticfiles', 'cookielaw'],
                   STATIC_URL='/static')
django.setup()

# make a template that extends the base layout from the fwtheme layout. This replaces the content block with a content variable     


def page(messages):

    t = Template('{% extends "fwtheme_django/layout.html" %} {% block content_header %}{% endblock content_header %} {% block content %}{{content|safe}}{% endblock content %}')

    if messages == []:
        messages = 'Please select a file to check'
    print("Content-type: text/html\n")

    content = """   
               <h1>BADC CSV file checker - Output</h1>
               <form action="csvchecker" method="post" enctype="multipart/form-data">
	       <table>
               <tr><td><input type="file" name="file"/>
	       <td><input type="submit" name="Submit" value="Check file" />
	       </td></tr>
	       </table>
               </form> 
               
               %s  
            """ % messages

    content = content + """<hr><h3>Standard metadata </h3>
  
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
            	
        content = content +  "<tr>%s<td>%s</td><td>%s</td></tr>" % (htmllabel, glob_or_col, meaning) 
        
    content = content + "</table>"



	
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    print(t.render(Context({'content': content.decode(encoding='ASCII', errors='replace')})))


form = cgi.FieldStorage()
if form:
  if "file" in form:
    filecontent=form["file"].value
    fh = io.StringIO(filecontent)
    fh.mode = 'r'
    
    try: 
      t = badctextfile.BADCTextFile(fh)
    except: 
      page(["parsing errors:",sys.exc_info()[1]])
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


