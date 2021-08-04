from django.shortcuts import render
from django.db import connection
import math
# Create your views here.

USERNAME = ""

def AllCrackGroups(request, username):
    USERNAME = username
    cursor = connection.cursor()
    sql = "SELECT GROUP_ID, NAME, NVL(URL, 'nourl'), LOGO FROM CRACK_GROUPS;"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    total_groups = 0
    dict_result = []
    for r in result:
        Name = r[1]
        URL = r[2]
        CGID = r[0]
        LOGO = r[3]
        TotalCracksDone = RetIntExecuteSQL("SELECT COUNT(*) FROM CRACKED_GAME WHERE GROUP_ID =" + str(CGID) + ";")
        if TotalCracksDone==0:
            LatestGameId = -1
            LatestGameName = ""
            LatestGameImage = ""
        else:
            LatestGameId = RetIntExecuteSQL("SELECT * FROM CRACKED_GAME WHERE GROUP_ID =" + str(CGID) + " AND ROWNUM = 1 ORDER BY CRACKED_DATE DESC;")
            LatestGameName = RetStrExecuteSQL("SELECT NAME FROM GAMES WHERE GAME_ID = " + str(LatestGameId) + ";")
            LatestGameImage = RetStrExecuteSQL("SELECT IMAGE FROM GAMES WHERE GAME_ID = " + str(LatestGameId) + ";")
        TotalFollowers = RetIntExecuteSQL("SELECT COUNT(*) FROM USER_FOLLOWS_C WHERE GROUP_ID =" + str(CGID) + ";")
        row = {'Name':Name, 'URL':URL,'CGID':CGID, 'LOGO': LOGO, 'TotalCracks': TotalCracksDone, 'LatestGameId': LatestGameId, 'LatestGameName': LatestGameName, 'LatestGameImage': LatestGameImage, 'TotalFollowers': TotalFollowers}
        dict_result.append(row)
        total_groups = total_groups + 1
    return render(request,'AllCrackGroups.html',{'CGs' : dict_result, 'username': username, 'total': total_groups})

def CGView(request, CGID, username):
    USERNAME = username

    AlreadyFollowsGroup = RetIntExecuteSQL("SELECT COUNT(1) FROM USER_FOLLOWS_C WHERE GROUP_ID = " + str(CGID) + " AND USERNAME = '" + str(username) + "';")

    if request.method=='POST':
        if AlreadyFollowsGroup==0:
            print("Does Not Follow Yet")
            cursor = connection.cursor()
            sql = "INSERT INTO USER_FOLLOWS_C VALUES('" + str(username) + "', " + str(CGID) + ");"
            cursor.execute(sql)
            cursor.close()

    GROUP_NAME = ""
    cursor = connection.cursor()
    AlreadyFollowsGroup = RetIntExecuteSQL("SELECT COUNT(1) FROM USER_FOLLOWS_C WHERE GROUP_ID = " + str(CGID) + " AND USERNAME = '" + str(username) + "';")
    sql = "SELECT GROUP_ID, NAME, NVL(URL, 'nourl'), LOGO, DESCRIPTION FROM CRACK_GROUPS WHERE GROUP_ID = " + str(CGID)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    dict_result = []
    for r in result:
        Name = r[1]
        GROUP_NAME = Name
        URL = r[2]
        CGID = r[0]
        LOGO = r[3]
        DESCRIPTION = r[4]
        row = {'Name':Name, 'URL':URL,'CGID':CGID, 'LOGO' : LOGO, 'DESCRIPTION': DESCRIPTION}
        dict_result.append(row)

    Followers = RetIntExecuteSQL("SELECT COUNT(*) FROM USER_FOLLOWS_C WHERE GROUP_ID = " + str(CGID) + ";")

    cursor = connection.cursor()
    sql = "SELECT G.GAME_ID, G.NAME, G.WIDE_IMAGE FROM GAMES G, CRACKED_GAME C WHERE  C.GROUP_ID = " + str(CGID) + " AND C.GAME_ID = G.GAME_ID;"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    AllCrackedGames = []
    for r in result:
        GameID = r[0]
        Name = r[1]
        Image = r[2]
        row = {'ID': GameID, 'Name': Name, 'Image': Image}
        AllCrackedGames.append(row)

    return render(request,'CGPage.html',{'CGs' : dict_result, 'username': username, 'Group': GROUP_NAME, 'Followers':Followers, 'AllCrackedGames': AllCrackedGames, 'AlreadyFollowsGroup': AlreadyFollowsGroup})


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
