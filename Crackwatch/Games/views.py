from django.shortcuts import render
from django.db import connection

# Create your views here.
USERNAME = ""

def GameList(request, username):
    USERNAME = username
    cursor = connection.cursor()
    sql = "SELECT * FROM GAMES"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    dict_result = []

    for r in result:
        Name = r[1]
        Genre = r[2]
        Platform = r[3]
        GameID = r[0]
        row = {'Name':Name, 'Genre':Genre, 'Platform':Platform, 'GameID':GameID}
        dict_result.append(row)

    return render(request,'Games.html',{'games' : dict_result})
    #TemplateResponse(request, 'loginsuccess.html', { 'user': username})

def GameView(request, GameID, username):
    USERNAME = username

    cursor = connection.cursor()
    sql = "SELECT COUNT(1) FROM USER_FOLLOWS_G WHERE GAME_ID = " + str(GameID) + "  AND USERNAME = '" + USERNAME + "';"
    cursor.execute(sql)
    result = cursor.fetchall()
    AlreadyFollows = result[0][0]
    cursor.close()

    cursor = connection.cursor()
    sql = "SELECT COUNT(1) FROM USER_PLAYED WHERE GAME_ID = " + str(GameID) + "  AND USERNAME = '" + USERNAME + "';"
    cursor.execute(sql)
    result = cursor.fetchall()
    Already_Rated = result[0][0]
    cursor.close()

    if request.method=='POST':
        if 'Follow' in request.POST:
            if AlreadyFollows==0:
                cursor = connection.cursor()
                sql = "INSERT INTO USER_FOLLOWS_G VALUES('" + str(username) + "', " + str(GameID) + ");"
                cursor.execute(sql)
                cursor.close()
        elif 'Rate' in request.POST or 'rating' in request.POST:
            rating_given = request.POST['rating']
            if rating_given:
                if Already_Rated==1:
                    sql = "UPDATE USER_PLAYED SET RATING = " +str(rating_given) + " WHERE USERNAME = '" + str(username) + "' AND GAME_ID = " + str(GameID) + ";"
                else:
                    sql = "INSERT INTO USER_PLAYED VALUES('" + str(username) + "', " + str(GameID) + ", " + str(rating_given)  + ");"
                print(sql)
                cursor = connection.cursor()
                cursor.execute(sql)
                cursor.close()
    GAME_NAME = ""

    cursor = connection.cursor()
    sql = "SELECT COUNT(1) FROM USER_FOLLOWS_G WHERE GAME_ID = " + str(GameID) + "  AND USERNAME = '" + USERNAME + "';"
    cursor.execute(sql)
    result = cursor.fetchall()
    AlreadyFollows = result[0][0]
    cursor.close()

    cursor = connection.cursor()
    sql = "SELECT COUNT(1) FROM USER_PLAYED WHERE GAME_ID = " + str(GameID) + "  AND USERNAME = '" + USERNAME + "';"
    cursor.execute(sql)
    result = cursor.fetchall()
    Already_Rated = result[0][0]
    cursor.close()

    cursor = connection.cursor()
    sql = "SELECT GAME_ID, NAME, WIDE_IMAGE, CPU, GPU, RAM, TRAILER, DESCRIPTION FROM GAMES WHERE GAME_ID = " + str(GameID)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    #PLSQL FUNCTION CALL
    cursor = connection.cursor()
    followable = cursor.callfunc("CAN_USER_FOLLOW", int, [USERNAME])
    cursor.close()

    dict_result = []

    for r in result:
        GAME_NAME = r[1]
        GameId = r[0]
        Name = r[1]
        Image = r[2]
        CPU = r[3]
        if not CPU:
            CPU = "Not Available"
        GPU = r[4]
        if not GPU:
            GPU = "Not Available"
        RAM = r[5]
        if not RAM:
            RAM = "Not Available"
        Trailer = r[6]
        Description = r[7]


        Release = RetStrExecuteSQL("SELECT TO_CHAR(DATE_RELEASED, 'Mon dd, yyyy') FROM STUD_PUBLISHED WHERE GAME_ID = " + str(GameId))
        if not Release:
            Released = "Date Not Available"
        else:
            Released = Release[0][0]

        Cracked = RetStrExecuteSQL("SELECT TO_CHAR(CRACKED_DATE, 'Mon dd, yyyy') FROM CRACKED_GAME WHERE GAME_ID =" + str(GameId))
        if not Cracked:
            CrackDate = "Date Not Available"
        else:
            CrackDate = Cracked[0][0]

        Prt = RetStrExecuteSQL("SELECT NAME FROM ENCRYPTED, PROTECTION WHERE ENCRYPTED.PRT_ID = PROTECTION.PRT_ID AND ENCRYPTED.GAME_ID =" + str(GameId))
        if not Prt:
            Protection = "No-DRM"
        else:
            Protection = Prt[0][0]
        PRT = RetStrExecuteSQL("SELECT PRT_ID FROM ENCRYPTED WHERE GAME_ID = " + str(GameId))
        if not PRT:
            PRT_ID = 1
        else:
            PRT_ID = PRT[0][0]

        StudioDev = RetStrExecuteSQL("SELECT NAME FROM STUDIO, STUD_DEVELOPED WHERE STUD_DEVELOPED.STD_ID = STUDIO.STD_ID AND STUD_DEVELOPED.GAME_ID = " + str(GameId))
        if not StudioDev:
            StudioDeveloped = "Not Available"
        else:
            StudioDeveloped = StudioDev[0][0]
        Stud_Dev_ID = RetStrExecuteSQL("SELECT STD_ID FROM STUD_DEVELOPED WHERE GAME_ID = " + str(GameId))
        if not Stud_Dev_ID:
            Dev_Id = -1
        else:
            Dev_Id = Stud_Dev_ID[0][0]

        StudioPub = RetStrExecuteSQL("SELECT NAME FROM STUDIO, STUD_PUBLISHED WHERE STUD_PUBLISHED.STD_ID = STUDIO.STD_ID AND STUD_PUBLISHED.GAME_ID = " + str(GameId))
        if not StudioPub:
            StudioPublished = "Not Available"
        else:
            StudioPublished = StudioPub[0][0]
        Stud_Pub_ID = RetStrExecuteSQL("SELECT STD_ID FROM STUD_PUBLISHED WHERE GAME_ID = " + str(GameId))
        if not Stud_Pub_ID:
            Pub_ID = -1
        else:
            Pub_ID = Stud_Pub_ID[0][0]

        Group = RetStrExecuteSQL("SELECT CRACK_GROUPS.NAME FROM CRACK_GROUPS, CRACKED_GAME WHERE CRACK_GROUPS.GROUP_ID = CRACKED_GAME.GROUP_ID AND CRACKED_GAME.GAME_ID = " + str(GameId) + " AND ROWNUM = 1 ORDER BY CRACKED_GAME.CRACKED_DATE ASC;")
        if not Group:
            SceneGroup = "Not Available"
        else:
            SceneGroup = Group[0][0]
        CG_ID = RetStrExecuteSQL("SELECT GROUP_ID FROM CRACKED_GAME WHERE GAME_ID = " + str(GameId))
        if not CG_ID:
            GROUP_ID = -1
        else:
            GROUP_ID = CG_ID[0][0]

        TotalCracks = RetIntExecuteSQL("SELECT COUNT(*) FROM CRACKED_GAME WHERE GAME_ID =" + str(GameId))

        Price = RetIntExecuteSQL("SELECT NVL(MIN(PRICE), -1) FROM AVAILABLE_AT WHERE GAME_ID = " + str(GameId))
        if Price < 0:
            BestPrice = "N/A"
        else:
            BestPrice = "$" + str(Price)

        Rate = RetStrExecuteSQL("SELECT NVL(TO_CHAR(AVG(RATING)), '-') FROM USER_PLAYED WHERE GAME_ID = " + str(GameId))
        if not Rate:
            Rating = "-"
        else:
            Rating = str(Rate[0][0]) + "/5"

        Followers = RetIntExecuteSQL("SELECT COUNT(*) FROM USER_FOLLOWS_G WHERE GAME_ID = " + str(GameId))

        cursor = connection.cursor()
        condition = 0
        Days = 0
        procedure_retval = cursor.callproc('GAME_STATUS', [r[0], Days, condition])
        Days = procedure_retval[1]
        condition = procedure_retval[2]
        CrackInfo = ""
        CrackStat = ""
        if condition == 1:
            CrackStat = "Cracked"
            CrackInfo = "D+" + str(Days)
        elif condition == 2:
            CrackStat = "Uncracked"
            CrackInfo = "D+" + str(Days)
        elif condition == 3:
            CrackStat = "Unreleased"
            CrackInfo = "D-" + str(Days)
        else:
            CrackStat = "Not Available"
            CrackInfo = "N/A"
        row = {'Name':Name, 'Image':Image, 'Released':Released, 'GameID':GameId, 'CrackDate':CrackDate, 'Protection':Protection, 'StudioDeveloped':StudioDeveloped, 'SceneGroup':SceneGroup, 'TotalCracks':TotalCracks, 'BestPrice':BestPrice, 'Rating':Rating, 'Followers':Followers, 'CrackInfo': CrackInfo, 'Condition': condition, 'Stud_Dev_ID': Dev_Id, 'PRT_ID': PRT_ID, 'GROUP_ID': GROUP_ID, 'CrackStat': CrackStat, 'CPU': CPU, 'GPU' : GPU, 'RAM' : RAM, 'Trailer' : Trailer, 'Description' : Description, 'StudioPublished': StudioPublished, 'Pub_ID' : Pub_ID}

        dict_result.append(row)

    cursor = connection.cursor()
    sql = "SELECT A.PRICE, M.NAME, M.MARKET_ID FROM AVAILABLE_AT A, MARKETPLACE M WHERE A.GAME_ID = " + str(GameID) + " AND M.MARKET_ID = A.MARKET_ID ORDER BY A.PRICE ASC;"
    total_selected = 0
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    markets = []
    for r in result:
        Price = "$" + str(r[0])
        Place = r[1]
        ID = r[2]
        row = {'Market': Place, 'Price' : Price, 'ID': ID}
        markets.append(row)
        total_selected = total_selected + 1
        if total_selected >= 3:
            break

    cursor = connection.cursor()
    sql = "SELECT RATING FROM USER_PLAYED WHERE GAME_ID = " + str(GameID) + "  AND USERNAME = '" + USERNAME + "';"
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        UserRating = str(result[0][0])
    else:
        UserRating = "-"
    cursor.close()

    cursor = connection.cursor()
    sql = "SELECT C.NAME, C.GROUP_ID FROM CRACK_GROUPS C, CRACKED_GAME CG WHERE CG.GAME_ID = " + str(GameID) + " AND C.GROUP_ID = CG.GROUP_ID;"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    Crackers = []
    if not result:
        row = {'Cracker': "No Group Yet", 'ID' : -1}
        Crackers.append(row)
    else:
        for r in result:
            row = {'Cracker': r[0], 'ID': r[1]}
            Crackers.append(row)
    print(Crackers)

    return render(request,'GamePage.html',{'games' : dict_result, 'followable' : followable, 'Name' : GAME_NAME, 'username': USERNAME, 'markets': markets, 'AlreadyFollows': AlreadyFollows, 'Already_Rated': Already_Rated, 'UserRating': UserRating, 'Crackers': Crackers})


