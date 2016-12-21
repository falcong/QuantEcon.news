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

#-BUILD-#

CONFIG_LECTURES = {
    'build_dir' : "./lecture_site/",
    'tag' : "lecture-site"
}

CONFIG_ORG = {
    'build_dir' : "./org_site/",
    'tag' : "org-site"
}

BUILD = [CONFIG_LECTURES, CONFIG_ORG]

#--------------------#
#-Document Templates-#
#--------------------#

#-RST-#
rst_filename  = "news.rst"
rst_doc       = [
                ".. _%s:" % rst_filename.split(".")[0]    , 
                ""                          , 
                "*************************" , 
                "News & Announcements"      , 
                "*************************" , 
                ""
                ]
#-HTML-#
html_items = 4
html_filename = "news_snippet.html"
html_doc =  [
            r'<div class="news clearfix">'  , 
            r'<h2>News</h2>'                ,
            r'<ul>'                         ,
            ]   
html_end =  [r'</ul>',r'<p class="more"><a href="/common/news.html">Read more QuantEcon news</a></p>',r'</div>']

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
        dates.append((year, month_to_num[month], day))
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
    doc = {k: v for k,v in doc.items() if project['tag'] in v['website']}

    #-Build RST Document-#

    dates = _to_numeric_dates(list(doc.keys()))
    for year, month, day in sorted(dates, reverse=True):
        date = "%s-%s-%s" % (day, num_to_month[month], year)
        rst_doc.append(date)
        rst_doc.append("-"*len(date))
        rst_doc.append("")
        rst_doc.append(doc[date]['description'].replace("\n", "\n\n"))
    #-Write RST Document-#
    print("Writing RST File: %s" % rst_filename)
    write_file(os.path.join(project['build_dir'], rst_filename), rst_doc)

    #-Build HTML Snippet-#

    for year, month, day in sorted(dates, reverse=True)[:html_items]:
        date = "%s-%s-%s" % (day, num_to_month[month], year)                #Long Date Style: '03-October-2014'
        short_date = "%s %s %s" % (day, num_to_month[month][:3], year)      #Short Date Style: '03 Oct 2014'
        html_id = "%s-%s" % (num_to_month[month].lower(), year)
        html_doc.append(r'<li><span class="date">'+short_date+r'</span> <a href="%s/news.html#%s">'%(project['build_dir'], html_id)+doc[date]['title'].rstrip("\n")+r'</a>')
        html_doc.append(r'<span class="summ">'+doc[date]['summary'].rstrip("\n")+r'</span></li>')
    html_doc += html_end
    #-Write HTML Snippet-#
    print("Writing HTML File: %s" % html_filename)
    write_file(os.path.join(project['build_dir'], html_filename), html_doc)


