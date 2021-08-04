from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection
from django.template.response import TemplateResponse
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings

# Create your views here.

USERNAME = ""

def AdminHomeView(request, user):
    AllUsers = request.session.get('admin')
    print(AllUsers)
    if AllUsers is not None and user in AllUsers:
        return render(request, 'adminHome.html', {'username':user})
    else:
        return redirect('index')

def AdminLoginView(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        cursor = connection.cursor()
        sql = "SELECT username, password, issuperuser FROM USERS"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        matched = False
        isAdmin = False
        for r in result:
            if r[0]==username and check_password(password,r[1]):
                matched=True
                if r[2]==1:
                    isAdmin = True
                break
        if matched and isAdmin:
            request.session['admin'] = username
            SuccessText = "Successfully Logged In As Admin"
            Superuser = "1"
            USERNAME = username
            return TemplateResponse(request, 'loginsuccess.html', { 'user': username, 'success': SuccessText, 'superuser': Superuser})
        else:
            return render(request, 'loginfailed.html')
    else:
        return render(request, 'adminLogin.html')

def AddGameView(request, user):
    print("Adding Game")
    if request.method=='POST':
        cursor = connection.cursor()
        sql = "SELECT NVL(max(GAME_ID), 0) FROM GAMES;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        last_game_id = result[0][0]
        game_id = last_game_id + 1
        name = request.POST['name']
        genre = request.POST['Genre']
        stud_dev = request.POST.get('std_dev', False)
        stud_pub = request.POST.get('std_pub', False)
        platform = request.POST['platform']
        protection = request.POST.get('protection', False)
        market = request.POST.get('market', False)
        cpu = request.POST['cpu']
        gpu = request.POST['gpu']
        ram = request.POST['ram']
        #wide_image = request.POST['wide_image']
        wimage = request.FILES.get('wide_image', False)
        if not ram:
            ram = "''"
        trailer = request.POST['trailer']
        #image = request.POST['image']
        img = request.FILES.get('image', False)
        description = request.POST['description']
        price = request.POST['price']
        date = request.POST['Date']

        if not name or not genre or not platform:
            failure = "Not Enough Information On Game"
            Superuser = "1"
            return TemplateResponse(request, 'ErrorTemplate.html', { 'user': user, 'failure': failure, 'superuser': Superuser})

        name = name.replace("'", "")
        description = description.replace("'", "")
        genre = genre.replace("'", "")
        cpu = cpu.replace("'", "")
        gpu = gpu.replace("'", "")

        if not date:
            date = "''"
        else:
            date = "TO_DATE('" + date + "', 'yyyy-mm-dd')"

        if not wimage:
            page_image = "images/GameImages/NoGame.png"
        else:
            destinationw = open("static\\images\\GameImages\\" + str(game_id) + "_2.jpg", 'wb+')
            for chunk in wimage.chunks():
                destinationw.write(chunk)
            destinationw.close()
            page_image = "images/GameImages/" + str(game_id) + "_2.jpg"

        if not img:
            normal_image = "images/GameImages/NoGame.png"
        else:
            destination = open("static\\images\\GameImages\\" +str(game_id) + ".jpg", 'wb+')
            for chunk in img.chunks():
                destination.write(chunk)
            destination.close()
            normal_image = "images/GameImages/" + str(game_id) + ".jpg"
        #Games Table
        cursor = connection.cursor()
        sql = "INSERT INTO GAMES VALUES(" + str(game_id) + ", '" + name + "', '" + genre + "', '" + platform + "', '"+ cpu + "', '"+ gpu + "', " + str(ram) + ", '" + trailer + "', '" + str(normal_image) + "', '" + description + "', '" + str(page_image) + "');"
        print(sql)
        cursor.execute(sql)
        cursor.close()

        #STUDIO
        cursor = connection.cursor()
        sql = "SELECT STD_ID FROM STUDIO WHERE NAME='" + str(stud_dev) + "';"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            dev_id = result[0][0]
        else:
            dev_id = -1
        cursor.close()

        cursor = connection.cursor()
        sql = "SELECT STD_ID FROM STUDIO WHERE NAME='" + str(stud_pub) + "';"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            pub_id = result[0][0]
        else:
            pub_id = -1
        cursor.close()

        if not dev_id == -1:
            cursor = connection.cursor()
            sql = "INSERT INTO STUD_DEVELOPED VALUES(" + str(game_id) + ", " + str(dev_id) + ");"
            cursor.execute(sql)
            cursor.close()

        if not pub_id == -1:
            cursor = connection.cursor()
            sql = "INSERT INTO STUD_PUBLISHED VALUES(" + str(game_id) + ", " + str(pub_id) + ", " + date + ");"
            cursor.execute(sql)
            cursor.close()

        #MARKETPLACE
        cursor = connection.cursor()
        sql = "SELECT MARKET_ID FROM MARKETPLACE WHERE NAME='" + str(market) + "';"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            market_id = result[0][0]
        else:
            market_id = -1
        cursor.close()

        if not market_id == -1:
            cursor = connection.cursor()
            sql = "INSERT INTO AVAILABLE_AT VALUES(" + str(game_id) + ", " + str(market_id) + ", " + price + ");"
            cursor.execute(sql)
            cursor.close()

        #PROTECTION
        cursor = connection.cursor()
        sql = "SELECT PRT_ID FROM PROTECTION WHERE NAME='" + str(protection) + "';"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            prt_id = result[0][0]
        else:
            prt_id = -1
        cursor.close()

        if not prt_id == -1:
            cursor = connection.cursor()
            sql = "INSERT INTO ENCRYPTED VALUES(" + str(game_id) + ", " + str(prt_id) +  ");"
            cursor.execute(sql)
            cursor.close()

        Success = "Successfully Added To Database"
        Superuser = "1"
        return TemplateResponse(request, 'AddSuccess.html', { 'user': user, 'success': Success, 'superuser': Superuser})
    else:
        cursor = connection.cursor()
        sql = "SELECT NAME FROM STUDIO;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        print(result)
        names = []
        for r in result:
            names.append(r[0])

        cursor = connection.cursor()
        sql = "SELECT NAME FROM PROTECTION;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        print(result)
        prts = []
        for r in result:
            prts.append(r[0])

        cursor = connection.cursor()
        sql = "SELECT NAME FROM MARKETPLACE;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        print(result)
        market = []
        for r in result:
            market.append(r[0])

        return render(request,'AddGamesView.html', {'user': USERNAME, 'studio_names': names, 'prts': prts, 'markets':market})

def AddCrackedGameView(request, user):
    if request.method=='POST':
        name = request.POST.get('name', False)
        cracker = request.POST.get('Cracker', False)
        date = request.POST['Date']
        if not date:
            date = "''"
        else:
            date = "TO_DATE('" + date + "', 'yyyy-mm-dd')"
        cursor = connection.cursor()
        sql = "SELECT GAME_ID FROM GAMES WHERE NAME = '" + str(name) + "';"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()

        cursor = connection.cursor()
        sql = "SELECT GROUP_ID FROM CRACK_GROUPS WHERE NAME = '" + str(cracker) + "';"
        cursor.execute(sql)
        cracker_result = cursor.fetchall()
        cursor.close()


        if not result:
            failure = "Game Does Not Exists In Database"
            Superuser = "1"
            return TemplateResponse(request, 'ErrorTemplate.html', { 'user': user, 'failure': failure, 'superuser': Superuser})
        elif not cracker_result:
            failure = "Group Does Not Exists In Database"
            Superuser = "1"
            return TemplateResponse(request, 'ErrorTemplate.html', { 'user': user, 'failure': failure, 'superuser': Superuser})
        else:
            game_id = result[0][0]
            group_id = cracker_result[0][0]
            cursor = connection.cursor()
            sql = "INSERT INTO CRACKED_GAME VALUES(" + str(game_id) + ", " + str(group_id) + ", " + date + ");"
            cursor.execute(sql)
            cursor.close()
            Success = "Successfully Added To Database"
            Superuser = "1"
            return TemplateResponse(request, 'AddSuccess.html', { 'user': user, 'success': Success, 'superuser': Superuser})
    else:
        cursor = connection.cursor()
        sql = "SELECT NAME FROM GAMES;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        print(result)
        names = []
        for r in result:
            names.append(r[0])

        cursor = connection.cursor()
        sql = "SELECT NAME FROM CRACK_GROUPS;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        print(result)
        crackers = []
        for r in result:
            crackers.append(r[0])

        return render(request,'AddCrackedGameView.html', {'user': USERNAME, 'games': names, 'crackers': crackers})

def AddStudioView(request, user):
    if request.method=='POST':
        name = request.POST['name']
        date = request.POST['Date']
        img = request.FILES.get('logo', False)
        description = request.POST['description']

        if not name:
            failure = "Not Enough Information"
            Superuser = "1"
            return TemplateResponse(request, 'ErrorTemplate.html', { 'user': user, 'failure': failure, 'superuser': Superuser})

        name = name.replace("'", "\'")
        description = description.replace("'", "")
        cursor = connection.cursor()
        sql = "SELECT NVL(max(STD_ID), 0) FROM STUDIO;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        last_std_id = result[0][0]
        studio_id = last_std_id + 1

        if not date:
            date = "''"
        else:
            date = "TO_DATE('" + date + "', 'yyyy-mm-dd')"

        if not img:
            normal_image = "images/GameImages/NoGame.png"
        else:
            destination = open("static\\images\\StudioLogo\\" + str(studio_id) + ".jpg", 'wb+')
            for chunk in img.chunks():
                destination.write(chunk)
            destination.close()
            normal_image = "images/StudioLogo/" + str(studio_id) + ".jpg"
        cursor = connection.cursor()
        sql = "INSERT INTO STUDIO VALUES(" + str(studio_id) + ", '" + name + "', " + date + ",'" + normal_image + "', '" + description + "');"
        cursor.execute(sql)
        cursor.close()
        Success = "Successfully Added To Database"
        Superuser = "1"
        return TemplateResponse(request, 'AddSuccess.html', { 'user': user, 'success': Success, 'superuser': Superuser})
    else:
        return render(request,'AddStudio.html', {'user': USERNAME})

def AddProtectionView(request, user):
    if request.method=='POST':
        name = request.POST['name']
        year = request.POST['year']
        company = request.POST['company']
        img = request.FILES.get('logo', False)
        description = request.POST['description']
        if not name:
            failure = "Not Enough Information"
            Superuser = "1"
            return TemplateResponse(request, 'ErrorTemplate.html', { 'user': user, 'failure': failure, 'superuser': Superuser})

        if not year:
            year = "''"
        if not company:
            company = ""
        name = name.replace("'", "")
        company = company.replace("'", "")
        description = description.replace("'", "")
        cursor = connection.cursor()
        sql = "SELECT NVL(max(PRT_ID), 0) FROM PROTECTION;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        last_prt_id = result[0][0]
        new_prt_id = last_prt_id + 1
        if not img:
            normal_image = "images/GameImages/NoGame.png"
        else:
            destination = open("static\\images\\ProtectionLogo\\" + str(new_prt_id) + ".jpg", 'wb+')
            for chunk in img.chunks():
                destination.write(chunk)
            destination.close()
            normal_image = "images/ProtectionLogo/" + str(new_prt_id) + ".jpg"

        cursor = connection.cursor()
        sql = "INSERT INTO PROTECTION VALUES(" + str(new_prt_id) + ", '" + name + "', " + year + ", '" + company + "', '" + normal_image + "', '" + description + "');"
        cursor.execute(sql)
        cursor.close()
        Success = "Successfully Added To Database"
        Superuser = "1"
        return TemplateResponse(request, 'AddSuccess.html', { 'user': user, 'success': Success, 'superuser': Superuser})
    else:
        return render(request,'AddProtection.html', {'user': USERNAME})

def AddCrackGroupView(request, user):
    if request.method=='POST':
        name = request.POST['name']
        url = request.POST['url']
        img = request.FILES.get('logo', False)
        description = request.POST['description']
        if not name:
            failure = "Not Enough Information"
            Superuser = "1"
            return TemplateResponse(request, 'ErrorTemplate.html', { 'user': user, 'failure': failure, 'superuser': Superuser})

        cursor = connection.cursor()
        sql = "SELECT NVL(max(GROUP_ID), 0) FROM CRACK_GROUPS;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        last_group_id = result[0][0]
        new_group_id = last_group_id + 1


        name = name.replace("'", "")
        description = description.replace("'", "")
        if not url:
            url = ""
        if not img:
            normal_image = "images/GameImages/NoGame.png"
        else:
            destination = open("static\\images\\GroupLogo\\" + str(new_group_id) + ".jpg", 'wb+')
            for chunk in img.chunks():
                destination.write(chunk)
            destination.close()
            normal_image = "images/GroupLogo/" + str(new_group_id) + ".jpg"
        cursor = connection.cursor()
        sql = "INSERT INTO CRACK_GROUPS VALUES(" + str(new_group_id) + ", '" + name + "', '" + url + "', '" + normal_image + "', '" + description + "');"
        cursor.execute(sql)
        cursor.close()
        Success = "Successfully Added To Database"
        Superuser = "1"
        return TemplateResponse(request, 'AddSuccess.html', { 'user': user, 'success': Success, 'superuser': Superuser})
    else:
        return render(request,'AddGroup.html', {'user': USERNAME})

def AddMarketplaceView(request, user):
    if request.method=='POST':
        name = request.POST['name']
        url = request.POST['url']
        img = request.FILES.get('logo', False)
        description = request.POST['description']
        if not name:
            failure = "Not Enough Information"
            Superuser = "1"
            return TemplateResponse(request, 'ErrorTemplate.html', { 'user': user, 'failure': failure, 'superuser': Superuser})

        name = name.replace("'", "")
        description = description.replace("'", "")
        cursor = connection.cursor()
        sql = "SELECT NVL(max(MARKET_ID), 0) FROM MARKETPLACE;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        last_market_id = result[0][0]
        new_market_id = last_market_id + 1


        if not url:
            url = ""
        if not img:
            normal_image = "images/GameImages/NoGame.png"
        else:
            destination = open("static\\images\\MarketplaceLogo\\" + str(new_market_id) + ".jpg", 'wb+')
            for chunk in img.chunks():
                destination.write(chunk)
            destination.close()
            normal_image = "images/MarketplaceLogo/" + str(new_market_id) + ".jpg"
        cursor = connection.cursor()
        sql = "INSERT INTO MARKETPLACE VALUES(" + str(new_market_id) + ", '" + name + "', '" + url + "', '" + normal_image + "', '" + description + "');"
        cursor.execute(sql)
        cursor.close()
        Success = "Successfully Added To Database"
        Superuser = "1"
        return TemplateResponse(request, 'AddSuccess.html', { 'user': user, 'success': Success, 'superuser': Superuser})
    else:
        return render(request,'AddMarketplace.html', {'user': USERNAME})

def CreateNewAdminView(request, user):
    if request.method=='POST':
        cursor = connection.cursor()
        sql = "SELECT NVL(max(u_id), 0) FROM USERS;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        last_user_id = result[0][0]
        u_id = last_user_id + 1
        name = request.POST['fullname']
        password = make_password(request.POST['password'])
        #password = POST['password']
        email = request.POST['email']
        username = request.POST['username']
        cursor = connection.cursor()
        sql2 = "SELECT username, email FROM users"
        cursor.execute(sql2)
        users = cursor.fetchall()
        cursor.close()

        unique_username = True
        unique_email = True
        for u in users:
            print(u[0] + " " + u[1])
            if u[1] == email:
                unique_email = False
                print(u[0])
                break
            if u[0] == username:
                print(u[1])
                unique_username = False
                break
        if not unique_email:
            return render(request,'AdminEmailTaken.html', {'user': USERNAME})
        if not unique_username:
            return render(request, 'AdminUsernameTaken.html', {'user': USERNAME})
        print(name + " " + username + " " + password + " " + email)
        cursor = connection.cursor()
        sql = "INSERT INTO USERS VALUES(" + str(u_id) + ",\'" + name + "\',\'" + password + "\',\'" + email + "\',\'" + username + "\', 1, 1);"
        print(sql)
        cursor.execute(sql)
        cursor.close()
        print("User saved")
        Success = "Successfully Created Admin"
        Superuser = "1"
        return TemplateResponse(request, 'AddSuccess.html', { 'user': user, 'success': Success, 'superuser': Superuser})
    else:
        return render(request,'CreateAdmin.html', {'user': USERNAME})

def DemoUpload(request, user):
    if request.method == 'POST':
        image = request.FILES['demo']
        destination = open("adminHome\\static\\images\\" +image.name, 'wb+')
        print(settings.STATIC_ROOT)
        for chunk in image.chunks():
            destination.write(chunk)
        destination.close()
        return render(request, 'adminHome.html', {'username':user})
    else:
        return render(request,'DemoUpload.html', {'user': USERNAME})

def AddMarketplaceToGame(request, user):
    if request.method=='POST':
        game = request.POST.get('game', False)
        market = request.POST.get('market', False)
        price = request.POST['price']
        if not game or not market or not price:
            print(game)
            print(market)
            print(price)
            failure = "Not enough Information"
            Superuser = "1"
            return TemplateResponse(request, 'ErrorTemplate.html', { 'user': user, 'failure': failure, 'superuser': Superuser})

        cursor = connection.cursor()
        sql = "SELECT GAME_ID FROM GAMES WHERE NAME = '" + str(game) +"';"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        game_id = result[0][0]

        cursor = connection.cursor()
        sql = "SELECT MARKET_ID FROM MARKETPLACE WHERE NAME = '" + str(market) +"';"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        market_id = result[0][0]

        cursor = connection.cursor()
        sql = "SELECT COUNT(1) FROM AVAILABLE_AT WHERE GAME_ID = " + str(game_id) + " AND MARKET_ID = " + str(market_id) + ";"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        already_input = result[0][0]

        if not already_input == 0:
            cursor = connection.cursor()
            sql = "DELETE FROM AVAILABLE_AT WHERE GAME_ID = " + str(game_id) + " AND MARKET_ID = " + str(market_id) + ";"
            cursor.execute(sql)
            cursor.close()

        cursor = connection.cursor()
        sql = "INSERT INTO AVAILABLE_AT VALUES(" + str(game_id) + ", " + str(market_id) + ", " + str(price) + ");"
        cursor.execute(sql)
        cursor.close()

        Success = "Successfully Added To Database"
        Superuser = "1"
        return TemplateResponse(request, 'AddSuccess.html', { 'user': user, 'success': Success, 'superuser': Superuser})
    else:
        cursor = connection.cursor()
        sql = "SELECT NAME FROM GAMES;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        print(result)
        names = []
        for r in result:
            names.append(r[0])

        cursor = connection.cursor()
        sql = "SELECT NAME FROM MARKETPLACE;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        print(result)
        markets = []
        for r in result:
            markets.append(r[0])

        return render(request,'AddAvailableAt.html', {'user': USERNAME, 'games': names, 'markets': markets})
