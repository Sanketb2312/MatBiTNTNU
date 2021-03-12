# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Arrangement(models.Model):
    events = models.Manager()

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
    arrangementinnholdid = models.AutoField(db_column='ArrangementinnholdID', primary_key=True)  # Field name made lowercase.
    arrangementid = models.IntegerField(db_column='ArrangementID')  # Field name made lowercase.
    innholdid = models.IntegerField(db_column='InnholdID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'arrangementinnhold'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bruker(models.Model):
    users = people = models.Manager()

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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Harallergi(models.Model):
    harallergiid = models.AutoField(db_column='HarallergiID', primary_key=True)  # Field name made lowercase.
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
    paameldingid = models.AutoField(db_column='PaameldingID', primary_key=True)  # Field name made lowercase.
    brukerid = models.IntegerField(db_column='BrukerID')  # Field name made lowercase.
    arrangementid = models.IntegerField(db_column='ArrangementID')  # Field name made lowercase.
    tidspunkt = models.DateTimeField(db_column='Tidspunkt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pamelding'


class Vertskap(models.Model):
    vertskapid = models.AutoField(db_column='VertskapID', primary_key=True)  # Field name made lowercase.
    brukerid = models.IntegerField(db_column='BrukerID')  # Field name made lowercase.
    arrangementid = models.IntegerField(db_column='ArrangementID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vertskap'
