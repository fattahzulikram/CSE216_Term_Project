from django.shortcuts import render
from django.db import connection
import datetime
# Create your views here.

USERNAME = ""
def AllStudios(request, username):
    USERNAME = username
    cursor = connection.cursor()
    sql = "SELECT STD_ID, NAME, EST_YEAR, LOGO FROM STUDIO;"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    total_studios = 0
    dict_result = []
    for r in result:
        Name = r[1]
        Year = r[2]
        EST_YEAR = Year.strftime("%B %d, %Y")
        ID = r[0]
        LOGO = r[3]
        TotalGamesDev = RetIntExecuteSQL("SELECT COUNT(*) FROM STUD_DEVELOPED WHERE STD_ID =" + str(ID) + ";")
        TotalGamesPub = RetIntExecuteSQL("SELECT COUNT(*) FROM STUD_PUBLISHED WHERE STD_ID =" + str(ID) + ";")
        Total = TotalGamesDev+TotalGamesPub

        cursor = connection.cursor()
        sql = "SELECT G.GAME_ID, G.NAME, G.IMAGE, STP.DATE_RELEASED FROM GAMES G, (SELECT * FROM STUD_PUBLISHED ORDER BY DATE_RELEASED ASC) STP WHERE G.GAME_ID = STP.GAME_ID AND STP.STD_ID = " + str(ID) + " AND ROWNUM = 1 ORDER BY STP.DATE_RELEASED ASC;"
        cursor.execute(sql)
        values = cursor.fetchall()
        cursor.close()

        LatestGameID = -1
        LatestGameName = ""
        LatestGameImage = ""
        LatestGameDate = datetime.datetime.now()
        if not TotalGamesPub==0:
            print(Name + " Pub " + str(values[0][3]))
            LatestGameID = values[0][0]
            LatestGameName = values[0][1]
            LatestGameImage = values[0][2]
            LatestGameDate = values[0][3]

        cursor = connection.cursor()
        sql = "SELECT G.GAME_ID, G.NAME, G.IMAGE, STP.DATE_RELEASED FROM GAMES G, STUD_DEVELOPED STD, (SELECT * FROM STUD_PUBLISHED ORDER BY DATE_RELEASED ASC) STP WHERE G.GAME_ID = STD.GAME_ID AND G.GAME_ID = STP.GAME_ID AND STD.STD_ID = " + str(ID) + " AND ROWNUM = 1 ORDER BY STP.DATE_RELEASED ASC;"
        cursor.execute(sql)
        values = cursor.fetchall()
        cursor.close()

        if (not TotalGamesDev==0) and values[0][3] < LatestGameDate:
            print(Name + " Dev " + str(values[0][3]))
            LatestGameID = values[0][0]
            LatestGameName = values[0][1]
            LatestGameImage = values[0][2]
            LatestGameDate = values[0][3]

        row = {'Name':Name, 'EST_YEAR':EST_YEAR,'ID':ID, 'LOGO': LOGO, 'TotalGamesPub': TotalGamesPub, 'TotalGamesDev': TotalGamesDev, 'LatestGameID': LatestGameID, 'LatestGameName': LatestGameName, 'LatestGameImage': LatestGameImage, 'TotalGames': Total}
        dict_result.append(row)
        total_studios = total_studios + 1
    return render(request,'AllStudios.html',{'Studios' : dict_result, 'username': username, 'total': total_studios})


def StudioView(request, StudioID, username):
    cursor = connection.cursor()
    STUDIO =""
    sql = "SELECT * FROM STUDIO WHERE STD_ID = " + str(StudioID)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    dict_result = []
    for r in result:
        Name = r[1]
        STUDIO = Name
        Year = r[2]
        EST_YEAR = Year.strftime("%B %d, %Y")
        Logo = r[3]
        Description = r[4]

        row = {'Name':Name, 'Year':EST_YEAR,'LOGO':Logo, 'Description' : Description}
        dict_result.append(row)

    TotalGamesDeveloped = 0
    TotalGamesPublished = 0
    cursor = connection.cursor()
    sql = "SELECT G.GAME_ID, G.NAME, G.WIDE_IMAGE FROM GAMES G, STUD_DEVELOPED STD WHERE G.GAME_ID = STD.GAME_ID AND STD.STD_ID = " + str(StudioID) + ";"
    cursor.execute(sql)
    result = cursor.fetchall()
    AllGamesDeveloped = []
    for r in result:
        GameID = r[0]
        GameName = r[1]
        GameImage = r[2]
        row = {'GID': GameID, 'GName': GameName, 'GImage': GameImage}
        AllGamesDeveloped.append(row)
        TotalGamesDeveloped = TotalGamesDeveloped + 1

    cursor = connection.cursor()
    sql = "SELECT G.GAME_ID, G.NAME, G.WIDE_IMAGE FROM GAMES G, STUD_PUBLISHED STP WHERE G.GAME_ID = STP.GAME_ID AND STP.STD_ID = " + str(StudioID) + ";"
    cursor.execute(sql)
    result = cursor.fetchall()
    AllGamesPublished = []
    for r in result:
        GameID = r[0]
        GameName = r[1]
        GameImage = r[2]
        row = {'GID': GameID, 'GName': GameName, 'GImage': GameImage}
        AllGamesPublished.append(row)
        TotalGamesPublished = TotalGamesPublished + 1

    return render(request,'StudioPage.html',{'Studios' : dict_result, 'username' : username, 'Studio': STUDIO, 'TotalDeveloped': TotalGamesDeveloped, 'Developed': AllGamesDeveloped, 'TotalPublished': TotalGamesPublished, 'Published': AllGamesPublished})


def RetStrExecuteSQL(Query):
    cursor = connection.cursor()
    cursor.execute(Query)
    result = cursor.fetchall()
    if not result:
        retval = ""
    else:
        retval = result[0][0]
    return retval


def RetIntExecuteSQL(Query):
    cursor = connection.cursor()
    cursor.execute(Query)
    result = cursor.fetchall()
    cursor.close()
    return result[0][0]