def AllGames(request, username):
    USERNAME = username
    cursor = connection.cursor()
    if request.method=='POST':
        title = request.POST['title']
        crackedornot = request.POST['crackstatus']
        releasedornot = request.POST['releasedstatus']
        genre = request.POST['genre']
        sql = "SELECT G.GAME_ID, G.NAME, G.IMAGE FROM GAMES G WHERE "
        UseAnd = False
        if title:
            sql = sql + "LOWER(G.NAME) LIKE '%" + str(title).lower() + "%'"
            UseAnd = True
        if not crackedornot=='0':
            if UseAnd:
                sql = sql + " AND "
            if crackedornot=='1':
                sql = sql + "EXISTS(SELECT * FROM CRACKED_GAME WHERE GAME_ID = G.GAME_ID)"
            else:
                sql = sql + "NOT EXISTS(SELECT * FROM CRACKED_GAME WHERE GAME_ID = G.GAME_ID)"
            UseAnd = True
        if not releasedornot=='0':
            if UseAnd:
                sql = sql + " AND "
            if releasedornot=='1':
                sql = sql + "EXISTS(SELECT * FROM STUD_PUBLISHED WHERE GAME_ID = G.GAME_ID AND DATE_RELEASED < SYSDATE)"
            else:
                sql = sql + "EXISTS(SELECT * FROM STUD_PUBLISHED WHERE GAME_ID = G.GAME_ID AND DATE_RELEASED > SYSDATE)"
        if genre:
            if UseAnd:
                sql = sql + " AND "
            sql = sql + "LOWER(G.GENRE) LIKE '%" + str(genre).lower() + "%'"
        if not title and not genre and crackedornot=='0' and releasedornot=='0':
            sql = "SELECT GAME_ID, NAME, IMAGE FROM GAMES"
    else:
        sql = "SELECT GAME_ID, NAME, IMAGE FROM GAMES"

    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    dict_result = []
    total_games = 0
    for r in result:
        total_games = total_games + 1
        GameId = r[0]
        Name = r[1]
        Image = r[2]


        Release = RetStrExecuteSQL("SELECT TO_CHAR(DATE_RELEASED, 'Mon dd, yyyy') FROM STUD_PUBLISHED WHERE GAME_ID = " + str(GameId))
        if not Release:
            Released = "-"
        else:
            Released = Release[0][0]

        Cracked = RetStrExecuteSQL("SELECT TO_CHAR(CRACKED_DATE, 'Mon dd, yyyy') FROM CRACKED_GAME WHERE GAME_ID =" + str(GameId))
        if not Cracked:
            CrackDate = "-"
        else:
            CrackDate = Cracked[0][0]

        Prt = RetStrExecuteSQL("SELECT NAME FROM ENCRYPTED, PROTECTION WHERE ENCRYPTED.PRT_ID = PROTECTION.PRT_ID AND ENCRYPTED.GAME_ID =" + str(GameId))
        if not Prt:
            Protection = "No-DRM"
        else:
            Protection = Prt[0][0]
        PRT = RetStrExecuteSQL("SELECT PRT_ID FROM ENCRYPTED WHERE GAME_ID = " + str(GameId))
        if not PRT:
            PRT_ID = 1
        else:
            PRT_ID = PRT[0][0]

        StudioDev = RetStrExecuteSQL("SELECT NAME FROM STUDIO, STUD_DEVELOPED WHERE STUD_DEVELOPED.STD_ID = STUDIO.STD_ID AND STUD_DEVELOPED.GAME_ID = " + str(GameId))
        if not StudioDev:
            StudioDeveloped = "-"
        else:
            StudioDeveloped = StudioDev[0][0]
        Stud_Dev_ID = RetStrExecuteSQL("SELECT STD_ID FROM STUD_DEVELOPED WHERE GAME_ID = " + str(GameId))
        if not Stud_Dev_ID:
            Dev_Id = -1
        else:
            Dev_Id = Stud_Dev_ID[0][0]

        Group = RetStrExecuteSQL("SELECT CRACK_GROUPS.NAME FROM CRACK_GROUPS, CRACKED_GAME WHERE CRACK_GROUPS.GROUP_ID = CRACKED_GAME.GROUP_ID AND CRACKED_GAME.GAME_ID = " + str(GameId) + " AND ROWNUM = 1 ORDER BY CRACKED_GAME.CRACKED_DATE ASC;")
        if not Group:
            SceneGroup = "-"
        else:
            SceneGroup = Group[0][0]
        CG_ID = RetStrExecuteSQL("SELECT GROUP_ID FROM CRACKED_GAME WHERE GAME_ID = " + str(GameId))
        if not CG_ID:
            GROUP_ID = -1
        else:
            GROUP_ID = CG_ID[0][0]

        TotalCracks = RetIntExecuteSQL("SELECT COUNT(*) FROM CRACKED_GAME WHERE GAME_ID =" + str(GameId))

        Price = RetIntExecuteSQL("SELECT NVL(MIN(PRICE), -1) FROM AVAILABLE_AT WHERE GAME_ID = " + str(GameId))
        if Price < 0:
            BestPrice = "N/A"
        else:
            BestPrice = "$" + str(Price)

        Rate = RetStrExecuteSQL("SELECT NVL(TO_CHAR(AVG(RATING)), '-') FROM USER_PLAYED WHERE GAME_ID = " + str(GameId))
        if not Rate:
            Rating = "-"
        else:
            Rating = str(Rate[0][0]) + "/5"

        Followers = RetIntExecuteSQL("SELECT COUNT(*) FROM USER_FOLLOWS_G WHERE GAME_ID = " + str(GameId))

        cursor = connection.cursor()
        condition = 0
        Days = 0
        procedure_retval = cursor.callproc('GAME_STATUS', [r[0], Days, condition])
        Days = procedure_retval[1]
        condition = procedure_retval[2]
        CrackInfo = ""
        if condition == 1:
            CrackInfo = "Cracked D+" + str(Days)
        elif condition == 2:
            CrackInfo = "Uncracked D+" + str(Days)
        elif condition == 3:
            CrackInfo = "Unreleased D-" + str(Days)
        else:
            CrackInfo = "No Date Informations"
        row = {'Name':Name, 'Image':Image, 'Released':Released, 'GameID':GameId, 'CrackDate':CrackDate, 'Protection':Protection, 'StudioDeveloped':StudioDeveloped, 'SceneGroup':SceneGroup, 'TotalCracks':TotalCracks, 'BestPrice':BestPrice, 'Rating':Rating, 'Followers':Followers, 'CrackInfo': CrackInfo, 'Condition': condition, 'Stud_Dev_ID': Dev_Id, 'PRT_ID': PRT_ID, 'GROUP_ID': GROUP_ID}

        dict_result.append(row)

    return render(request,'AllGames.html',{'games' : dict_result, 'username': USERNAME, 'total': total_games })


def RetStrExecuteSQL(Query):
    cursor = connection.cursor()
    cursor.execute(Query)
    result = cursor.fetchall()
    if not result:
        retval = ""
    else:
        retval = result[0][0]
    return result


def RetIntExecuteSQL(Query):
    cursor = connection.cursor()
    cursor.execute(Query)
    result = cursor.fetchall()
    cursor.close()
    return result[0][0]
