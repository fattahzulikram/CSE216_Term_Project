from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db import connection

class Users(models.Model):
    u_id = models.IntegerField(primary_key=True)
    name = models.TextField(null=False)  # This field type is a guess.
    password = models.TextField(null=False)  # This field type is a guess.
    email = models.TextField(unique=True, null=False)  # This field type is a guess.
    username = models.TextField(unique=True, blank=True, null=False)  # This field type is a guess.
    issuperuser = models.DecimalField(max_digits=1, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'users'

def AddNewUser(name, password, email, Uusername, issuperuser):

    cursor = connection.cursor()
    sql = "SELECT NVL(max(u_id), 0) FROM USERS;"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    last_user_id = result[0][0]
    u_id = last_user_id + 1

    cursor = connection.cursor()
    sql2 = "SELECT username, email FROM users"
    cursor.execute(sql2)
    users = cursor.fetchall()
    cursor.close()

    unique_username = True
    unique_email = True
    for user in users:
        if user[1] == email:
            unique_email = False
            print(user[0])
            break
        if user[0] == Uusername:
            print(user[1])
            unique_username = False
            break
    if not unique_email:
        print('Email Taken')
        return False
    if not unique_username:
        print('Username Taken')
        return False
    cursor = connection.cursor()
    sql = "INSERT INTO USERS VALUES(" + str(u_id) + ",\'" + str(name) + "\',\'" + str(password) + "\',\'" + str(email) + "\',\'" + str(Uusername) + "\'," + str(issuperuser) + ");"
    DjangoUser = User.objects.create_user(username=Uusername, email=email, password=password)
    DjangoUser.save()
    print("User saved")
    cursor.execute(sql)
    cursor.close()
    return True
