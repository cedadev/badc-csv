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
    
    print """
    <html>
<head>
<meta name="robots" content="noindex,nofollow">
<title>
Get Data
</title>
<link rel="stylesheet" type="text/css" href="/styles/menu.new.css">

<script language="javascript">

function Start(page) {
OpenWin = this.open (page,"PlotWindow", 
"toolbar=no,menubar=yes,location=no,scrollbars=yes,resizable=yes,width=700,height=700");
OpenWin.focus();
}

function OpenEditWin (page) {
win = this.open (page, "Edit", 
"toolbar=yes,menubar=no,location=no,scrollbars=yes,resizable=yes,width=700,height=600");
win.focus();
}

function OpenPasswdWin (page) {
win = this.open (page, "Passwd", 
"toolbar=yes,menubar=no,location=no,scrollbars=yes,resizable=yes,width=700,height=400");
win.focus();
}

function OpenHelpWin (page) {
win = this.open (page, "Help", 
"toolbar=yes,menubar=no,location=no,scrollbars=yes,resizable=yes,width=500,height=400");
win.focus();
}
</script>

<meta http-equiv="Content-type" content="text/html; charset=utf-8">
<meta name="viewport" content="width=device-width">
<meta name="keywords" content="">
<meta name="description" content="">
<title> | Centre for Environmental Data Archival</title>

<link rel="shortcut icon" href="http://www.ceda.ac.uk/static/img/favicon.ico">
<link rel="alternate" type="application/rss+xml" title="RSS" href="http://www.ceda.ac.uk/blog/feeds/rss/">
<link rel="alternate" type="application/atom+xml" title="Atom" href="http://www.ceda.ac.uk/blog/feeds/atom/">
<link rel="stylesheet" type="text/css" media="screen,projection,print" href="http://www.ceda.ac.uk/static/css/mf54_reset.css" />
<link rel="stylesheet" type="text/css" media="screen,projection,print" href="http://www.ceda.ac.uk/static/css/mf54_grid.css" />
<link rel="stylesheet" type="text/css" media="screen,projection,print" href="http://www.ceda.ac.uk/static/css/mf54_content.css" />

<link rel="stylesheet" type="text/css" media="screen" href="http://www.ceda.ac.uk/static/cookielaw/css/cookielaw.css" />

<script src="http://www.ceda.ac.uk/static/js/jquery-1.10.1.min.js"></script>
<script src="http://www.ceda.ac.uk/static/cookielaw/js/cookielaw.js"></script>


<!--[if lt IE 9]>
<script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script>
<![endif]-->


</head>

<body>
  <!-- CONTAINER FOR ENTIRE PAGE -->
  <div class="container" id="">

    <!-- A. HEADER -->         
    <div class="corner-page-top"></div>        
    <div class="header">
      <div class="header-top">
        
        <!-- A.1 SITENAME -->      
        <a class="sitelogo" href="http://www.ceda.ac.uk" title="CEDA Home"></a>
        <div class="sitename">
        </div>
    
        <!-- A.2 BUTTON NAVIGATION -->
        <div class="navbutton">
          <ul>
            <li><a href="http://www.ceda.ac.uk/blog/feeds/rss/" title="RSS"><img src="http://www.ceda.ac.uk/static/img/rss.png" alt="RSS-Button" /></a></li>
            <li><a href="http://www.ceda.ac.uk/blog/feeds/atom/" title="Atom"><img src="http://www.ceda.ac.uk/static/img/atom.png" alt="Atom-Button" /></a></li>
            <li><a href="http://twitter.com/cedanews" title="Twitter"><img src="http://www.ceda.ac.uk/static/img/twitter.png" alt="Twitter-Button" /></a></li>
          </ul>
        </div>

        <!-- A.X USERSTATUS -->
        <div class="userstatus">
           
           
        </div>
        
        <!-- A.3 GLOBAL NAVIGATION -->
        <div class="navglobal">
            
    

<ul><li><a href="http://www.ceda.ac.uk/blog/">CEDA News</a></li></ul><ul><li><a href="http://www.ceda.ac.uk/contact/">Contact Us</a></li></ul>

        </div>        
      </div>
    
      <!-- A.4 BREADCRUMB and SEARCHFORM -->
      <div class="header-bottom">

            
  <p>&nbsp;</p>  

&nbsp;
 <a href="http://www.ceda.ac.uk">CEDA Home</a> &nbsp;

 <a href="http://badc.nerc.ac.uk">BADC Home</a> &nbsp;
 <a href="http://neodc.nerc.ac.uk">NEODC Home</a>
 


      </div>
    </div>
    <div class="corner-page-bottom"></div>    
    
<div class="editable-original">
      <h1 class="menu"><B>
<FONT SIZE="6">
BADC CSV file checker
</FONT>
</B></h1>
      <p>
               <form action="badctextfileChecker-cgi.py" method="post"  
            enctype="multipart/form-data">
                 <input type="file" name="file"/>
                 <input type="submit" name="Submit" value="Check file" /></p>
               </form> 
              </p>
              <p> 
               %s</p>  
            """ % messages
   
#     print  """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "DTD/xhtml1-strict.dtd">
#              <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
#              <head>
#                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
#                #<link rel="stylesheet" href="/styles/meet.css" type="text/css" />
#                <title>BADC CSV file checker</title>
#              </head>
#              <body>
#                <h1>BADC CSV file checker</h1>
#                <form action="badctextfileChecker-cgi-warn.py" method="post"  
#             enctype="multipart/form-data">
#                  <input type="file" name="file"/>
#                  <input type="submit" name="Submit" value="Check file" /></p>
#                </form> 
#                
#                %s  
#             """ % messages

    print"""<hr><b><font size="6"><h3 class="menu">Standard metadata</font></b> </h3>
  
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
        
    print """ </table>
    </div>
    
            <!-- D. FOOTER -->  
    <div class="corner-page-top"></div>        
            
        <div class="footer">
 
          
    

<ul class="clearfix"><li 
            id="footer-menu-accessibility"><a href="http://www.ceda.ac.uk/accessibility/">Accessibility</a></li></ul><ul class="clearfix"><li 
            id="footer-menu-disclaimer"><a href="http://www.ceda.ac.uk/disclaimer/">Disclaimer</a></li></ul><ul class="clearfix"><li 
            id="footer-menu-privacy-and-cookies"><a href="http://www.ceda.ac.uk/privacy-and-cookies/">Privacy and Cookies</a></li></ul>


        </div>
        <div class="corner-page-bottom"></div> 
    </div> 
 
    </body></html>
    """


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

