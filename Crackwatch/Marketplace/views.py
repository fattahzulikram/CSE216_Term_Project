from django.shortcuts import render
from django.db import connection

# Create your views here.
USERNAME = ""
def AllMarketplaces(request, username):
    USERNAME = username
    cursor = connection.cursor()
    sql = "SELECT MARKET_ID, NAME, LOGO, URL FROM MARKETPLACE;"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    total_markets = 0
    dict_result = []
    for r in result:
        Name = r[1]
        ID = r[0]
        LOGO = r[2]
        URL = r[3]
        TotalGames = RetIntExecuteSQL("SELECT COUNT(*) FROM AVAILABLE_AT WHERE MARKET_ID =" + str(ID) + ";")

        row = {'Name':Name, 'ID':ID, 'LOGO': LOGO, 'URL': URL, 'TotalGames': TotalGames}
        dict_result.append(row)
        total_markets = total_markets + 1
    return render(request,'AllMarkets.html',{'Markets' : dict_result, 'username': username, 'TotalMarkets': total_markets})

def MarketView(request, MarketID, username):
    USERNAME = username
    MARKET_NAME = ""
    cursor = connection.cursor()
    sql = "SELECT NAME, LOGO, URL, DESCRIPTION FROM MARKETPLACE WHERE MARKET_ID = " + str(MarketID)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    dict_result = []
    for r in result:
        Name = r[0]
        MARKET_NAME = Name
        URL = r[2]
        LOGO = r[1]
        Description = r[3]
        row = {'Name':Name, 'URL':URL,'LOGO':LOGO, 'Description': Description}
        dict_result.append(row)

    cursor = connection.cursor()
    sql = "SELECT G.GAME_ID, G.NAME, G.WIDE_IMAGE FROM GAMES G, AVAILABLE_AT A WHERE  A.MARKET_ID = " + str(MarketID) + " AND A.GAME_ID = G.GAME_ID;"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    total_available = 0
    AllAvailableGames = []
    for r in result:
        GameID = r[0]
        Name = r[1]
        Image = r[2]
        row = {'ID': GameID, 'Name': Name, 'Image': Image}
        AllAvailableGames.append(row)
        total_available = total_available + 1
    return render(request,'MarketPage.html',{'Markets' : dict_result, 'username': username, 'MARKET_NAME': MARKET_NAME, 'AllAvailableGames': AllAvailableGames, 'TotalAvailable': total_available})

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
