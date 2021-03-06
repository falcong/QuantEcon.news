"""
GENERATE NEWS
=============

This script generates supporting news files for:
    lectures.quantecon.org
    www.quantecon.org

The results are rst files and html snippets for inclusion in sphinx compilation

The news information is contained in: news.yaml

Usage
-----
python generate_news.py

Returns
-------

lecture-site/
    news.rst
    news-snippet.html
org-site/
    news.rst
    news-snippet.html

"""

import yaml
import os
import copy

#-BUILD CONFIGURATION AND DOCUMENT TEMPLATES-#

RST_FILENAME = "news.rst"
HTML_FILENAME = "news_snippet.html"

CONFIG_LECTURES = {
    'build_dir' : "./lecture_site/",
    'tag' : "lecture-site",
    'web-folder' : "news",
    #-HTML OPTIONS-#
    'html-items' : 4,
    'html-filename' : "news_snippet.html",
    'html-doc' :   [
                    r'<div class="news clearfix">'  , 
                    r'<h2>News</h2>'                ,
                    r'<ul>'                         ,
                   ],   
    'html-end' : [r'</ul>',r'<p class="more"><a href="/news/news.html">Read more QuantEcon news</a></p>',r'</div>'],
    #-RST OPTIONS-#
    'rst-doc': [
                ".. _%s:" % RST_FILENAME.split(".")[0]    , 
                ""                          ,
                "*************************" , 
                "News & Announcements"      , 
                "*************************" , 
                ""
                ],
}

CONFIG_ORG = {
    'build_dir' : "./org_site/",
    'tag' : "org-site",
    'web-folder' : "",
    #-HTML OPTIONS-#
    'html-items' : 3,
    'html-doc' :   [
                    r'<div class="news clearfix">'  , 
                    r'<h2>News</h2>'                ,
                    r'<ul>'                         ,
                   ],   
    'html-end'   : [r'</ul>',r'<p class="more"><a href="news.html">Read more QuantEcon news</a></p>',r'</div>'],
    #-RST OPTIONS-#
    'rst-doc': [
                ".. _%s:" % RST_FILENAME.split(".")[0]    , 
                ""                          ,
                ".. include:: org_banner.raw", 
                ""                          ,
                "*************************" , 
                "News & Announcements"      , 
                "*************************" , 
                ""
                ],

}

BUILD = [CONFIG_LECTURES, CONFIG_ORG]

#-Check if Directories are present-#
for project in BUILD:
    if not os.path.isdir(project["build_dir"]):
        print("Setting up directory: %s" % project["build_dir"])
        os.makedirs(project["build_dir"])

#------------#
#-Month Data-#
#------------#

month_to_num = {
    'January'   : 1,
    'February'  : 2,
    'March'     : 3,
    'April'     : 4,
    'May'       : 5,
    'June'      : 6,
    'July'      : 7,
    'August'    : 8,
    'September' : 9,
    'October'   : 10,
    'November'  : 11,
    'December'  : 12,
}
num_to_month = {v:k for k,v in list(month_to_num.items())}

#------------------#
#-Helper Functions-#
#------------------#

def write_file(filename, data):
    f = open(filename, 'w')
    for line in data:
        f.write(line+"\n")
    f.close()

def _to_numeric_dates(datelist):
    """ Convert to Numeric Dates """
    dates = []
    for date in datelist:
        (day,month,year) = date.split('-')
        dates.append((int(year), int(month_to_num[month]), int(day)))
    return dates

#------------#
#---Script---#
#------------#

for project in BUILD:
    print("[generate_news.py] Building news for %s" % project['tag'])

    #-Open YAML File-#
    fl = open('news.yaml', 'r') #-YAML at Base Level of Repo-#
    doc = yaml.load(fl)
    #-Filter for Project Tags-#
    doc = {k: v for k,v in doc.items() if project['tag'] in v['website'].strip("\n")}

    #-Build RST Document-#
    rst_doc = copy.copy(project['rst-doc'])
    dates = _to_numeric_dates(list(doc.keys()))
    for year, month, day in sorted(dates, reverse=True):
        date = "%s-%s-%s" % (str(day).zfill(2), num_to_month[month], year)
        rst_doc.append(date)
        rst_doc.append("-"*len(date))
        rst_doc.append("")
        rst_doc.append(doc[date]['description'].replace("\n", "\n\n"))
    #-Write RST Document-#
    print("Writing RST File: %s" % RST_FILENAME)
    write_file(os.path.join(project['build_dir'], RST_FILENAME), rst_doc)

    #-Build HTML Snippet-#
    HTML_ITEMS = project['html-items']
    html_doc = copy.copy(project['html-doc'])
    for year, month, day in sorted(dates, reverse=True)[:HTML_ITEMS]:
        date = "%s-%s-%s" % (str(day).zfill(2), num_to_month[month], year)                #Long Date Style: '03-October-2014'
        short_date = "%s %s %s" % (day, num_to_month[month][:3], year)      #Short Date Style: '03 Oct 2014'
        html_id = "%s-%s" % (num_to_month[month].lower(), year)
        try:
        	html_doc.append(r'<li><span class="date">'+short_date+r'</span> <a href="%s">'%(doc[date]['link'])+doc[date]['title'].rstrip("\n")+r'</a>')
        except:
        	html_doc.append(r'<li><span class="date">'+short_date+r'</span> <a href="%s/news.html#%s">'%(project['web-folder'], html_id)+doc[date]['title'].rstrip("\n")+r'</a>')
        html_doc.append(r'<span class="summ">'+doc[date]['summary'].rstrip("\n")+r'</span></li>')
    html_doc += project['html-end'] #HTML_END
    #-Write HTML Snippet-#
    print("Writing HTML File: %s" % HTML_FILENAME)
    write_file(os.path.join(project['build_dir'], HTML_FILENAME), html_doc)


