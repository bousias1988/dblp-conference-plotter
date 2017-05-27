# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 20:24:50 2016

@author: user
"""

import requests as req

import xml.etree.ElementTree as ET

import sys

reload(sys)
sys.setdefaultencoding('utf8')
import dbOps
import gmplot
import urllib2
import re
# import htmlentitydefs

import webbrowser
from HTMLParser import HTMLParser
import json
import time

from bs4 import BeautifulSoup

TITLE_FONT = ("Helvetica", 8, "bold")


# source url: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter/7557028#7557028


def search_for_conf(conf_name):
    conf_name1 = conf_name.replace(' ', '%20')
    search_html = req.get('http://dblp.org/search/venue/api?q=' + conf_name1)

    conf = ET.fromstring(search_html.text)
    temp_list = []
    if conf.find("hits").attrib["sent"] == '0':
        print("Conference not found", "Sorry conference not found. Please try again.")
    else:
        for child in conf.find("hits"):
            if child.find('info').find('type').text != 'Journal':
                temp_list.append([child.find('info').find('url').text, child.find('info').find('venue').text])
        print temp_list
    return temp_list

def main_conf_function(conf_url, conf_name):
    html_conf = BeautifulSoup(req.get(conf_url).text, "html.parser")
    conf_name2 = conf_name
    all_conf = html_conf.find_all('h2')
    print all_conf[0]
    locations = []
    for iconf in all_conf:
        if str(iconf).find('</a>') != -1:
            a = str(iconf).find('</a>')
            b = str(iconf)[a::].find(':')
            loc_year = str(iconf)[a + b - 4:a + b]
            c = a + b + 2
            d = str(iconf)[c::].find('<')
            locations.append([str(iconf)[c:c + d], conf_name2, loc_year])
        else:
            if str(iconf).find(':') != -1:
                e = str(iconf).find(':')
                loc_year = str(iconf)[e - 4:e]
                e = e + 2
                f = str(iconf)[e::].find('<')
                loc_place = str(iconf)[e:e + f]
                locations.append([loc_place, conf_name2, loc_year])
    # locations
    # for loc in locations:
    #    print loc
    locations1 = []
    final_locations = []
    for loc in locations:
        loc
        con_res = dbOps.check_if_loc_exists(loc[0])
        if con_res != 0:
            [(temp_lat, temp_lng)] = dbOps.get_coord_from_DB(loc[0])
            final_locations.append((temp_lat, temp_lng, loc[0], loc[1], loc[2]))
        else:
            locations1.append(loc)
    locations2 = []
    for i in locations1:
        locations2.append(i[0])
    locations3 = get_coord_google(locations2)
    for i in locations3:
        dbOps.add_location(i[0], i[1], i[2])
    for iloc in locations1:
        [(temp_lat, temp_lng)] = dbOps.get_coord_from_DB(iloc[0])
        final_locations.append((temp_lat, temp_lng, iloc[0], iloc[1], iloc[2]))
    # print final_locations
    draw_final_map(final_locations)
    return final_locations


# Enter the rest of the code!

def search_dblp(author_name, author_surname):

    author_name = author_name.lower()
    author_surname = author_surname.lower()

    if author_name != None:
        search_xml = req.get('http://dblp.org/search/author/api?q=' + author_name + '%20' + author_surname + '$')
    else:
        search_xml = req.get('http://dblp.org/search/author/api?q=' + author_surname + '$')

    author = ET.fromstring(search_xml.text)
    temp_list_url = []
    temp_list_author = []

    if author.find("hits").attrib["sent"] == '0':
        print("Author not found",
              "Sorry author not found. Try again.\n You could try using only his last name")
    else:
        # collect all urls
        for child in author.find("hits"):
            temp_list_author.append(child.find('info').find('author').text)
            temp_list_url.append(child.find('info').find('url').text)
        temp_list = zip(temp_list_author,temp_list_url)
    return temp_list



def get_final_part_of_url(url):
    url_req = urllib2.Request(url)
    url_res = urllib2.urlopen(url_req)
    url = url_res.geturl()
    reversed_url = url[::-1]
    reversed_f_part = reversed_url.partition("/")[0] + reversed_url.partition("/")[1]
    reversed_rest = reversed_url.partition(reversed_f_part)[2]
    reversed_s_part = reversed_rest.partition("/")[0] + reversed_rest.partition("/")[1]
    reversed_concat = reversed_f_part + reversed_s_part
    url = reversed_concat[::-1]
    return url


def get_conf_data_xml(part_of_url):
    # Fetch author's XML page and convert to string
    author_req = urllib2.Request('http://dblp.uni-trier.de/pers/xx' + part_of_url + '.xml')
    author_response = urllib2.urlopen(author_req)
    webpage = author_response.read()
    webstr = webpage.decode(encoding="utf-8", errors="strict")

    # Parse XML to get root element (dblpperson)
    parser = ET.XMLParser(encoding="utf-8")
    root = ET.fromstring(webstr, parser=parser)

    # Populate Lists with values from each xml Element
    conf_title = []
    conf_year = []
    conf_url = []

    for elem in root.findall("./r/inproceedings/url"):
        conf_url.append(elem.text)
    for elem in root.findall("./r/inproceedings/booktitle"):
        conf_title.append(elem.text)
    for elem in root.findall("./r/inproceedings/year"):
        conf_year.append(elem.text)

    # remove anchor (# and the part after it) in URL tail
    clean_conf_url = []  # all URLs without anchor in tail
    for url in conf_url:
        head, sep, tail = url.partition('#')
        clean_conf_url.append(head)

    conf_all = zip(conf_title, conf_year, clean_conf_url)  # keep them together
    dist_title_year_url = list(set(conf_all))  # and remove duplicates
    return dist_title_year_url


def get_conf_data_web(dist_title_year_url):
    parser = HTMLParser()
    locations_arg = []

    for item in dist_title_year_url:
        conf_req = urllib2.Request('http://dblp.uni-trier.de/' + item[2])
        conf_response = urllib2.urlopen(conf_req)
        conf_page = conf_response.read()
        pattern = re.compile('<header class="headline noline"><h1>.*:\n(.*)</h1> </header>')
        pattern1 = re.findall(pattern, conf_page)
        if pattern1.__len__() != 0:
            find_pattern = parser.unescape(pattern1[0])
            print(find_pattern)
            locations_arg.append(find_pattern)
        else:
            find_pattern = 'Unknown'
            print(find_pattern)
            locations_arg.append(find_pattern)

    l0 = zip(*dist_title_year_url)  # unzip title year url to zip them with location
    l1 = l0[0]  # title
    l2 = l0[1]  # year
    l3 = l0[2]  # url

    dist_title_year_url_loc = zip(l1, l2, l3, locations_arg)
    return dist_title_year_url_loc


def get_coord_google(names1_arg):
    t_lat1 = []
    t_lng1 = []
    t_names = []
    cnt = 0
    for city in names1_arg:
        if city == 'Unknown':
            lat = 0.000000
            lng = 0.000000
            t_lat1.append(lat)
            t_lng1.append(lng)
            t_names.append(city)
            continue
        cnt += 1
        geocode = req.get(
            'http://maps.googleapis.com/maps/api/geocode/json?address="%s"' % city)
        geocode = json.loads(geocode.text)
        print city
        if geocode['status'] == 'ZERO_RESULTS':
            lat = 0.000000
            lng = 0.000000
            t_lat1.append(lat)
            t_lng1.append(lng)
            t_names.append(city)
            cnt += 1
            continue
        lat = geocode['results'][0]['geometry']['location']['lat']
        lng = geocode['results'][0]['geometry']['location']['lng']
        t_lat1.append(lat)
        t_lng1.append(lng)
        t_names.append(city)
        if cnt > 9:
            cnt = 0
            time.sleep(2)  # Papatziliki gia na tre3ei olh h lista
            print "Waiting for Google..."

    dist_loc_lat_lng_out = zip(t_names, t_lat1, t_lng1)
    return dist_loc_lat_lng_out


def draw_final_map(resarg_input):
    # reasrg (lat,lon, city_country, conference, year)
    resarg = []
    for entry in resarg_input:
        resarg.append(list(entry))
    # list1.sort(key= lambda place: place[2])
    resarg.sort(key=lambda resarg: resarg[2])
    print resarg
    resarg1 = []
    res0 = resarg[0]
    print res0
    res0.append('cornflowerblue')
    res0.append(res0[2] + ' ' + res0[3] + ' ' + str(res0[4]))
    resarg1.append(res0)
    index1 = 0
    for res in resarg[1::]:
        print res
        print res[2], res0[2]
        print index1
        if res[2] == res0[2]:
            print type(resarg1[index1][2])
            print type(res[2])
            resarg1[index1][5] = 'red'
            resarg1[index1][6] = resarg1[index1][6] + ' \\n ' + res[2] + ', ' + res[3] + ', ' + str(res[4])
        else:
            res.append('cornflowerblue')
            res.append(res[2] + ', ' + res[3] + ', ' + str(res[4]))
            resarg1.append(res)
            res0 = resarg1[index1 + 1]
            print 'res0', res0, ',', index1
            print 'resarg1[index1+1]', resarg1[index1 + 1], ',', index1
            index1 = index1 + 1

    gmap = gmplot.GoogleMapPlotter(0, 0, 5)  # apla gia na ftia3w to object

    lat1 = [item[0] for item in resarg1]
    lon1 = [item[1] for item in resarg1]
    names1 = [item[6] for item in resarg1]
    color1 = [item[5] for item in resarg1]

    zlvl = zoomlvl(lat1, lon1)
    c_lat, c_lng = map_center(lat1, lon1)
    gmap = gmplot.GoogleMapPlotter(c_lat, c_lng, zlvl)
    coord = zip(lat1, lon1, names1, color1)
    for i in coord:
        if (i[0] != 0) & (i[1] != 0):
            gmap.marker(i[0], i[1], i[3], title=i[2])

    gmap.draw("mymap.html")

    webbrowser.open_new("mymap.html")
    # return resarg2


def zoomlvl(t_lat1, t_lng1):
    if t_lat1.__len__() > 1:
        a = 360 - (max(t_lng1) - min(t_lng1))
        if a < 10:
            z_lvl = 1
        elif a < 90:
            z_lvl = 2
        else:
            z_lvl = 3
    else:
        z_lvl = 5
    return z_lvl


def map_center(t_lat1, t_lng1):
    if t_lat1.__len__() > 1:
        a = max(t_lng1) - min(t_lng1)
        ce_lng = a / 2 + min(t_lng1)
        ce_lat = (max(t_lat1) - min(t_lat1)) / 2 + min(t_lat1)
    else:
        ce_lng = t_lng1[0]
        ce_lat = t_lat1[0]
    return ce_lat, ce_lng


class Author:
    '''Surname = ""
    Name = ""
    author_id = 0   # Author's id in db
    cnr = 0         # Number of Conferences in xml file
    dbcnr = 0       # Number of Conferences in db
    initial = ''
    alreadyIn= False #Boolean False -> the author isn't in the Database yet
    '''
    def __init__(self, author_url, cnr=0, dbcnr=0,alreadyIn=False):
        #self.Surname = surname
       # self.Name = name
        self.author_url = author_url
        self.cnr = cnr
        self.dbcnr = dbcnr
        #self.initial = surname.lower()[0]
        self.alreadyIn= alreadyIn
        self.author_id = 0


def main_function(authorUrl):
    # Setup DB
    dbOps.create_tables()

    newAuthor = Author(authorUrl)

    # Check if author exists in db
    newAuthor.alreadyIn = dbOps.check_author_id(newAuthor.author_url)

    # If new, add author to the db and fetch the new id
    if not (newAuthor.alreadyIn):
        x = dbOps.add_person(newAuthor.author_url)
        newAuthor.alreadyIn = True

    newAuthor.author_id = dbOps.get_author_id(newAuthor.author_url)
    # Get xml and Conference Title, Year and URL from it
    print get_final_part_of_url(authorUrl)
    distConfAll = get_conf_data_xml(get_final_part_of_url(authorUrl))

    # Get number of Author's Conferences from xml
    newAuthor.cnr = len(distConfAll)
    # Get number of Author's Conferences from db
    newAuthor.dbcnr = dbOps.get_dbcnr(newAuthor.author_url)

    if newAuthor.cnr > newAuthor.dbcnr:
        # Get Locations
        dist_title_year_url_new = []
        for conf in distConfAll:
            check = dbOps.check_if_conf_exists(conf[0], conf[1])
            if check == 0:
                dist_title_year_url_new.append(conf)

        if dist_title_year_url_new:
            distConfAllwLoc = get_conf_data_web(dist_title_year_url_new)
            distConfAllwLoc_unzip = zip(*distConfAllwLoc)
            locations = distConfAllwLoc_unzip[3]

            for conference in distConfAllwLoc:
                dbOps.add_conference(conference[0], conference[1])

            names1 = []
            for location in locations:
                if dbOps.check_if_loc_exists(location) == 0 and location.__len__() != 0 and location not in names1:
                    print(location)
                    names1.append(location)
            if names1:
                distLocLatLng = get_coord_google(names1)

                for location in distLocLatLng:
                    dbOps.add_location(location[0], location[1], location[2])

            for conference in distConfAllwLoc:
                dbOps.update_conf(conference[0], conference[1], conference[3])

        for conference in distConfAll:
            dbOps.add_participation(newAuthor.author_id, dbOps.get_conf_id(conference[0], conference[1]))

        dbOps.update_dbcnr(newAuthor.author_url)

    res = dbOps.get_info_for_map(newAuthor.author_url)
    print(res)
    if res != []:
        draw_final_map(res)


##End of the rest of the code!!


if __name__ == "__main__":
    main_function('http://dblp.org/pers/a/Anagnostopoulos:Ioannis')

