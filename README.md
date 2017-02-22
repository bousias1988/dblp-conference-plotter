# dblp-conference-plotter Synopsis

DBLP conference plotter is a desktop application which allows the user to depict conference locations utilizing google maps background. The user may produce a map based on a specified author or based on a conference name.

The user is provided with a Graphical User Interface and two basic search modes: (a) search by author and (b) search by conference.
(a) Search by author mode allows the user to depict locations of all the conferences the author has attended.
(b) Search by conference mode allows the user to depict the locations where a conference has been held over time.

# How to - Installation
Compile and run the program in any Python environment.
The following libraries have to be installed:
BeautifulSoup
gmplot
...


# Contents
dblp_search_and_draw_GUI5.py (main app)
dbOps.py (includes all DB handling operations)
test.db (db file. An instance is provided. In case it is deleted, it is created on next run.)
mymap.html (Output file, which contains the final map. It is created after each run.)


# Various Info
This project was created by Bousias-Alexakis Evangelos and Kostoulas Aristotelis as part of the Contemporary Web Applications course of the Techno-Economic Systems Post-Graduate program run by the National Technical University of Athens. The project was supervised by Assistant Professor Ioannis Anagnostopoulos and PhD Candidate Gerasimos Razis, who we would like to thank for their guidance and support during project development.
