from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.db import connection
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout

# Create your views here.
def RegisterView(request):
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
        for user in users:
            print(user[0] + " " + user[1])
            if user[1] == email:
                unique_email = False
                print(user[0])
                break
            if user[0] == username:
                print(user[1])
                unique_username = False
                break
        if not unique_email:
            return render(request,'signup-emailTaken.html')
        if not unique_username:
            return render(request, 'signup-usernameTaken.html')
        print(name + " " + username + " " + password + " " + email)
        cursor = connection.cursor()
        sql = "INSERT INTO USERS VALUES(" + str(u_id) + ",\'" + name + "\',\'" + password + "\',\'" + email + "\',\'" + username + "\', 0, 1);"
        print(sql)
        cursor.execute(sql)
        cursor.close()
        print("User saved")
        request.session['username'] = username
        SuccessText = "Successfully Registered"
        Superuser = "0"
        return TemplateResponse(request, 'loginsuccess.html', { 'user': username, 'success': SuccessText, 'superuser': Superuser})
    else:
        return render(request,'signupview.html')


def LoginView(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        cursor = connection.cursor()
        sql = "SELECT username, password FROM USERS"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        matched = False
        print(username + ' ' + password)
        for r in result:
            if r[0]==username and check_password(password,r[1]):
                matched=True
                break
        if matched:
            request.session['username'] = username
            SuccessText = "Successfully Logged In"
            Superuser = "0"
            return TemplateResponse(request, 'loginsuccess.html', { 'user': username, 'success': SuccessText, 'superuser': Superuser})
        else:
            return render(request, 'loginfailed.html')
    else:
        return render(request, 'loginPage.html')

def HomepageView(request):
    logout(request)
    return render(request, 'index.html')
