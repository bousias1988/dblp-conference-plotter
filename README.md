# dblp-conference-plotter Synopsis

DBLP conference plotter is a desktop application which allows the user to depict conference locations utilizing Google maps background. The user may produce a map based on a specified author or based on a conference name.

The user is provided with a Graphical User Interface and two basic search modes: (a) search by author and (b) search by conference.
<br/>
(a) Search by author mode allows the user to depict locations of all the conferences the author has attended.
<br/>
(b) Search by conference mode allows the user to depict the locations where a conference has been held over time.

# How to - Installation
Download 'dblp_search_and_draw_GUI_.py', 'dbOps.py' and 'dbplSD.db' (optionally- if not downloaded, the database is automatically created during the first run of the program). Place them in the same folder. Compile and run 'dblp_search_and_draw_GUI5.py' file in any Python environment and the Graphical User Interface will pop up.  

## Dependencies
The following modules have to be installed:
<br/> -BeautifulSoup
<br/> -requests
<br/> -gmplot https://github.com/vgm64/gmplot

A known issue of the gmplot module that we also came across is that the marker path does not work on Windows (the markers don't appear in the final map). A solution is described in the following link: https://github.com/vgm64/gmplot/issues/18 .Change the following line
self.coloricon = os.path.join(os.path.dirname(file), 'markers/%s.png')
in the class init definition to
self.coloricon = 'http://www.googlemapsmarkers.com/v1/%s/'

## Graphical User Interface

The starting frame allows the user to search dblp based on the author's name and surname (he can also search dblp by using only the author's surname).<br/>
![starting_frame](https://cloud.githubusercontent.com/assets/25885525/23277653/53cfd40e-fa17-11e6-8939-4e23952aa2a9.PNG)
<br/>
By pressing the submit button the program interacts with dblp search API and returns all the retrieved URI's in a list form.

![frame2](https://cloud.githubusercontent.com/assets/25885525/23277669/677dd15e-fa17-11e6-9bf3-c7da68455475.png)
<br/>
By clicking submit the program will search for all conferences attended by the selected author and subsequently for the location where each conference was held and will return an html file with the map which will pop up in the user's browser.

![map_example](https://cloud.githubusercontent.com/assets/25885525/23277750/b80e3eba-fa17-11e6-8e48-1b97df0d83ca.PNG)

By dragging the mouse over a marker a list appears consisting of all the conferences held in the specified location:

![map_list](https://cloud.githubusercontent.com/assets/25885525/23278075/ecdb8066-fa18-11e6-8030-2436a9ba302f.png)

The *Search By Conference* Button in the Starting Frame opens the search by conference Frame, where the User can search for any conference by either its name or abbreviation in a manner similar to the one presented in search by author mode.

![search_by_conference](https://cloud.githubusercontent.com/assets/25885525/23278295/ae0c58a0-fa19-11e6-8e4d-99842d12ae12.PNG)

# Contents
dblp_search_and_draw_GUI_.py (main app) </br>
dbOps.py (includes all DB handling operations) </br>
dblpSD.db (db file. An instance is provided. In case it is deleted, it is created on next run.) </br>
mymap.html (Output file, which contains the final map. It is created after each run.)


# Various Info
This project was created by Evangelos Bousias-Alexakis and Aristotelis Kostoulas as part of the Contemporary Web Applications course of the Techno-Economic Systems Post-Graduate program run by the National Technical University of Athens. The project was supervised by Assistant Professor Ioannis Anagnostopoulos and PhD Candidate Gerasimos Razis, who we would like to thank for their guidance and support during project development.
