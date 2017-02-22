import sqlite3


createDb = sqlite3.connect('dblpSD.db')


def create_tables():
    query_curs = createDb.cursor()
    query_curs.execute('''CREATE TABLE IF NOT EXISTS Persons
    (url TEXT PRIMARY KEY, Surname TEXT, Name TEXT, ConfCount INTEGER, UNIQUE(Surname, Name))''')
    query_curs.execute('''CREATE TABLE IF NOT EXISTS Conferences
    (id INTEGER PRIMARY KEY, ConfTitle TEXT, Year INTEGER, id_location INTEGER, UNIQUE(ConfTitle, Year))''')
    query_curs.execute('''CREATE TABLE IF NOT EXISTS Locations
    (id INTEGER PRIMARY KEY, Location TEXT,Latitude DECIMAL(9,6), Longitude DECIMAL(8,6), UNIQUE(Location))''')
    query_curs.execute('''CREATE TABLE IF NOT EXISTS Participations
    (id INTEGER PRIMARY KEY, id_Person TEXT, id_Conf INTEGER, FOREIGN KEY(id_Person) REFERENCES Persons(url),
    FOREIGN KEY(id_Conf) REFERENCES Conferences(id), UNIQUE(id_Person, id_Conf))''')
    query_curs.close()


def get_info_for_map(id_acc):
    createDb.text_factory = str
    query_curs = createDb.cursor()
    query_curs.execute('''SELECT Loc.Latitude, Loc.Longitude, Loc.Location, Con.ConfTitle,Con.Year
    FROM Participations Par
    JOIN Persons Per on Par.id_Person = Per.url
    JOIN Conferences Con on Par.id_Conf = Con.id
    JOIN Locations Loc on Con.id_location = Loc.id
    WHERE Per.url = ?''', (id_acc,))
    res = query_curs.fetchall()
    query_curs.close()
    return res

##Start of Changes- Method for Search Based On Conference

def get_coord_from_DB(location):
    query_curs = createDb.cursor()
    query_curs.execute('''SELECT Loc.Latitude, Loc.Longitude FROM Locations Loc
    WHERE Loc.Location=?''', (location,))
    res = query_curs.fetchall()
    query_curs.close()
    return res

##End Of Changes
def add_person(url,surname, name):
    query_curs = createDb.cursor()
    query_curs.execute('''INSERT OR IGNORE INTO Persons (url,Surname,Name,ConfCount)
    VALUES (?,?, ?,0)''', (url,surname, name))
    result = query_curs.rowcount  # 0:IGNORED, no lines inserted - 1:OK
    createDb.commit()
    query_curs.close()
    return result


def add_conference(title, year):
    query_curs = createDb.cursor()
    query_curs.execute('''INSERT OR IGNORE INTO Conferences (ConfTitle,Year,id_location)
    VALUES (?,?,null)''', (title, year))
    result = query_curs.rowcount
    createDb.commit()
    query_curs.close()
    return result


def add_location(loc, lat, lon):
    query_curs = createDb.cursor()
    query_curs.execute('''INSERT OR IGNORE INTO Locations (Location,Latitude,Longitude)
    VALUES (?,?,?)''', (loc, lat, lon))
    result = query_curs.rowcount
    createDb.commit()
    query_curs.close()
    return result


def add_participation(id_person, id_conf):
    query_curs = createDb.cursor()
    query_curs.execute('''INSERT OR IGNORE INTO Participations (id_Person, id_Conf)
    VALUES (?,?)''', (id_person, id_conf))
    result = query_curs.rowcount
    createDb.commit()
    query_curs.close()
    return result


def update_conf(title, year, loc):
    query_curs = createDb.cursor()
    query_curs.execute('''UPDATE Conferences
    SET id_location = (SELECT id FROM Locations WHERE Location = ?)
    WHERE id_location is null
    AND ConfTitle = ?
    AND Year = ?''', (loc, title, year))
    createDb.commit()
    query_curs.close()


def update_dbcnr(author_id):
    query_curs = createDb.cursor()
    query_curs.execute('''UPDATE Persons
    SET ConfCount = (SELECT COUNT(*) FROM Participations WHERE id_Person = ?)
    WHERE url = ?''', (author_id, author_id))
    createDb.commit()
    query_curs.close()


def drop_table(table_name):
    query_curs = createDb.cursor()
    query_curs.execute('''DROP TABLE ''' + table_name)
    query_curs.close()


def check_author_id(url): #changed it to follow url instead of id 
    query_curs = createDb.cursor()
    query_curs.execute('''SELECT url FROM Persons
    WHERE url=?''', (url,))
    res = query_curs.fetchall()
    if len(res) == 0:
        result = False
    else:
        result = True
    query_curs.close()
    return result


def get_conf_id(title, year):
    query_curs = createDb.cursor()
    query_curs.execute('''SELECT id FROM Conferences
    WHERE ConfTitle = ? and Year = ?''', (title, year))
    result = int(query_curs.fetchone()[0])
    query_curs.close()
    return result


def check_if_conf_exists(title, year):
    query_curs = createDb.cursor()
    query_curs.execute('''SELECT id FROM Conferences
    WHERE ConfTitle = ? and Year = ?''', (title, year))
    res = query_curs.fetchall()
    if len(res) == 0:
        result = 0
    else:
        result = res[0][0]
    query_curs.close()
    return result


def check_if_loc_exists(location):
    createDb.text_factory = str
    query_curs = createDb.cursor()
    query_curs.execute('''SELECT id FROM Locations
    WHERE Location = ?''', (location, ))
    res = query_curs.fetchall()
    if len(res) == 0:
        result = 0
    else:
        result = res[0][0]
    query_curs.close()
    return result


def get_dbcnr(id_acc):
    query_curs = createDb.cursor()
    query_curs.execute('''SELECT ConfCount FROM Persons
    WHERE url = ?''', (id_acc,))
    result = int(query_curs.fetchone()[0])
    query_curs.close()
    return result


def test_select(table_name):
    query_curs = createDb.cursor()
    query_curs.execute('''SELECT * FROM ''' + table_name)
    k = 0

    for i in query_curs:
        print ("\n")
        for j in i:
            print (j)
            if k < 5:
                k += 1
            else:
                k = 0
    query_curs.close()
