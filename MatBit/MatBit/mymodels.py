# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Arrangement(models.Model):
    arrangementid = models.AutoField(db_column='ArrangementID', primary_key=True)  # Field name made lowercase.
    arrangementnavn = models.CharField(db_column='ArrangementNavn', max_length=256)  # Field name made lowercase.
    beskrivelse = models.TextField(db_column='Beskrivelse', blank=True, null=True)  # Field name made lowercase.
    antallplasser = models.IntegerField(db_column='AntallPlasser', blank=True, null=True)  # Field name made lowercase.
    lokasjon = models.CharField(db_column='Lokasjon', max_length=128, blank=True, null=True)  # Field name made lowercase.
    tidspunkt = models.DateTimeField(db_column='Tidspunkt', blank=True, null=True)  # Field name made lowercase.
    opprettet = models.DateTimeField(db_column='Opprettet')  # Field name made lowercase.
    pris = models.IntegerField(db_column='Pris', blank=True, null=True)  # Field name made lowercase.
    avlyst = models.IntegerField(db_column='Avlyst')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'arrangement'


class Arrangementinnhold(models.Model):
    arrangementid = models.IntegerField(db_column='ArrangementID')  # Field name made lowercase.
    innholdid = models.IntegerField(db_column='InnholdID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'arrangementinnhold'


class Bruker(models.Model):
    brukerid = models.AutoField(db_column='BrukerID', primary_key=True)  # Field name made lowercase.
    fornavn = models.CharField(db_column='Fornavn', max_length=128)  # Field name made lowercase.
    etternavn = models.CharField(db_column='Etternavn', max_length=128)  # Field name made lowercase.
    fodselsdato = models.DateTimeField(db_column='Fodselsdato', blank=True, null=True)  # Field name made lowercase.
    adresse = models.CharField(db_column='Adresse', max_length=128, blank=True, null=True)  # Field name made lowercase.
    postnummer = models.IntegerField(db_column='Postnummer', blank=True, null=True)  # Field name made lowercase.
    sted = models.CharField(db_column='Sted', max_length=128, blank=True, null=True)  # Field name made lowercase.
    eradministrator = models.IntegerField(db_column='ErAdministrator')  # Field name made lowercase.
    epost = models.CharField(db_column='Epost', max_length=128)  # Field name made lowercase.
    passord = models.CharField(db_column='Passord', max_length=256)  # Field name made lowercase.
    passordhash = models.CharField(db_column='PassordHash', max_length=256)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bruker'


class Harallergi(models.Model):
    brukerid = models.IntegerField(db_column='BrukerID')  # Field name made lowercase.
    innholdid = models.IntegerField(db_column='InnholdID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'harallergi'


class Innhold(models.Model):
    innholdid = models.AutoField(db_column='InnholdID', primary_key=True)  # Field name made lowercase.
    navn = models.CharField(db_column='Navn', max_length=128)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'innhold'


class Pamelding(models.Model):
    brukerid = models.IntegerField(db_column='BrukerID')  # Field name made lowercase.
    arrangementid = models.IntegerField(db_column='ArrangementID')  # Field name made lowercase.
    tidspunkt = models.DateTimeField(db_column='Tidspunkt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pamelding'


class Vertskap(models.Model):
    brukerid = models.IntegerField(db_column='BrukerID')  # Field name made lowercase.
    arrangementid = models.IntegerField(db_column='ArrangementID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vertskap'
