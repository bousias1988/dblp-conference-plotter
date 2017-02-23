# dblp-conference-plotter Synopsis

DBLP conference plotter is a desktop application which allows the user to depict conference locations utilizing google maps background. The user may produce a map based on a specified author or based on a conference name.

The user is provided with a Graphical User Interface and two basic search modes: (a) search by author and (b) search by conference.
<br/>
(a) Search by author mode allows the user to depict locations of all the conferences the author has attended.
<br/>
(b) Search by conference mode allows the user to depict the locations where a conference has been held over time.

# How to - Installation
Download 'dblp_search_and_draw_GUI_.py', 'dbOps.py' and 'test.db' (optionally- if not downloaded, the database is automaticly created during the first run of the program). Place them in the same folder. Compile and run 'dblp_search_and_draw_GUI5.py' file in any Python environment and the Graphical User Interface will pop up.  

## Dependencies
The following modules have to be installed:
<br/> BeautifulSoup
<br/> requests
<br/> gmplot

## Graphical User Interface

The starting frame (Picture 1) allows the user to search dblp based on the author's name and surname (he can also search dblp by using only the author's surname).
![screenshot_22](https://cloud.githubusercontent.com/assets/25885525/23229684/d567be2e-f949-11e6-9301-f434f0d2520c.png)
</br> center(Picture 1 </br>
By pressing the submit button the program interacts with dblp search API and returns all the retrieved URI's in a list form (Picture 2)

# Contents
dblp_search_and_draw_GUI5.py (main app)
dbOps.py (includes all DB handling operations)
test.db (db file. An instance is provided. In case it is deleted, it is created on next run.)
mymap.html (Output file, which contains the final map. It is created after each run.)


# Various Info
This project was created by Bousias-Alexakis Evangelos and Kostoulas Aristotelis as part of the Contemporary Web Applications course of the Techno-Economic Systems Post-Graduate program run by the National Technical University of Athens. The project was supervised by Assistant Professor Ioannis Anagnostopoulos and PhD Candidate Gerasimos Razis, who we would like to thank for their guidance and support during project development.
