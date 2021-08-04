from django.shortcuts import render
from django.db import connection
# Create your views here.

USERNAME = ""
def AllProtections(request, username):
    USERNAME = username
    cursor = connection.cursor()
    sql = "SELECT PRT_ID, NAME, LOGO, COMPANY FROM PROTECTION;"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    total_drms = 0
    dict_result = []
    for r in result:
        Name = r[1]
        ID = r[0]
        LOGO = r[2]
        Company = r[3]
        TotalDRMDone = RetIntExecuteSQL("SELECT COUNT(*) FROM ENCRYPTED WHERE PRT_ID =" + str(ID) + ";")
        if TotalDRMDone==0:
            LatestGameId = -1
            LatestGameName = ""
            LatestGameImage = ""
        else:
            LatestGameId = RetIntExecuteSQL("SELECT E.GAME_ID FROM ENCRYPTED E, (SELECT * FROM STUD_PUBLISHED ORDER BY DATE_RELEASED DESC) STP WHERE E.GAME_ID = STP.GAME_ID AND PRT_ID = " + str(ID) + " AND ROWNUM = 1 ORDER BY STP.DATE_RELEASED DESC;")
            LatestGameName = RetStrExecuteSQL("SELECT NAME FROM GAMES WHERE GAME_ID = " + str(LatestGameId) + ";")
            LatestGameImage = RetStrExecuteSQL("SELECT IMAGE FROM GAMES WHERE GAME_ID = " + str(LatestGameId) + ";")

        row = {'Name':Name, 'ID':ID, 'LOGO': LOGO, 'Company': Company, 'TotalDRMDone': TotalDRMDone, 'LatestGameId': LatestGameId, 'LatestGameName': LatestGameName, 'LatestGameImage': LatestGameImage}
        dict_result.append(row)
        total_drms = total_drms + 1
    return render(request,'AllProtection.html',{'DRMS' : dict_result, 'username': USERNAME, 'TotalDRMS': total_drms})

def ProtectionView(request, ProtectionID, username):
    USERNAME = username
    PRT_NAME = ""
    cursor = connection.cursor()
    sql = "SELECT NAME, LOGO, COMPANY, YEAR, DESCRIPTION FROM PROTECTION WHERE PRT_ID = " + str(ProtectionID)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    dict_result = []
    for r in result:
        Name = r[0]
        PRT_NAME = Name
        LOGO = r[1]
        Company = r[2]
        Year = r[3]
        DESCRIPTION = r[4]
        row = {'Name':Name, 'Year':Year, 'Company':Company, 'LOGO':LOGO, 'DESCRIPTION': DESCRIPTION}
        dict_result.append(row)

    cursor = connection.cursor()
    sql = "SELECT G.GAME_ID, G.NAME, G.WIDE_IMAGE FROM GAMES G, ENCRYPTED E WHERE  E.PRT_ID = " + str(ProtectionID) + " AND E.GAME_ID = G.GAME_ID;"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    total_protected = 0
    AllProtectedGames = []
    for r in result:
        GameID = r[0]
        Name = r[1]
        Image = r[2]
        row = {'ID': GameID, 'Name': Name, 'Image': Image}
        AllProtectedGames.append(row)
        total_protected = total_protected + 1
    return render(request,'ProtectionPage.html',{'DRMS' : dict_result, 'PRT_NAME': PRT_NAME, 'username': username, 'AllProtectedGames': AllProtectedGames, 'TotalGames': total_protected})


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
