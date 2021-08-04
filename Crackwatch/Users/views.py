from django.shortcuts import render,redirect
from django.db import connection
from django.template.response import TemplateResponse

# Create your views here.
USERNAME = ""

def UsersView(request, user):
    USERNAME = user
    AllUsers = request.session.get('username')
    print(AllUsers)
    if AllUsers is not None and USERNAME in AllUsers:
        #Latest Crack Games
        cursor = connection.cursor()
        sql = "SELECT GAMES.NAME, TO_CHAR(CRACKED_GAME.CRACKED_DATE, 'Mon dd, yyyy'), GAMES.GAME_ID FROM GAMES, CRACKED_GAME WHERE CRACKED_GAME.GAME_ID = GAMES.GAME_ID AND ROWNUM <= 5 ORDER BY CRACKED_DATE DESC;"
        cursor.execute(sql)
        result = cursor.fetchall()

        latest_cracked_games = []

        for r in result:
            Name = r[0]
            Date = r[1]
            ID = r[2]
            row = {'Name':Name, 'Date':Date, 'ID':ID}
            latest_cracked_games.append(row)

        #User Follows Games
        cursor = connection.cursor()
        sql = "SELECT GAMES.GAME_ID,GAMES.NAME,STUDIO.NAME FROM USER_FOLLOWS_G,GAMES,STUD_DEVELOPED,STUDIO WHERE USERNAME ='" + USERNAME + "' AND USER_FOLLOWS_G.GAME_ID=GAMES.GAME_ID AND STUD_DEVELOPED.GAME_ID = GAMES.GAME_ID AND STUDIO.STD_ID = STUD_DEVELOPED.STD_ID;"
        cursor.execute(sql)
        result = cursor.fetchall()

        user_follows_g = []

        for r in result:
            ID = r[0]
            Name = r[1]
            Studio = r[2]
            row = {'ID':ID, 'Name':Name, 'Studio':Studio}
            user_follows_g.append(row)

        #User Played
        cursor = connection.cursor()
        sql = "SELECT GAMES.GAME_ID,GAMES.NAME, USER_PLAYED.RATING FROM USER_PLAYED,GAMES WHERE USERNAME = '" + USERNAME + "' AND USER_PLAYED.GAME_ID=GAMES.GAME_ID;"
        cursor.execute(sql)
        result = cursor.fetchall()

        user_played = []

        for r in result:
            ID = r[0]
            Name = r[1]
            Rating = r[2]
            row = {'ID':ID, 'Name':Name, 'Rating':Rating}
            user_played.append(row)

        cursor = connection.cursor()
        sql = "SELECT * FROM (SELECT GAMES.NAME, TO_CHAR(STUD_PUBLISHED.DATE_RELEASED, 'Mon dd, yyyy') AS \"DATE\", GAMES.GAME_ID FROM GAMES, STUD_PUBLISHED WHERE STUD_PUBLISHED.GAME_ID = GAMES.GAME_ID ORDER BY DATE_RELEASED DESC ) WHERE ROWNUM <=5;"
        cursor.execute(sql)
        result = cursor.fetchall()

        latest_released = []

        for r in result:
            ID = r[2]
            Name = r[0]
            Date = r[1]
            row = {'ID':ID, 'Name':Name, 'Date':Date}
            latest_released.append(row)

        cursor = connection.cursor()
        sql = "SELECT USER_RANK FROM USERS WHERE USERNAME = '" + user + "';"
        cursor.execute(sql)
        result = cursor.fetchall()
        rank = result[0][0]
        print("Rank: " + str(rank))
        cursor.close()

        cursor = connection.cursor()
        sql = "SELECT TEXT FROM RANKS WHERE RANK = " + str(rank) + ";"
        cursor.execute(sql)
        result = cursor.fetchall()
        RankText = result[0][0]
        print("Level: " + str(RankText))
        cursor.close()

        return TemplateResponse(request, 'UserHome.html', {'username' : user, 'games' : latest_cracked_games, 'follows_game' : user_follows_g, 'played' : user_played, 'latest_released' : latest_released, 'rank' : rank, 'ranktext' : RankText})

    else:
        return redirect('index')

def AllRanksView(request, user):
    USERNAME = user
    AllUsers = request.session.get('username')
    if AllUsers is not None and USERNAME in AllUsers:
        cursor = connection.cursor()
        sql = "SELECT * FROM RANKS"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        rank_dict = []

        for r in result:
            rank = r[0]
            level = r[1]
            followable = r[2]
            playtoget = r[3]
            row = {'rank':rank, 'level':level, 'followable':followable, 'playtoget':playtoget}
            rank_dict.append(row)

        return TemplateResponse(request, 'Ranks.html', {'username': user, 'ranks': rank_dict})
