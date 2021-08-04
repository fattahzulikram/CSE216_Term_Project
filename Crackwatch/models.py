# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AvailableAt(models.Model):
    game = models.ForeignKey('Games', models.DO_NOTHING, blank=True, null=True)
    market = models.ForeignKey('Marketplace', models.DO_NOTHING, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'available_at'


class CrackGroups(models.Model):
    group_id = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)  # This field type is a guess.
    url = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'crack_groups'


class CrackedGame(models.Model):
    game = models.ForeignKey('Games', models.DO_NOTHING, blank=True, null=True)
    group = models.ForeignKey(CrackGroups, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cracked_game'


class Encrypted(models.Model):
    game = models.ForeignKey('Games', models.DO_NOTHING, blank=True, null=True)
    prt = models.ForeignKey('Protection', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'encrypted'


class Games(models.Model):
    game_id = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)  # This field type is a guess.
    genre = models.TextField(unique=True)  # This field type is a guess.
    platform = models.TextField(unique=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'games'


class Marketplace(models.Model):
    market_id = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)  # This field type is a guess.
    url = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'marketplace'


class Protection(models.Model):
    prt_id = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)  # This field type is a guess.
    year = models.IntegerField(blank=True, null=True)
    company = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'protection'


class StudDeveloped(models.Model):
    game = models.ForeignKey(Games, models.DO_NOTHING, blank=True, null=True)
    std = models.ForeignKey('Studio', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stud_developed'


class StudPublished(models.Model):
    game = models.ForeignKey(Games, models.DO_NOTHING, blank=True, null=True)
    std = models.ForeignKey('Studio', models.DO_NOTHING, blank=True, null=True)
    date_released = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'stud_published'


class Studio(models.Model):
    std_id = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)  # This field type is a guess.
    est_year = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'studio'


class UserFollowsC(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    group = models.ForeignKey(CrackGroups, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_follows_c'


class UserFollowsG(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    game = models.ForeignKey(Games, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_follows_g'


class UserPlayed(models.Model):
    u = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    game = models.ForeignKey(Games, models.DO_NOTHING, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_played'


class Users(models.Model):
    u_id = models.IntegerField(primary_key=True)
    name = models.TextField(unique=True)  # This field type is a guess.
    password = models.TextField(unique=True)  # This field type is a guess.
    email = models.TextField(unique=True)  # This field type is a guess.
    username = models.TextField(unique=True, blank=True, null=True)  # This field type is a guess.
    issuperuser = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'users'
